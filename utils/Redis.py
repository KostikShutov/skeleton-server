import redis
from utils.Config import config

host: str = config['REDIS_HOST']
redis = redis.Redis(host=host)
