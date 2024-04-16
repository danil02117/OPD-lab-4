import unittest
from calc import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    # Тестирование, что главная страница загружается
    def test_index_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!doctype html>', response.data)

    # Тестирование вычисления сложного процента
    def test_calculation(self):
        response = self.client.post('/', data={
            'principal': '1000',
            'rate': '5',
            'time': '10',
            'times_per_year': '12'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'result', response.data)
    # Тестирование ввода отрицательных чисел
    def test_negative_values(self):
        response = self.client.post('/', data={
            'principal': '-1000',
            'rate': '-5',
            'time': '-10',
            'times_per_year': '-12'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'error_message', response.data)  
    # Тестирование ввода некорректных данных (например, текст вместо чисел)
    def test_invalid_input(self):
        response = self.client.post('/', data={
            'principal': 'one thousand',
            'rate': 'five',
            'time': 'ten',
            'times_per_year': 'twelve'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'error_message', response.data)



