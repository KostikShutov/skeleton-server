#!/usr/bin/python

import eventlet
import socketio
import json
from dotenv import dotenv_values


def mergeConfigs(firstConfig, secondConfig):
    result = firstConfig.copy()
    result.update(secondConfig)
    return result


config = mergeConfigs(dotenv_values('.env'), dotenv_values('.env.local'))
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
def connect(sid, environ, auth):
    token = auth['token']

    if token != 'secret':
        raise ConnectionRefusedError('Authentication failed')

    sio.save_session(sid, {'token': token})
    print('Connect (%s)' % sid)


@sio.event
def disconnect(sid):
    controller.stop()
    print('Disconnect (%s)' % sid)


@sio.event
def health(sid):
    print('Health (%s)' % sid)


@sio.event
def init(sid):
    return json.dumps(controller.init())


# ============== Movement =============
@sio.event
def forward(sid, data):
    controller.forward(int(data['speed']))


@sio.event
def backward(sid, data):
    controller.backward(int(data['speed']))


@sio.event
def stop(sid):
    controller.stop()


@sio.event
def left(sid):
    controller.left()


@sio.event
def straight(sid):
    controller.straight()


@sio.event
def right(sid):
    controller.right()


@sio.event
def turn(sid, data):
    controller.turn(int(data['angle']))


@sio.event
def angle(sid):
    return controller.angle()


# ================ Camera =================
@sio.event
def cameraLeft(sid):
    controller.cameraLeft()


@sio.event
def cameraRight(sid):
    controller.cameraRight()


@sio.event
def cameraUp(sid):
    controller.cameraUp()


@sio.event
def cameraDown(sid):
    controller.cameraDown()


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
