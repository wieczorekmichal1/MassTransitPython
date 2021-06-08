class RabbitMQConfiguration(object):
    """ Create RabbitMQ Configuration """
    def __init__(self, credentials, queue='DefaultQueue', host='localhost', port='5672', virtual_host='/', durable=False):
        self.credentials = credentials
        self.queue = queue
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.durable = durable
