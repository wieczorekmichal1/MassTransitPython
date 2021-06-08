from pika import BlockingConnection
from pika import ConnectionParameters
from json import dumps
import logging


class RabbitMQSender(object):
    __slots__ = ["_configuration", "_connection", "_channel", "_queue", "_routing_key", "_exchange"]

    def __init__(self, configuration):
        """
        Create RabbitMQ Sender
        :param configuration: RabbitMQConfiguration object
        """
        self._configuration = configuration
        self._connection = BlockingConnection(ConnectionParameters(host=self._configuration.host,
                                                                   port=self._configuration.port,
                                                                   virtual_host=self._configuration.virtual_host,
                                                                   credentials=self._configuration.credentials))
        self._channel = self._connection.channel()
        self._queue = self._configuration.queue
        self._channel.queue_declare(queue=self._queue, self._configuration.durable)
        self._routing_key = ''
        self._exchange = ''

    def __enter__(self):
        return self

    def set_routing_key(self, routing_key=''):
        """ Set routing key """
        self._routing_key = routing_key

    def set_exchange(self, exchange=''):
        """ Set exchange """
        self._exchange = exchange

    def publish(self, message):
        """
        Publish message
        :param message: JSON string
        :return: None
        """
        self._channel.basic_publish(exchange=self._exchange,
                                    routing_key=self._routing_key,
                                    body=message)
        logging.info(f"Message published to {self._queue} queue\n")

    def create_masstransit_response(self, message, request_body):
        response = {
            "messageId": request_body['messageId'],
            "conversationId": request_body['conversationId'],
            "sourceAddress": request_body['sourceAddress'],
            "destinationAddress": request_body['destinationAddress'],
            "messageType": ['urn:message:' + self._exchange],
            "message": message
        }
        return dumps(response)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()
