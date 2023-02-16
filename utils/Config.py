from dotenv import dotenv_values


def mergeConfigs(firstConfig: dict, secondConfig: dict) -> dict:
    result = firstConfig.copy()
    result.update(secondConfig)
    return result


config: dict = mergeConfigs(
    dotenv_values('.env'),
    dotenv_values('.env.local'),
)
