from dataclasses import asdict, dataclass
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {training_type};'
               ' Длительность: {duration:.3f} ч.;'
               ' Дистанция: {distance:.3f} км;'
               ' Ср. скорость: {speed:.3f} км/ч;'
               ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # метра
    M_IN_KM: int = 1000  # метров
    M_IN_H: int = 60  # минут

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
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        info = InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight / self.M_IN_KM
                           * (self.duration * self.M_IN_H))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029
    KMH_IN_MS: int = 0.278
    M_IN_SM: int = 100  # см

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:

        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                            * self.weight
                            + ((self.get_mean_speed() * self.KMH_IN_MS)**2
                               / (self.height / self.M_IN_SM))
                            * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
                           * (self.duration * self.M_IN_H))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # метров
    SPEED_OFFSET: float = 1.1
    MOLTIPLIER_TWO: int = 2

    def __init__(self, action: int,
                 duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed: float = (self.length_pool
                             * self.count_pool
                             / self.M_IN_KM
                             / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        calories: float = (self.get_mean_speed() + self.SPEED_OFFSET) * \
            self.MOLTIPLIER_TWO * self.weight * self.duration
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    if workout_type not in training_dict:
        raise ValueError('Ошибка типа тренировки!', *training_dict.keys())
    new_training: Training = training_dict[workout_type](*data)
    return new_training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
