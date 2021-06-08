from pika import BlockingConnection
from pika import ConnectionParameters
import logging


class MetaClass(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        """ Singleton Pattern """
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class RabbitMQReceiver(metaclass=MetaClass):
    __slots__ = ["_configuration", "_connection", "_channel", "_queue", "_routing_key", "_exchange",
                 "_on_message_callback"]

    def __init__(self, configuration, exchange, routing_key=''):
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
        self._routing_key = routing_key
        self._exchange = exchange
        self._channel.queue_declare(queue=self._queue, durable=self._configuration.durable)
        self._channel.exchange_declare(exchange=exchange,
                                       exchange_type='fanout',
                                       durable=True)
        self._channel.queue_bind(queue=self._queue,
                                 exchange=self._exchange,
                                 routing_key=self._routing_key)
        self._on_message_callback = None

    def add_on_message_callback(self, on_message_callback):
        """
        Add function callback
        :param self:
        :param on_message_callback: function where the message is consumed
        :return: None
        """
        self._on_message_callback = on_message_callback

    def start_consuming(self):
        """ Start consumer with earlier defined callback """
        logging.info(f"Listening to {self._queue} queue\n")
        self._channel.basic_consume(queue=self._queue,
                                    on_message_callback=self._on_message_callback,
                                    auto_ack=True)
        self._channel.start_consuming()
