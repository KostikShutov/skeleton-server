#!/usr/bin/python

import json
import eventlet
import socketio
from controllers.ControllerResolver import ControllerResolver
from commands.CommandService import CommandService
from utils.Config import config

eventlet.monkey_patch()
mgr = socketio.RedisManager('redis://%s:%s' % (config['REDIS_HOST'], config['REDIS_PORT']))
sio = socketio.Server(cors_allowed_origins='*', client_manager=mgr)
app = socketio.WSGIApp(sio)
configToken: str = config['TOKEN']
controller = ControllerResolver().resolve()
commandService = CommandService(socketManager=mgr)


@sio.event
def connect(sid: str, environ: str, auth: dict) -> None:
    requestToken: str = auth['token']

    if requestToken != configToken:
        raise ConnectionRefusedError('Authentication failed')

    sio.save_session(sid, {'token': requestToken})
    print('Connect (%s)' % sid)


@sio.event
def disconnect(sid: str) -> None:
    print('Disconnect (%s)' % sid)


@sio.event
def state(sid: str) -> str:
    return json.dumps(controller.state())


@sio.event
def pushCommands(sid: str, payloads: list) -> str:
    return json.dumps(commandService.pushCommands(payloads))


@sio.event
def pushCommand(sid: str, payload: object) -> str:
    return str(commandService.pushCommand(payload))


@sio.event
def revokeCommand(sid: str, commandId: str) -> None:
    commandService.revokeCommand(commandId)


@sio.event
def statusCommand(sid: str, commandId: str) -> str:
    return commandService.getCommandStatus(commandId)


@sio.event
def purgeCommands(sid: str) -> None:
    commandService.purgeCommands()


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
