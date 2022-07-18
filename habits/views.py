import datetime
from django.shortcuts import render, redirect 
from habits.models import Habit, Record
from .forms import HabitForm, RecordForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect("list_habits")
    return render(request, "habits/home.html")


@login_required
def list_habits(request):
    habits = Habit.objects.filter(user=request.user.pk)
    date = {
        'year': datetime.date.today().year,
        'month': datetime.date.today().month,
        'day': datetime.date.today().day
    }
    return render(
        request, "habits/list_habits.html", 
            {"user": request.user, "habits": habits, 'date':  date}
        )


@login_required
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


@login_required
def create_update_record(request, pk, year, month, day):
    user_habit = Habit.objects.filter(user=request.user.pk).get(pk=pk)
    record_date = datetime.date(year, month, day)

    if request.method == "POST":
        target = request.POST.get('daily_number')
        record, _ = Record.objects.get_or_create(date=record_date, habit=user_habit)
        record.daily_number = target
        record.save()
        return redirect("details_habit", pk=user_habit.pk)
    else:
        records = Record.objects.filter(date=record_date, habit=user_habit)
        if records.exists():
            form = RecordForm(instance=records[0])
        else:
            form = RecordForm()

    return render(
        request, "habits/create_update_record.html",
         {"form": form, "habit": user_habit}
    )


@login_required
def details_habit(request, pk):
    user_habit = Habit.objects.filter(user=request.user.pk).get(pk=pk)
    user_records = Record.objects.filter(habit=user_habit).order_by('-date')
    record_form = RecordForm()
    date = {
        'year': datetime.date.today().year,
        'month': datetime.date.today().month,
        'day': datetime.date.today().day
    }
    return render(request, "habits/details_habit.html", {
        "habit": user_habit,
        "date": date,
        "user_records": user_records,
        "form": record_form
    })


@login_required
def delete_record(request, pk, year, month, day):
    user_habit = Habit.objects.filter(user=request.user.pk).get(pk=pk)
    record_date = datetime.date(year, month, day) 
    record = Record.objects.get(date=record_date, habit=user_habit.pk)

    if request.method == "POST":
        record.delete()
        return redirect('details_habit', pk=pk)

    return render(request, "habits/delete_record.html", 
        {"record": record, "habit": user_habit})
