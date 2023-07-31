from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from menu.models import Cook, Dish, DishType


def index(request):
    """View function for the home page of the site."""
    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }
    return render(request, "menu/index.html", context=context)


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "menu/dish_type_list.html"
    context_object_name = "dish_type_list"
    paginate_by = 2


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "menu/dish_type_form.html"
    success_url = reverse_lazy("menu:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "menu/dish_type_form.html"
    success_url = reverse_lazy("menu:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "menu/dish_type_confirm_delete.html"
    success_url = reverse_lazy("menu:dish-type-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 2
    queryset = Cook.objects.all()


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("cooks__dish_type")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    fields = ["username", "password", "first_name", "last_name", "email", "years_of_experience"]
    template_name = "menu/cook_form.html"
    success_url = reverse_lazy("menu:cooks-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = ["years_of_experience"]
    template_name = "menu/cook_form.html"
    success_url = reverse_lazy("menu:cooks-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "menu/cook_confirm_delete.html"
    success_url = reverse_lazy("menu:cooks-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 2


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("menu:dishes-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("menu:dishes-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("menu:dishes-list")


@login_required
def toggle_assign_to_dish(request, pk):
    cooker = Cook.objects.get(id=request.user.id)
    if (
        Dish.objects.get(id=pk) in cooker.cooks.all()
    ):  # probably could check if car exists
        cooker.cooks.remove(pk)
    else:
        cooker.cooks.add(pk)
    return HttpResponseRedirect(reverse_lazy("menu:dishes-detail", args=[pk]))
