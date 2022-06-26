from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    # def __init__(self, training_type, duration: float, distance: float, speed: float, calories: float):
    #     training_type = self.training_type
    #     duration = self.duration
    #     distance = self.distance
    #     speed = self.speed
    #     calories = self.calories

    def get_message(self) -> str:
        return(
            f'Тип тренировки: {self.training_type}; Длительность: {self.duration} ч.; Дистанция: {self.distance} км;')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)

    def get_spent_calories(self):
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2) * self.weight / self.M_IN_KM * self.duration


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        return (coeff_calorie_1 * self.weight + (self.get_mean_speed()**2 // self.height) * coeff_calorie_2 * self.weight) * self.duration


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self):
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(*data)
    elif workout_type == 'RUN':
        return Running(*data)
    else:
        return SportsWalking(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
