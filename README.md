# skeleton-server

## Развертывание

Поднять docker контейнеры (для локальной разработки):
```bash
docker-compose up -d
```

Установить зависимости на операционную систему:
```bash
bash install-dependencies.sh
```

Проверить i2c на raspberry pi:
```bash
python i2c.py
```

---

## Запуск

Запустить backend:
```bash
python server.py
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
