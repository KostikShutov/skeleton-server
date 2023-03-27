import redis
from utils.Config import config

host: str = config['REDIS_HOST']
port: int = config['REDIS_PORT']
redis = redis.Redis(host=host, port=port)
