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

## Запуск

Запустить backend:

```bash
make server
```

Запустить worker:

```bash
make worker
```

## Raspberry

Проверить i2c на raspberry pi:

```bash
python i2c.py
```

Запустить камеру:

```bash
cd mjpg-streamer/mjpg-streamer-experimental
bash start.sh
```
