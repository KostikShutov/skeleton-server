import utils.Config as Config
from celery import Celery

config: dict = Config.Config().getConfig()
host: str = config['RABBITMQ_HOST']

app = Celery('commands',
             broker=host,
             backend='rpc://',
             include=['commands.tasks'])

app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
