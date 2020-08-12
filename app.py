import requests, json
from chalice import Chalice

app = Chalice(app_name='buy_stock')

API_KEY = 'Enter API Key'
SECRET_KEY = 'Enter API Secret'
BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    request = app.current_request
    webhook_message = request.json_body

    data = {
        "symbol": webhook_message['ticker'],
        "qty": 1,
        "side": "buy",
        "type": "limit",
        "limit_price": webhook_message['close'],
        "time_in_force": "gtc",
        "order_class": "bracket",
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    response = json.loads(r.content) 

    return {
        'webhook_message': webhook_message,
        'id': response['id'],
        'client_order_id': response['client_order_id']
    }
