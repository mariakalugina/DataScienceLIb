# python-flask-docker
Итоговый проект курса "Машинное обучение в бизнесе"

Стек:

ML: sklearn, pandas, numpy, catboost
API: flask
Данные: с kaggle - "Heart Failure" https://www.kaggle.com/fedesoriano/heart-failure-prediction
Задача: предсказать, будет ли у пациента сердечная недостаточность (поле HeartDisease). Бинарная классификация

Используемые признаки:

- Age (int)
- Sex (text - M-F)
- ChestPainType (ASY, NAP, ATA, TA)
- Cholesterol (int)
- ExerciseAngina (N, Y)
- Oldpeak (float)
- ST_Slope (Flat,Up,Down)

Преобразования признаков: StandartScaler, OHEEncoder

Модель: catboost


