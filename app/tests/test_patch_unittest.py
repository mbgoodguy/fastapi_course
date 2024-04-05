import unittest
from unittest.mock import patch, Mock

from app.homeworks import worker


class TestWorker(unittest.TestCase):
    # def test_can_repeat(self):
    #     sleep_time = 7 * 60 * 60
    #     expected_res = False
    #
    #     new_worker = worker.Worker('Bob')
    #
    #     res = new_worker.can_repeat(sleep_time)
    #     self.assertEqual(expected_res, res)

    def test_can_repeat_cases(self):
        test_cases = [
            {
                'args': {'sleep_time': 9 * 60 * 60},
                'expected_res': True
            },
            {
                'args': {'sleep_time': 7 * 60 * 60},
                'expected_res': False
            }

        ]

        new_worker = worker.Worker('Alice')

        for test_case in test_cases:
            result = new_worker.can_repeat(**test_case['args'])
            self.assertEqual(test_case['expected_res'], result)

    def test_sleep_more_10h(self):
        new_worker = worker.Worker('Ivan')
        sleep_time = 11 * 60 * 60

        # чтобы протестить вызывалось ли исключение внутри ф-ии, используем with assert.Raises(Exception)
        with self.assertRaises(Exception):
            _ = new_worker.sleep(sleep_time)

    # def test_work(self):
    #     new_worker = worker.Worker('Ivan')
    #     res = new_worker.work()  # здесь придется ждать выполнения ф-ии eat() :(
    #
    #     self.assertEqual('Work is Done', res)

    @patch.object(worker.Worker, 'eat')  # указываем что будем мокать метод eat из класса Worker модуля worker
    def test_work_1(self, mock_eat):  # чтобы замокать метод eat пробрасываем mock_eat как аргумент

        # указываем значение, которое будет подставлено вместо вызова self.eat
        mock_eat.return_value = True  # так мы замокали ф-ию eat()
        new_worker = worker.Worker('Ivan')
        res = new_worker.work()

        self.assertEqual('Work is Done', res)
        mock_eat.assert_called()  # говорим что вызов mock_eat вообще ожидался. Тест пройдет
        # mock_eat.assert_not_called()  # говорим что вызов mock_eat не ожидался. Тест упадет, т.к mock_eat вызывается

    @staticmethod
    def food_se(args):
        food_dict = {
            1: 'apple',
            2: 'bread',
            3: 'cheese',
        }

        return [food_dict.get(args)]

    @patch('time.sleep')  # мокаем ф-ию time.sleep. Уже без object
    def test_eat(self, _):  # _ здесь т.к мы не испольузем возвращаемое значение ф-ии mock_time_sleep
        new_worker = worker.Worker('MB')

        # как помденяем ф-ию food():
        res = new_worker.eat()
        new_worker.food = Mock(side_effect=self.food_se)  # говорим что хотим заменить ф-ию food на food_se

        self.assertEqual(['apple', 'bread', 'cheese'], res)
