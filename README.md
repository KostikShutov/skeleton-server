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

Запустить камеру:
```bash
cd mjpg-streamer
bash start.sh
```

---

## Todo list

- [ ] Автономность
  - [ ] Подключить и настроить OpenCV
  - [ ] Реализовать автономное движение
- [ ] Геопозиция
  - [ ] Подключить GPS, настроить получение координат
  - [ ] Подключить Yandex/Google Maps
