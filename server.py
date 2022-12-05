#!/usr/bin/python

import eventlet
import socketio
import json
from dotenv import dotenv_values


def mergeConfigs(firstConfig: dict, secondConfig: dict) -> dict:
    result = firstConfig.copy()
    result.update(secondConfig)
    return result


config: dict = mergeConfigs(dotenv_values('.env'), dotenv_values('.env.local'))
print(config)

if config['CONTROLLER'] == 'car_remote':
    from controllers.car import RemoteController
    controller = RemoteController.RemoteController()
elif config['CONTROLLER'] == 'car_stub':
    from controllers.car import StubController
    controller = StubController.StubController()
else:
    raise Exception('Unknown controller')

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


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


@sio.event
def init(sid: str) -> str:
    return json.dumps(controller.init())


# ============== Movement =============
@sio.event
def forward(sid: str, data) -> None:
    controller.forward(int(data['speed']))


@sio.event
def backward(sid: str, data) -> None:
    controller.backward(int(data['speed']))


@sio.event
def stop(sid: str) -> None:
    controller.stop()


@sio.event
def left(sid: str) -> None:
    controller.left()


@sio.event
def straight(sid: str) -> None:
    controller.straight()


@sio.event
def right(sid: str) -> None:
    controller.right()


@sio.event
def turn(sid: str, data) -> None:
    controller.turn(int(data['angle']))


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
