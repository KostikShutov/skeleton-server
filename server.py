#!/usr/bin/python

import eventlet
import socketio
import json
from controllers.ControllerResolver import ControllerResolver
from commands.CommandPusher import CommandPusher

controller = ControllerResolver().resolve()
commandPusher = CommandPusher()
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
def pushCommand(sid: str, data: object) -> None:
    commandPusher.pushCommand(data)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
