from django.shortcuts import render, redirect, get_object_or_404
from habits.models import Habit
from .forms import HabitForm


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect("list_habits")
    return render(request, "habits/home.html")


def list_habits(request):
    habits = Habit.objects.filter(user=request.user.pk)
    print(habits)
    return render(
        request, "habits/list_habits.html", {"user": request.user, "habits": habits}
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
