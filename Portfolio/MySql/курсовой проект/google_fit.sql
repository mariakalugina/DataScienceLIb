-- Создаем таблицы БД Google Fit
DROP DATABASE google_fit;
CREATE DATABASE google_fit;
USE google_fit;

CREATE TABLE users (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT "Идентификатор строки", 
  first_name VARCHAR(100) NOT NULL COMMENT "Имя пользователя",
  last_name VARCHAR(100) NOT NULL COMMENT "Фамилия пользователя",
  email VARCHAR(100) NOT NULL UNIQUE COMMENT "Почта",
  phone VARCHAR(100) NOT NULL UNIQUE COMMENT "Телефон",
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT "Время создания строки",  
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "Время обновления строки"
) COMMENT "Пользователи";  

DROP TABLE IF EXISTS profiles;
-- Таблица профилей
CREATE TABLE profiles (
  user_id INT UNSIGNED NOT NULL PRIMARY KEY COMMENT "Ссылка на пользователя", 
  gender CHAR(1) NOT NULL COMMENT "Пол",
  birthday DATE COMMENT "Дата рождения",
  city_id INT UNSIGNED COMMENT " ссылка на город проживания",
  height INT UNSIGNED COMMENT "РОСТ В САНТИМЕТРАХ",
  weight FLOAT UNSIGNED COMMENT "ВЕС В КГ",
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT "Время создания строки",  
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "Время обновления строки"
) COMMENT "Профили";

DROP TABLE IF EXISTS countries;
CREATE TABLE cities (
  id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT "Идентификатор города", 
  name VARCHAR(100) NOT NULL,
  country_id INT UNSIGNED NOT NULL COMMENT "Ссылка на страну проживания"
) COMMENT "Справочник городов";

DROP TABLE IF EXISTS countries;
CREATE TABLE countries (
  id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT "Идентификатор страны", 
  name VARCHAR(100) NOT NULL  COMMENT "Название страны"
)COMMENT "Справочник стран";


CREATE TABLE perposes (
	user_id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT "Ссылка на пользователя",
	points INT UNSIGNED NOT NULL COMMENT "Ежедневная цель в баллах кардиотренеровки",
	steps INT UNSIGNED NOT NULL COMMENT "Ежедневная цель в шагах",
	time_to_go_to_bed TIME COMMENT "Желаемое время отхода ко сну",
	time_to_wake_up TIME COMMENT "Желаемое время подъема"
)COMMENT "Ежедневные цели пользователя";

CREATE TABLE types_of_trainings 
(
	id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT "Идентификатор типа тренировки",
	name  VARCHAR(100)  NOT NULL  COMMENT "Название тренировки",
	cardio_intencity INT UNSIGNED NOT NULL COMMENT "Кардио интенсивность тренировки по умолчанию в час",
	kkal_hour INT UNSIGNED NOT NULL COMMENT "Количество сжигаемых каллорий в час",
	steps_hour INT UNSIGNED NOT NULL COMMENT "Количество шагов во время тренировки в час"

) COMMENT "Справочник типов тренеровки";
DROP TABLE IF EXISTS trainings;
CREATE TABLE trainings
(
   id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT  COMMENT "Идентификатор тренировки",
   user_id INT UNSIGNED NOT NULL COMMENT "Ссылка на пользователя",
   type_of_training_id INT UNSIGNED NOT NULL COMMENT "Ссылка на тип тренировки",
   started_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT "Время начала тренировки",
   finished_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT "Время окончания тренировки",
   updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "Время создания и обновления строки",
   cardio_intencity INT UNSIGNED NOT NULL COMMENT "Кардио интенсивность тренировки, которую задает пользователь",
   kkal INT UNSIGNED NOT NULL COMMENT "Количество сожженных каллорий, которые задает пользоваель",
   steps INT UNSIGNED NOT NULL COMMENT "Количество пройденных шагов, которые задает пользоваель",
   comment VARCHAR(255) COMMENT "Примечание к тренировке"

)COMMENT "Тренировки пользователей";

-- Добавляем внешние ключ
ALTER TABLE profiles
  ADD CONSTRAINT profiles_user_id_fk 
    FOREIGN KEY (user_id) REFERENCES users(id),
   ADD CONSTRAINT profiles_city_id_fk 
    FOREIGN KEY (city_id) REFERENCES cities(id);
   
ALTER TABLE cities
  ADD CONSTRAINT cities_country_id_fk 
    FOREIGN KEY (country_id) REFERENCES countries(id);   
   
ALTER TABLE perposes
  ADD CONSTRAINT perposes_user_id_fk 
    FOREIGN KEY (user_id) REFERENCES users(id); 

   
ALTER TABLE trainings
  ADD CONSTRAINT trainings_user_id_fk 
    FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE trainings 
  ADD CONSTRAINT trainings_type_of_training_idfk
    FOREIGN KEY (type_of_training_id) REFERENCES types_of_trainings(id);  

 
   -- Вносим изменения - не работает
ALTER TABLE profiles MODIFY COLUMN gender ENUM('M', 'F') NOT NULL;
   
-- приводим данные в порядок
-- Приводим в порядок временные метки
UPDATE users SET updated_at = NOW() WHERE updated_at < created_at;    

UPDATE profiles SET updated_at = NOW() WHERE updated_at < created_at;
-- Поправим столбец пола
CREATE TEMPORARY TABLE genders (name CHAR(1));

INSERT INTO genders VALUES ('M'), ('F'); 

SELECT * FROM genders;

-- Обновляем пол
UPDATE profiles 
  SET gender = (SELECT name FROM genders ORDER BY RAND() LIMIT 1);
 
SELECT * FROM profiles; 


-- Приводим в порядок временные метки
UPDATE trainings SET updated_at = NOW() WHERE updated_at < finished_at ;    

-- Приводим в порядок временные метки
UPDATE trainings SET finished_at = NOW() WHERE started_at > finished_at ;


-- создаем индексы
CREATE INDEX users_last_name_idx ON users(last_name);
CREATE INDEX users__first_name_last_name_idx ON users(last_name, first_name);
  
CREATE INDEX types_of_trainings_idx ON types_of_trainings(name);
   
CREATE INDEX cities ON cities(name);
CREATE INDEX trainings_started_at ON trainings(started_at);
CREATE INDEX trainings_finished ON trainings(finished_at);


-- запросы
-- сумма баллов кардиотренировок за последнюю неделю для каждого пользователя

SELECT CONCAT(u.first_name,' ', u.last_name), SUM(t.cardio_intencity) 
FROM users u 
	LEFT JOIN trainings t ON u.id=t.user_id 
	LEFT JOIN types_of_trainings tot ON tot.id = t.type_of_training_id  
	WHERE t.started_at >= DATE_SUB(CURRENT_DATE() , INTERVAL 7 DAY)
GROUP BY u.id;

-- количество шагов за текущий день для определенного пользователя c ID = 20
SELECT  SUM(t.steps) FROM users u 
	LEFT JOIN trainings t 
	       ON u.id=t.user_id
   -- WHERE t.started_at >= DATE_SUB(CURRENT_DATE() , INTERVAL 1 DAY) 
   WHERE t.started_at >= (CURRENT_DATE() )
    AND (u.id = 20)
GROUP BY user_id;

-- запрос определяет достиг ли пользователь целей 
-- по тренировкам за этот день
SELECT 
CASE WHEN 
		(SELECT SUM(t.steps) 
		    FROM trainings t 
		    WHERE (t.started_at >= CURRENT_DATE)
		    AND (user_id = 20) GROUP BY t.user_id) > 
		(SELECT steps FROM perposes WHERE user_id = 20)
 		THEN
	    'Пользователь достиг цели по шагам на сегодня'
		ELSE 
		'Пользователь не достиг целей на сегодня'
	END;

-- запрос определяет, кто больше прошел шагов за текущий год - мужчины или женщины

SELECT 
CASE WHEN 
		(SELECT SUM(t2.steps) 
		FROM users 
		JOIN  trainings t2 
		  ON t2.user_id = users.id 
		JOIN profiles p2
		  ON users.id = p2.user_id 
		WHERE p2.gender = 'F')		
			 >
		(SELECT SUM(t3.steps) 
		FROM users 
		JOIN  trainings t3 
		  ON t3.user_id = users.id 
		JOIN profiles p2
		  ON users.id = p2.user_id 
		WHERE p2.gender = 'M')
 		THEN
	    'Женщины прошли больше шагов'
		ELSE 
		'Мужчины прошли больше лайков'
	END;
	



-- создаем представление, которое показывает тренировки всех пользователей 
-- за текущий месяц,сортированные по пользователям
DROP VIEW IF EXISTS tr_for_month;
CREATE VIEW tr_for_month AS 
SELECT u.id, CONCAT(u.last_name,' ', u.first_name), 
    t.started_at, t.finished_at,  t.cardio_intencity, t.steps
  FROM users u 
   LEFT JOIN trainings t 
          ON u.id = t.user_id 
   WHERE (t.started_at >= DATE_FORMAT(NOW(), '%Y-%m-1'))
  ORDER BY u.id, t.started_at;
 
 SELECT * FROM tr_for_month;

DROP VIEW IF EXISTS tr_for_cities_for_month;
CREATE VIEW tr_for_cities_for_month AS 
SELECT DISTINCT c.id, c.name, CONCAT(u.last_name,' ', u.first_name), 
    SUM(t.cardio_intencity) OVER (PARTITION BY u.id)
  FROM cities c 
  LEFT JOIN profiles p 
         ON c.id = p.city_id
  LEFT JOIN users u
         ON u.id=p.user_id 
  LEFT JOIN trainings t 
          ON u.id = t.user_id
  WHERE (t.started_at >= DATE_FORMAT(NOW(), '%Y-%m-1'))
  ORDER BY c.name, t.started_at;
 
 SELECT * FROM tr_for_cities_for_month;

-- создаем представление, которое содержит выборку - пользователи в каждом городе и сумма 
-- баллов кардиотренировки, которые они получили за последний месяц
DROP VIEW IF EXISTS tr_for_cities_for_month;
CREATE VIEW tr_for_cities_for_month AS 
SELECT  c.id, c.name, CONCAT(u.last_name,' ', u.first_name), 
-- SEC_TO_TIME((SUM(t.finished_at-t.started_at) OVER (PARTITION BY u.id))),
    (SUM(t.cardio_intencity) OVER (PARTITION BY u.id))
  FROM cities c 
  LEFT JOIN profiles p 
         ON c.id = p.city_id
  LEFT JOIN users u
         ON u.id=p.user_id 
  LEFT JOIN trainings t 
          ON u.id = t.user_id
  WHERE (t.started_at >= DATE_FORMAT(NOW(), '%Y-%m-1'))
  ORDER BY c.name;

 
 -- хранимые процедуры и функции
-- функция опредялет, достиг ли пользователь цели за неделю по шагам. 
-- возвращает TRUE, если достиг цели, и FALSE в обратном случае
-- параметр new_user_id - ID пользователя
DROP FUNCTION IF EXISTS is_get_steps_perpose;
DELIMITER //
CREATE FUNCTION is_get_steps_perpose(new_user_id INT)
RETURNS BOOLEAN 
   READS SQL DATA
   NOT DETERMINISTIC
  BEGIN
	 DECLARE number_steps INT;
     DECLARE perpose_for_week INT;
    
     SELECT SUM(t.steps) INTO number_steps FROM users u 
	   LEFT JOIN trainings t 
	       ON u.id=t.user_id
      WHERE t.started_at >= DATE_SUB(CURRENT_DATE() , INTERVAL 7 DAY) 
      AND (u.id = new_user_id)
      GROUP BY u.id;

     SELECT p2.steps INTO perpose_for_week FROM perposes p2
	  WHERE (p2.user_id = new_user_id) LIMIT 1;
	  
	 SET perpose_for_week  = perpose_for_week * 7;  
       RETURN (number_steps  >= perpose_for_week);
 END//
DELIMITER ;
SELECT is_get_steps_perpose(20);

-- Создадим триггер для проверки валидности target_id и target_type_id

DROP TRIGGER IF EXISTS time_validation;
DELIMITER //
CREATE TRIGGER time_validation BEFORE INSERT ON trainings
FOR EACH ROW BEGIN
  IF (NEW.started_at>NEW.finished_at) THEN 
      	SIGNAL SQLSTATE "45000"
    	SET MESSAGE_TEXT = "Error adding training!";
  END IF;
END//
DELIMITER ;