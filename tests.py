# tests.py
import unittest
from datetime import datetime
import tempfile
import os
import json

from models import BaseProduct, Clothing, Furniture
from validation import ValidationError
from utils import parse_json, set_write_off_date

class TestBaseProductEquality(unittest.TestCase):
    def test_base_product_equality(self):
        """
        Создаем два объекта BaseProduct с одинаковыми данными и
        сравниваем их с помощью assertEqual, используя перегруженный __eq__.
        """
        data = {
            "name": "Product A",
            "date_of_receipt": "10.04.2025",
            "count": 5
        }
        product1 = BaseProduct(data)
        product2 = BaseProduct(data)
        self.assertEqual(product1, product2)

    def test_base_product_inequality(self):
        """
        Создаем два объекта с различными данными и убеждаемся, что они не равны.
        """
        data1 = {
            "name": "Product A",
            "date_of_receipt": "10.04.2025",
            "count": 5
        }
        data2 = {
            "name": "Product B",  # отличающееся имя
            "date_of_receipt": "10.04.2025",
            "count": 5
        }
        product1 = BaseProduct(data1)
        product2 = BaseProduct(data2)
        self.assertNotEqual(product1, product2)

class TestClothingEquality(unittest.TestCase):
    def test_clothing_equality(self):
        """
        Создаем два объекта Clothing с одинаковыми данными и сравниваем их.
        """
        data = {
            "name": "Shirt",
            "date_of_receipt": "10.04.2025",
            "count": 10,
            "size": "M",
            "color": "Red",
            "material": "Cotton"
        }
        product1 = Clothing(data)
        product2 = Clothing(data)
        self.assertEqual(product1, product2)

    def test_clothing_inequality(self):
        """
        Создаем два объекта Clothing, различающиеся хотя бы одним параметром (размер),
        и проверяем, что они не равны.
        """
        data1 = {
            "name": "Shirt",
            "date_of_receipt": "10.04.2025",
            "count": 10,
            "size": "M",
            "color": "Red",
            "material": "Cotton"
        }
        data2 = {
            "name": "Shirt",
            "date_of_receipt": "10.04.2025",
            "count": 10,
            "size": "L",
            "color": "Red",
            "material": "Cotton"
        }
        product1 = Clothing(data1)
        product2 = Clothing(data2)
        self.assertNotEqual(product1, product2)

class TestFurnitureEquality(unittest.TestCase):
    def test_furniture_equality(self):
        """
        Создаем два объекта Furniture с идентичными данными и проверяем их равенство.
        """
        data = {
            "name": "Table",
            "date_of_receipt": "10.04.2025",
            "count": 3,
            "material": "Wood",
            "dimensions": "100x50x30",
            "weight": 20
        }
        product1 = Furniture(data)
        product2 = Furniture(data)
        self.assertEqual(product1, product2)

    def test_furniture_inequality(self):
        """
        Создаем два объекта Furniture, где один параметр (material) различается, и
        убеждаемся, что объекты не равны.
        """
        data1 = {
            "name": "Table",
            "date_of_receipt": "10.04.2025",
            "count": 3,
            "material": "Wood",
            "dimensions": "100x50x30",
            "weight": 20
        }
        data2 = {
            "name": "Table",
            "date_of_receipt": "10.04.2025",
            "count": 3,
            "material": "Metal",
            "dimensions": "100x50x30",
            "weight": 20
        }
        product1 = Furniture(data1)
        product2 = Furniture(data2)
        self.assertNotEqual(product1, product2)

class TestUtilsFunctions(unittest.TestCase):
    def test_set_write_off_date_and_equality(self):
        """
        Проверяем функцию set_write_off_date, устанавливая дату списания, и сравниваем
        объект с эталонным, который создается с уже заданной датой списания.
        """
        data = {"name": "Product A", "date_of_receipt": "10.04.2025", "count": 5}
        product = BaseProduct(data)
        set_write_off_date(product, "15.04.2025")
        expected_data = {
            "name": "Product A",
            "date_of_receipt": "10.04.2025",
            "date_of_write_off": "15.04.2025",
            "count": 5
        }
        expected_product = BaseProduct(expected_data)
        self.assertEqual(product, expected_product)

    def test_parse_json_equality(self):
        """
        Тест функции parse_json:
        - Создаем временный JSON-файл с тремя продуктами.
        - Функция должна вернуть список объектов, который мы сравниваем с эталонными объектами.
        """
        test_data = {
            "Prod1": {
                "name": "Product A",
                "date_of_receipt": "10.04.2025",
                "count": 5
            },
            "Prod2": {
                "name": "Shirt",
                "date_of_receipt": "10.04.2025",
                "count": 10,
                "size": "M",
                "color": "Red",
                "material": "Cotton"
            },
            "Prod3": {
                "name": "Table",
                "date_of_receipt": "10.04.2025",
                "count": 3,
                "material": "Wood",
                "dimensions": "100x50x30",
                "weight": 20
            }
        }
        tmp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.json')
        json.dump(test_data, tmp_file, indent=2)
        tmp_file.close()

        try:
            products = parse_json(tmp_file.name)
            self.assertEqual(len(products), 3)

            expected_product1 = BaseProduct(test_data["Prod1"])
            expected_product2 = Clothing(test_data["Prod2"])
            expected_product3 = Furniture(test_data["Prod3"])

            self.assertEqual(products[0], expected_product1)
            self.assertEqual(products[1], expected_product2)
            self.assertEqual(products[2], expected_product3)
        finally:
            os.unlink(tmp_file.name)

if __name__ == '__main__':
    unittest.main()
