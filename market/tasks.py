import json
import requests
from coinMena.celery import app as celery_app
from .models import Rate, Currency
from django.conf import settings


API_KEY = settings.API_KEY
EXCHANGE_BTC_USD_URL = settings.EXCHANGE_BTC_USD_URL

@celery_app.task
def fetch_exchange_every_hour():
    print('#### started hourly scheduled task to fetch BTC/USD exchange rate ####')
    url = f'{EXCHANGE_BTC_USD_URL}{API_KEY}'
    res = requests.get(
        url
    )
    if res.status_code == 200:
        print(f'#### Data fetch success with status: {res.status_code} ####')
        response_data = res.json()['Realtime Currency Exchange Rate']
        rate_obj = Rate.objects.create(
            exchange_rate=response_data['5. Exchange Rate'],
            bid_price=response_data['8. Bid Price'],
            ask_price=response_data['9. Ask Price']
        )

        exchange_name = str(response_data['1. From_Currency Code'] + '/' + response_data['3. To_Currency Code'])
        currency_filter = Currency.objects.filter(name=exchange_name)
        if not currency_filter:
            currency_obj = Currency.objects.create(
                name=exchange_name
            )
        else:
            currency_obj = currency_filter[0]

        currency_obj.rate.add(rate_obj)
        response = True
    else:
        error = res.json()
        response = False
        print(f'#### Data fetch failed with status: {res.status_code} && with reason {error} ####')

    print('#### Ending hourly scheduled task to fetch BTC/USD exchange rate ####')
    return response