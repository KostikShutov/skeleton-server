#!/usr/bin/python

import eventlet
import socketio
import json
import controllers.ControllerInterface as ControllerInterface
import controllers.ControllerResolver as ControllerResolver

controller: ControllerInterface = ControllerResolver.ControllerResolver().resolve()
sio: socketio.Server = socketio.Server(cors_allowed_origins='*')
app: socketio.WSGIApp = socketio.WSGIApp(sio)


# ============== General =============
@sio.event
def connect(sid: str, environ: str, auth: dict) -> None:
    token: str = auth['token']

    if token != 'secret':
        raise ConnectionRefusedError('Authentication failed')

    sio.save_session(sid, {'token': token})
    print('Connect (%s)' % sid)


@sio.event
def disconnect(sid: str) -> None:
    controller.stop()
    print('Disconnect (%s)' % sid)


@sio.event
def health(sid: str) -> None:
    print('Health (%s)' % sid)


# ============== Movement =============
@sio.event
def init(sid: str) -> str:
    return json.dumps(controller.init())


@sio.event
def pushCommand(sid: str, data: object) -> None:
    return controller.pushCommand(data)


@sio.event
def angle(sid: str) -> None:
    return controller.angle()


# ================ Camera =================
@sio.event
def cameraLeft(sid: str) -> None:
    controller.cameraLeft()


@sio.event
def cameraRight(sid: str) -> None:
    controller.cameraRight()


@sio.event
def cameraUp(sid: str) -> None:
    controller.cameraUp()


@sio.event
def cameraDown(sid: str) -> None:
    controller.cameraDown()


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
