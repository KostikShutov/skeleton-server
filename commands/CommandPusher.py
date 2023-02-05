import pika
import json
import utils.Config as Config


class CommandPusher:
    def __init__(self) -> None:
        config: dict = Config.Config().getConfig()
        host: str = config['RABBITMQ_HOST']
        self.queue: str = config['RABBITMQ_QUEUE']

        self.channel = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        ).channel()

        self.channel.queue_declare(queue=self.queue)

    def pushCommand(self, payload: object) -> None:
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=json.dumps(payload),
        )
