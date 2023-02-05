#!/usr/bin/python

import pika
import sys
import os
import json
import utils.Config as Config
import commands.BackwardCommand as BackwardCommand
import commands.ForwardCommand as ForwardCommand
import commands.LeftCommand as LeftCommand
import commands.RightCommand as RightCommand


class Commander:
    def __init__(self) -> None:
        config: dict = Config.Config().getConfig()
        host: str = config['RABBITMQ_HOST']
        self.queue: str = config['RABBITMQ_QUEUE']

        self.channel = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        ).channel()

        self.channel.queue_declare(queue=self.queue)

        self.commands = [
            BackwardCommand.BackwardCommand(),
            ForwardCommand.ForwardCommand(),
            LeftCommand.LeftCommand(),
            RightCommand.RightCommand(),
        ]

    def consume(self) -> None:
        def callback(ch, method, properties, body):
            payload = json.loads(body)

            for command in self.commands:
                if command.canExecute(payload):
                    command.execute(payload)

        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=callback,
            auto_ack=True,
        )

        print('[*] Waiting for messages. To exit press CTRL+C')

        self.channel.start_consuming()


if __name__ == '__main__':
    try:
        Commander().consume()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
