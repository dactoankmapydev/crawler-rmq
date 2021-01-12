import pika, requests

def setup(queue_name):
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5673,credentials=pika.PlainCredentials(username='test',password='test')))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672,credentials=pika.PlainCredentials(username='guest',password='guest')))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    return connection, channel
