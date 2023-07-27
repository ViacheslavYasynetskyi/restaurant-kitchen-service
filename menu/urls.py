from django.urls import path

from menu.views import index, DishTypeListView

urlpatterns = [
    path("", index, name="index"),
    path(
        "dish-types",
        DishTypeListView.as_view(),
        name="dish-type-list"
    ),
]

app_name = "menu"
