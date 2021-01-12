import pika, helper
import requests
import math


OTX_API_KEY = '779cc51038ddb07c5f6abe0832fed858a6039b9e8cdb167d3191938c1391dbba'

headers = {
    'X-OTX-API-KEY': OTX_API_KEY
}

proxies = {
        'http': 'http://127.0.0.1:3131',
        'https': 'http://127.0.0.1:3131',
    }

def send_indicator(channel, message):
    channel.basic_publish(exchange='',
        routing_key='ioc_collector',
        body=message,
        properties=pika.BasicProperties(delivery_mode = 2))
    print("Sent %r" % message)

def run():
    connection, channel = helper.setup('ioc_collector')

    results = requests.get('https://otx.alienvault.com/api/v1/pulses/subscribed', headers=headers).json()
    page = math.ceil(results['count']/50)
    for page in range (1, page+1):
        data = requests.get('https://otx.alienvault.com/api/v1/pulses/subscribed?limit=50&page={}'.format(page), headers=headers).json()
        for item in data['results']:
            for value in item['indicators']:
                name_indicator = value['indicator']
                type_indicator = value['type']
                created = value['created']
                send_indicator(channel, name_indicator)
                send_indicator(channel, type_indicator)
                send_indicator(channel, created)
    connection.close()

if __name__ == "__main__":
    run()
