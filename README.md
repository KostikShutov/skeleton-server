# skeleton-server

## Другие компоненты общей системы

[Webview for server](https://github.com/KostikShutov/skeleton-webview)

[Command generator](https://github.com/KostikShutov/skeleton-generator)

## Docker

Поднять docker контейнеры

 ```bash
make d-up
 ```

Остановить docker контейнеры

```bash
make d-down
```

Перезапустить docker контейнеры

```bash
make d-restart
```

Зайти в контейнер с Python

```bash
make d-python
```

## Raspberry

Установить зависимости на операционную систему:

```bash
bash install-dependencies.sh
```

Проверить i2c на raspberry pi:

```bash
python i2c.py
```

## Запуск

Запустить backend:

```bash
make s-server
```

Запустить commander (consumer):

```bash
make s-commander
```

Запустить камеру:

```bash
cd mjpg-streamer
bash start.sh
```
