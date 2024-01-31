import json
import socketio
from celery import current_task
from commands.CommandExecutor import CommandExecutor
from commands.celery import app
from utils.Config import config

sio = socketio.RedisManager('redis://%s:%s' % (config['REDIS_HOST'], config['REDIS_PORT']), write_only=True)
commandExecutor = CommandExecutor()


@app.task
def commandTask(body: str) -> None:
    payload: dict = json.loads(body)
    commandId: str = current_task.request.id

    try:
        commandExecutor.execute(payload)
        sio.emit('getCommand', data=json.dumps({'id': commandId, 'status': 'success'}))
    except Exception:
        sio.emit('getCommand', data=json.dumps({'id': commandId, 'status': 'error'}))
