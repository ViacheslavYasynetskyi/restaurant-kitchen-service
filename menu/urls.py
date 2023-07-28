from django.urls import path

from menu.views import (
    index,
    DishTypeListView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    CookListView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,
    CookDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "dish-types/",
        DishTypeListView.as_view(),
        name="dish-type-list",
    ),
    path(
        "dish-types/create/",
        DishTypeCreateView.as_view(),
        name="dish-types-create",
    ),
    path(
        "dish-types/<int:pk>/update/",
        DishTypeUpdateView.as_view(),
        name="dish-types-update",
    ),
    path(
        "dish-types/<int:pk>/delete/",
        DishTypeDeleteView.as_view(),
        name="dish-types-delete",
    ),
    path(
        "cooks/",
        CookListView.as_view(),
        name="cooks-list",
    ),
    path(
        "cooks/<int:pk>/",
        CookDetailView.as_view(),
        name="cooks-detail",
    ),
    path(
        "cooks/create/",
        CookCreateView.as_view(),
        name="cooks-create",
    ),
    path(
        "cooks/<int:pk>/update/",
        CookUpdateView.as_view(),
        name="cooks-update",
    ),
    path(
        "cooks/<int:pk>/delete/",
        CookDeleteView.as_view(),
        name="cooks-delete",
    ),
]

app_name = "menu"
