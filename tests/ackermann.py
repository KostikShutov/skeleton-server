import numpy as np
import math
from commands.CommandPusher import CommandPusher


def is_on_line(points, tolerance=0.1):
    if len(points) < 2:
        return True

    x1, y1 = points[0]
    x2, y2 = points[1]

    # Вычисляем уравнение прямой через первые две точки
    a = y2 - y1
    b = x1 - x2
    c = x2 * y1 - x1 * y2

    # Проверяем, что все остальные точки лежат на этой прямой с заданной погрешностью
    for i in range(2, len(points)):
        x, y = points[i]
        if abs(a * x + b * y + c) > tolerance:
            return False

    return True


def is_convex(x, y):
    # Вычисляем значения функции для каждой координаты в массиве
    f = np.array(y)
    # Находим точку с максимальным значением функции
    max_idx = np.argmax(f)
    # Находим точку с минимальным значением функции
    min_idx = np.argmin(f)
    # Находим точку, находящуюся между двумя соседними точками с наибольшим и наименьшим значением функции
    mid_idx = max_idx if max_idx < min_idx else min_idx
    # Вычисляем значение второй производной функции в этой точке
    d2f = np.gradient(np.gradient(f))
    d2f_mid = d2f[mid_idx]
    # Определяем, является ли функция выпуклой или вогнутой
    return d2f_mid >= 0


def generate_points(x, y):
    points = []

    for i in range(len(x)):
        points.append([x[i], y[i]])

    return points


# Создаем массив координат точек
x = np.linspace(0, 10, num=50)
y = np.sin(x)
# y = np.linspace(1, 1, num=50)
points = generate_points(x, y)

# Конфигурация
length: float = 0.2
# width: float = 0.05
delta: int = 6

# Зависимости
commandPusher = CommandPusher()

for i in range(0, len(points) - delta, delta):
    startIndex = i
    endIndex = i + delta
    x1, y1 = points[startIndex]
    x2, y2 = points[endIndex]
    x0: float = (x1 + x2) / 2
    y0: float = (y1 + y2) / 2
    radius: float = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2)) / 2
    # outerAngle: float = length / (radius + (width / 2))
    # innerAngle: float = length / (radius - (width / 2))
    # angle: float = (outerAngle + innerAngle) / 2
    angle: float = math.degrees(length / radius)

    command: str = 'undefined'
    xPoints = x[startIndex:endIndex + 1]
    yPoints = y[startIndex:endIndex + 1]

    distance: float = 0

    for j in range(startIndex, endIndex, 1):
        dx1, dy1 = points[j]
        dx2, dy2 = points[j + 1]
        distance += math.hypot(dx2 - dx1, dy2 - dy1)

    if is_on_line(points):
        # Forward
        commandPusher.pushCommand(
            {
                'name': 'TURN',
                'angle': 90,
            },
        )
    else:
        if i <= len(y) - delta:
            if is_convex(x[startIndex:endIndex + 1], y[startIndex:endIndex + 1]):
                # Left
                commandPusher.pushCommand(
                    {
                        'name': 'TURN',
                        'angle': 90 - angle,
                    },
                )
            else:
                # Right
                commandPusher.pushCommand(
                    {
                        'name': 'TURN',
                        'angle': 90 + angle,
                    },
                )

    commandPusher.pushCommand(
        {
            'name': 'FORWARD',
            'speed': 60,
            'distance': distance,
            'duration': 3,
        },
    )

    print(angle, distance)
