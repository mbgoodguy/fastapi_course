import time


class Worker:
    normal_sleep_time = 8 * 60 * 60

    def __init__(self, name: str):
        self.name = name

    def work(self):
        print('Working')
        if self.eat():  # вызов ф-ии которая долго выполняется.
            print('Dinner')
        print('Working')

        return 'Work is Done'


    # ф-ия которая долго выполняется. Ждать придется очень долго! Чтобы этого не делать
    # ее нужно замокать - заменить ф-ию eat на возвращаемое ей значение
    def eat(self):
        time.sleep(30)

        # Это более сложный случай, т.к food - ф-ия, которая при различных аргументах возвращает разные значения.
        res1 = self.food(1)
        res2 = self.food(2)
        res3 = self.food(3)

        return [res1, res2, res3]

    def sleep(self, sleep_time):
        if sleep_time > 10 * 60 * 60:
            self.wake_up()

    def wake_up(self):
        raise Exception('Wake up')
        # pass # тест провалится
        # raise ValueError('Wake up')  # и в этом случае тоже сработает assertRaises т.к наследование от Exception

    def can_repeat(self, sleep_time):
        if sleep_time >= self.normal_sleep_time:
            result = True
        else:
            result = False

        return result

    @staticmethod
    def food(arg):
        food_dict = {
            1: 'apple',
            2: 'bread',
            3: 'cheese',
        }

        return food_dict.get(arg)
