from decimal import Decimal
while True:
    number = input('Введите число в формете AAA.BB: ')
    try:
        number = Decimal(number)
    except:
        print('Неверный формат данных')
    else:
        rubles = int(number)
        kop = int(100 * (number - rubles))
        break

print(f'Результат: {rubles} рублей {kop} копеек')
