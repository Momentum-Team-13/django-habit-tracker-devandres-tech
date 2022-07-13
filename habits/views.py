from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from habits.models import Habit
from .forms import HabitForm, RecordForm


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect("list_habits")
    return render(request, "habits/home.html")


def list_habits(request):
    habits = Habit.objects.filter(user=request.user.pk)
    date = {
        'year': datetime.today().year,
        'month': datetime.today().month,
        'day': datetime.today().day
    }
    return render(
        request, "habits/list_habits.html", 
            {"user": request.user, "habits": habits, 'date':  date}
        )


def add_habit(request):
    if request.method == "POST":
        form = HabitForm(data=request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect("list_habits")
    else:
        form = HabitForm()
    
    return render(request, "habits/add_habit.html", {"form": form})


def create_update_record(request, pk, date):
    recipe = get_object_or_404(request.user.recipes, pk=recipe_pk)

    if request.method == "POST":
        form = RecipeStepForm(data=request.POST)

        if form.is_valid():
            recipe_step = form.save(commit=False)
            recipe_step.recipe = recipe
            recipe_step.save()

            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeStepForm()

    return render(
        request, "core/add_recipe_step.html", {"form": form, "recipe": recipe}
    )



