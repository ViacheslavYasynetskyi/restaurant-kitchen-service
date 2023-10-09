from django.contrib.auth import get_user_model
from django.test import TestCase

from menu.models import DishType, Dish


class ModelTests(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(
            name="test_name",
        )

        self.assertEqual(str(dish_type),
                         f"{dish_type.name}")

    def test_cook_str(self):
        cook = get_user_model().objects.create_user(
            username="test_username",
            password="test12345",
            first_name="test_first_name",
            last_name="test_last_name"
        )

        self.assertEqual(str(cook), f"{cook.username}")

    def test_dish_str(self):
        name = "test_name"
        price = 20.00
        cook = get_user_model().objects.create_user(
            username="test_username",
            password="test12345",
            first_name="test_first_name",
            last_name="test_last_name"
        )
        dish_type = DishType.objects.create(
            name="test_name",
        )
        dish = Dish.objects.create(
            name=name,
            price=price,
            dish_type=dish_type
        )
        dish.cooks.add(cook,)

        self.assertEqual(str(dish.name), dish.name)

    def test_cook_with_years_of_experience(self):
        username = "test_username"
        password = "test12345"
        years_of_experience = 5

        cook = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience
        )

        self.assertEqual(cook.username, username)
        self.assertTrue(cook.check_password(password))
        self.assertEqual(cook.years_of_experience, years_of_experience)
