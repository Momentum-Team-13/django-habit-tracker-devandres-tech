from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect("list_habits")
    return render(request, "habits/home.html")


def list_habits(request):
    return render(
        request, "habits/list_habits.html"
    )
