from django.test import TestCase

from menu.forms import (CookCreationForm,
                        CookSearchForm,
                        DishTypeSearchForm,
                        DishSearchForm)


class CookCreateFormTests(TestCase):
    def test_driver_create_with_year_of_experience_lastname_is_valid(self):
        form_data = {
            "username": "test_username",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "years_of_experience": 5,
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DishSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "name"
        form_data = {field: "test_name"}
        form = DishSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)


class DishTypeSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "name"
        form_data = {field: "test_name"}
        form = DishTypeSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)


class CookSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "name"
        form_data = {field: "test_name"}
        form = CookSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)
