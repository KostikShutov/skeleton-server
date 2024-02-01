import json
import socketio
from celery import current_task
from controllers.ControllerResolver import ControllerResolver
from commands.CommandExecutor import CommandExecutor
from commands.celery import app
from utils.Config import config

sio = socketio.RedisManager('redis://%s:%s' % (config['REDIS_HOST'], config['REDIS_PORT']), write_only=True)
controller = ControllerResolver().resolve()
commandExecutor = CommandExecutor(controller=controller)


@app.task
def commandTask(body: str) -> None:
    payload: dict = json.loads(body)
    commandId: str = current_task.request.id

    try:
        commandExecutor.execute(payload)
        sio.emit('getCommand', data=json.dumps({
            'id': commandId,
            'status': 'success',
            'state': controller.state(),
        }))
    except Exception:
        sio.emit('getCommand', data=json.dumps({
            'id': commandId,
            'status': 'error',
            'state': controller.state(),
        }))
