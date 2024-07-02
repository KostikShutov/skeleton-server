import json
from executor.celery import app
from executor.tasks import commandTask
from socketio import RedisManager as SocketManager


class CommandCoordinator:
    def __init__(self, socketManager: SocketManager) -> None:
        self.socketManager = socketManager

    def pushCommands(self, payloads: list[object]) -> list[str]:
        tasks: list[str] = []

        for payload in payloads:
            task = self.pushCommand(payload)
            tasks.append(task)

        return tasks

    def pushCommand(self, payload: object) -> str:
        body: str = json.dumps(payload)
        result = commandTask.delay(body=body)

        return result.task_id

    def revokeCommand(self, commandId: str) -> None:
        app.control.revoke(commandId, terminate=True)
        self.socketManager.emit('getCommand', json.dumps({'id': commandId, 'status': 'cancelled'}))

    def getCommandStatus(self, commandId: str) -> str:
        return app.AsyncResult(commandId).state

    def purgeCommands(self) -> None:
        app.control.purge()  # Remove pending tasks
        i = app.control.inspect()
        self.__revokeJobs(i.active())  # Remove active tasks
        self.__revokeJobs(i.reserved())  # Remove reserved tasks

    def __revokeJobs(self, jobs: list) -> None:
        for hostname in jobs:
            tasks = jobs[hostname]

            for task in tasks:
                self.revokeCommand(task['id'])
