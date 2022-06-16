import requests
import keys
import pandas as pd
from time import sleep


def get_crypto_rates(base_currency='USD', assets='BTC,ETH,XRP'):
    url = 'https://api.nomics.com/v1/currencies/ticker'

    payload = {'key': keys.NOMIC_API_KEY,
               'convert': base_currency, 'ids': assets, 'interval': '1d'}
    response = requests.get(url, params=payload)
    data = response.json()

   # print(data)

    crypto_currency, crypto_price, price_timestamp = [], [], []

    for asset in data:
        crypto_currency.append(asset['currency'])
        crypto_price.append(asset['price'])
        price_timestamp.append(asset['price_timestamp'])

    raw_data = {
        'assets': crypto_currency,
        'rates': crypto_price,
        'timestamp': price_timestamp
    }

    df = pd.DataFrame(raw_data)
    return df


def set_alert(dataframe, asset, alert_high_price):
    crypto_value = float(
        dataframe[dataframe['assets'] == asset]['rates'].item())

    details = f'{asset}: {crypto_value}, Traget {alert_high_price}'

    if crypto_value >= alert_high_price:
        print(details + ' << TARGET VALUE REACHED!')
    else:
        print(details)


# Alert While loop
loop = 0

while True:
    print(
        f'----------------------------------({loop})----------------------------------')

    try:
        df = get_crypto_rates()

        set_alert(df, 'BTC', 30000)
        set_alert(df, 'ETH', 1000)
        set_alert(df, 'XRP', .6)
    except Exception as e:
        print('Couldn\'t retrieve the data... Trying again.')

    loop += 1
    sleep(30)
