#!/usr/bin/python

import eventlet
import socketio
import json
from controllers.ControllerResolver import ControllerResolver
from commands.CommandService import CommandService

controller = ControllerResolver().resolve()
commandService = CommandService()
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid: str, environ: str, auth: dict) -> None:
    token: str = auth['token']

    if token != 'secret':
        raise ConnectionRefusedError('Authentication failed')

    sio.save_session(sid, {'token': token})
    print('Connect (%s)' % sid)


@sio.event
def disconnect(sid: str) -> None:
    print('Disconnect (%s)' % sid)


@sio.event
def health(sid: str) -> None:
    print('Health (%s)' % sid)


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
