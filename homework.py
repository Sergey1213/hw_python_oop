from typing import Any


class InfoMessage ():
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:  # TODO перевести в часы
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distans_km: float = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distans_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed: float = self.distans_km / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self, distans_km, mean_speed) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distans_km = self.get_distance()
        mean_speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()
        info_message = InfoMessage(
            self.__class__.__name__, self.duration, distans_km, mean_speed, spent_calories)
        # text_message = info_message.get_message()
        return info_message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        self.spent_calories: float = (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.mean_speed
                                      + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM * self.duration
        return self.spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K1: float = 0.035
    K2: float = 0.029
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        self.spent_calories: float = (0.035 * self.weight + (self.mean_speed**2 / self.height)
                                      * self.K2 * self.weight) * self.duration  # TODO проверить скорость дб м/с
        return self.spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    K3: float = 1.1
    K4: float = 2

    def __init__(self, action: int, duration: float, weight: float, length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed: float = self.length_pool * \
            self.count_pool / self.M_IN_KM / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        self.spent_calories: float = (
            self.mean_speed + self.K3) * self.K4 * self.weight * self.duration
        return self.spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(*data)
    elif workout_type == 'RUN':
        return Running(*data)
    elif workout_type == 'WLK':
        return SportsWalking(*data)
    else:
        ...  # TODO предусмотреть нестандартные типы тренировок


def main(training: Training) -> None:
    """Главная функция."""
    training_data_distance = training.get_distance()
    training_data_speed = training.get_mean_speed()
    # training_data_spent_calories = training.get_spent_calories()
    info = training.show_training_info(
        training_data_distance, training_data_speed)
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:

        training = read_package(workout_type, data)
        main(training)
