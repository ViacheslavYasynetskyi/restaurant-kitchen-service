from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from menu.forms import CookCreationForm, DishForm, CookLicenseUpdateForm, DishTypeSearchForm, DishSearchForm, \
    CookSearchForm
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = DishType.objects.all()
        form = DishTypeSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("name", "")
        context["search_form"] = CookSearchForm(
            initial={"name": username}
        )

        return context

    def get_queryset(self):
        queryset = Cook.objects.all()
        form = CookSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["name"]
            )
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__dish_type")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = CookCreationForm
    template_name = "menu/cook_form.html"
    success_url = reverse_lazy("menu:cooks-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookLicenseUpdateForm
    template_name = "menu/cook_form.html"
    success_url = reverse_lazy("menu:cooks-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "menu/cook_confirm_delete.html"
    success_url = reverse_lazy("menu:cooks-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = Dish.objects.all().select_related("dish_type")
        form = DishSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("menu:dishes-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("menu:dishes-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("menu:dishes-list")


# @login_required
# def toggle_assign_to_dish(request, pk):
#     cooker = Cook.objects.get(id=request.user.id)
#     if (
#         Dish.objects.get(id=pk) in cooker.dish.all()
#     ):
#         cooker.dish.remove(pk)
#     else:
#         cooker.dish.add(pk)
#     return HttpResponseRedirect(reverse_lazy("menu:dishes-detail", args=[pk]))


class DishToggleAssignCookUpdateView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    # fields = ["cooks"]
    template_name = "menu/dish_update.html"
    # success_url = reverse_lazy("menu:dishes-detail")

    def post(self, request, *args, **kwargs):
        cooker = Cook.objects.get(id=request.user.id)
        if (
            Dish.objects.get(id=self.kwargs["pk"]) in cooker.dishes.all()
        ):
            cooker.dishes.remove(self.kwargs["pk"])
        else:
            cooker.dishes.add(self.kwargs["pk"])
        return redirect("menu:dishes-detail", pk=self.kwargs["pk"])
