from dotenv import dotenv_values


class Config:
    def getConfig(self) -> dict:
        return self.__mergeConfigs(
            dotenv_values('.env'),
            dotenv_values('.env.local'),
        )

    def __mergeConfigs(self, firstConfig: dict, secondConfig: dict) -> dict:
        result = firstConfig.copy()
        result.update(secondConfig)
        return result
