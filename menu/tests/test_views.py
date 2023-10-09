from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from menu.models import DishType, Dish

DISH_TYPE_URL = reverse("menu:dish-type-list")
DISH_URL = reverse("menu:dishes-list")


class PublicDishTypeTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DISH_TYPE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDishTypeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="driver1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_type_list(self):
        DishType.objects.create(name="test_name1")
        DishType.objects.create(name="test_name2")

        response = self.client.get(DISH_TYPE_URL)

        dish_types = DishType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_types)
        )
        self.assertTemplateUsed(response, "menu/dish_type_list.html")

    def test_dish_type_list_search(self):
        DishType.objects.create(
            name="test_name",
        )
        DishType.objects.create(
            name="first dish",
        )
        response = self.client.get(DISH_TYPE_URL, {"name": "test_name"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(DishType.objects.filter(name="test_name"))
        )


class PublicDishTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DISH_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDishTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="driver1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_type_list(self):
        dish_type = DishType.objects.create(
            name="test_name",
        )
        dish1 = Dish.objects.create(
            name="test_name_1",
            price=20.00,
            dish_type=dish_type
        )
        dish2 = Dish.objects.create(
            name="test_name_2",
            price=25.00,
            dish_type=dish_type
        )
        dish1.cooks.add(self.user)
        dish2.cooks.add(self.user)

        response = self.client.get(DISH_URL)

        dishes = Dish.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_list"]),
            list(dishes)
        )
        self.assertTemplateUsed(response, "menu/dish_list.html")

    def test_dish_list_search(self):
        dish_type = DishType.objects.create(
            name="test_name",
        )
        dish_type2 = DishType.objects.create(
            name="second dish",
        )
        Dish.objects.create(name="test_name", price=20.00, dish_type=dish_type)
        Dish.objects.create(name="new", price=25.00, dish_type=dish_type2)
        response = self.client.get(DISH_URL, {"name": "test_name"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_list"]),
            list(Dish.objects.filter(name="test_name"))
        )


class PrivateCookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="cook",
            password="cook1234",
        )
        self.client.force_login(self.user)

    def test_create_cook(self):
        form_data = {
            "username": "test_username",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "years_of_experience": 5,
        }
        self.client.post(reverse("menu:cooks-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.years_of_experience, form_data["years_of_experience"])
