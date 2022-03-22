import requests

apikey = '9c3aa4ae952545dcaafc9421ae913158'

# долгота и широта
lat = 53.13
lon = 50.11
main_link = 'http://api.weatherbit.io/v2.0/current'
params = {'lat': lat, 'lon': lon, 'key': apikey, 'lang': 'ru'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'Accept': '*/*'}
try:
    response = requests.get(main_link, params=params, headers=headers)
    j_body = response.json()
    j_data = j_body['data'][0]
except:
    print('Ошибка')
    print({j_body.get('error')})
    j_data = None

if j_data:
    print(f"Погода в городе {j_data.get('city_name')}: {j_data.get('weather').get('description').lower()},\n "
          f"температура {j_data.get('temp')}\xb0 C (ощущается как {j_data.get('app_temp')} \xb0 C), \n ветер {j_data.get('wind_cdir_full')}"
          f" {j_data.get('wind_spd')} м/c, отн. влажность воздуха: {j_data.get('rh')} %")
