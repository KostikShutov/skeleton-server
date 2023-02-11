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
python commander.py
```

Запустить камеру:
```bash
cd mjpg-streamer
bash start.sh
```

---

## Todo list

- [ ] Очередь сообщений
  - [x] Настроить RabbitMQ
  - [x] Написать endpoint для отправки сообщений
  - [x] Написать consumer для обработки сообщений
  - [ ] Перевести frontend на новый endpoint
- [ ] Автономность
  - [ ] Сверстать блок для рисования траектории движения
  - [ ] Реализовать генерацию команд на основе заданной траектории движения
- [ ] Геопозиция
  - [ ] Подключить GPS, настроить получение координат
  - [ ] Подключить Yandex/Google Maps, отображать метку на основе полученных координат
