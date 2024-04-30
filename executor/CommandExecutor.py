import logging
from skeleton_xml.ConfigService import ConfigService
from utils.Env import env


class CommandExecutor:
    def __init__(self) -> None:
        self.configService: ConfigService = ConfigService(config=env['CONFIG'])

    def execute(self, payload: dict) -> None:
        logging.info('Received command: %s' % payload)
        commandName: str = payload.pop('name')
        self.configService.execute(commandName=commandName, request=payload)
