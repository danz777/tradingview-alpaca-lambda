import requests, json
from chalice import Chalice

app = Chalice(app_name='buylive')

API_KEY = 'apikey'
SECRET_KEY = 'secretkey'
BASE_URL = "https://api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/buylive', methods=['POST'])
def buylive():
    request = app.current_request
    webhook_message = request.json_body
    
    data = {
        "symbol": webhook_message['ticker'],
        "qty": '1',
        "side": 'buy',
        "type": 'market',
        "time_in_force": 'gtc'
    }
    
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    response = json.loads(r.content)
        
    return {
        'webhook_message': webhook_message,
        'id': response['id'],
        'client_order_id': response['client_order_id']
    }
