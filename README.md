# Description
Python library to exchange messages between MassTransit RabbitMQ Client and Python application.

## Installation
Run the following to install:
```python
pip install masstransitpython
```

## Usage
Simple receiver/sender model was implemented to show basic package usage.

### Configuration
Default client configuration can be implemented as follows:
```python
from pika import PlainCredentials
from RabbitMQConfiguration import RabbitMQConfiguration

RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_VIRTUAL_HOST = '/'

credentials = PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
conf = RabbitMQConfiguration(credentials, 
                             queue='PythonServiceQueue', 
                             host=RABBITMQ_HOST, 
                             port=RABBITMQ_PORT,
                             virtual_host=RABBITMQ_VIRTUAL_HOST)
```

### Receiver
Receiver must have an appropriately defined exchange name: `[SOLUTION_NAME:DIRECTORY_NAME:MESSAGE_NAME]`
```python
from masstransitpython import RabbitMQReceiver
from json import loads

def handler(ch, method, properties, body):
    msg = loads(body.decode())
    print("Received message: %s" % msg["message"])

# define receiver
receiver = RabbitMQReceiver(conf, 'MassTransitService.Messages:SampleMessage')
receiver.add_on_message_callback(handler)
receiver.start_consuming()
```

### Sender
```python
from masstransitpython import RabbitMQSender
from json import loads

def send_message(body):
    '''
    :param body: Message received from MassTransit client
    :return: None
    '''
    with RabbitMQSender(conf) as sender:
        sender.set_exchange('MassTransitService.Messages:SampleMessage')

        encoded_msg = MessageEncoder().encode(SampleMessage("Hello World!"))
        response = sender.create_masstransit_response(loads(encoded_msg), body)
        sender.publish(message=response)
```

### Message
```python
from json import JSONEncoder


class SampleMessage:
    def __init__(self, name):
        self.name = name


class MessageEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
```

## Other
Full example avaliable in https://github.com/byQ96/MassTransitPython/example