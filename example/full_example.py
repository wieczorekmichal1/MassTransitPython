from pika import PlainCredentials
from masstransitpython import RabbitMQConfiguration
from masstransitpython import RabbitMQReceiver
from masstransitpython import RabbitMQSender
from threading import Thread
from json import loads, JSONEncoder

RABBITMQ_USERNAME = 'rabbitmq'
RABBITMQ_PASSWORD = 'rabbitmq'
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5900
RABBITMQ_VIRTUAL_HOST = '/epicservices'


class SampleMessage:
    def __init__(self, name):
        self.name = name


class MessageEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def handler(ch, method, properties, body):
    msg = loads(body.decode())
    print("Received message: %s" % msg["message"])

    t = Thread(target=send_message(msg))
    t.start()
    threads.append(t)


def send_message(body):
    # configure publisher
    sender_conf = RabbitMQConfiguration(credentials,
                                        queue='MassTransitServiceQueue',
                                        host=RABBITMQ_HOST,
                                        port=RABBITMQ_PORT,
                                        virtual_host=RABBITMQ_VIRTUAL_HOST)
    # create sender and send a value
    with RabbitMQSender(sender_conf) as sender:
        sender.set_exchange('MassTransitService.Messages:SampleMessage')

        encoded_msg = MessageEncoder().encode(SampleMessage("Hello World!"))
        response = sender.create_masstransit_response(loads(encoded_msg), body)
        sender.publish(message=response)


if __name__ == "__main__":
    # define thread container
    threads = []

    # define credentials and configuration for receiver
    credentials = PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    conf = RabbitMQConfiguration(credentials,
                                 queue='PythonServiceQueue',
                                 host=RABBITMQ_HOST,
                                 port=RABBITMQ_PORT,
                                 virtual_host=RABBITMQ_VIRTUAL_HOST)

    # define receiver
    receiver = RabbitMQReceiver(conf, 'MassTransitService.Messages:SampleMessage')
    receiver.add_on_message_callback(handler)
    receiver.start_consuming()

