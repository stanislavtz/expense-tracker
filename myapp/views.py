from django.shortcuts import render, redirect
from django.shortcuts import get_list_or_404
from .forms import ExpenseForm
from .models import Expense

# Create your views here.
def index(request):
    form = ExpenseForm()

    if request.method == "POST":
        form = ExpenseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("index")
        
    all_expenses = get_list_or_404(Expense)

    context = {
        "form": form,
        "all_expenses": all_expenses,
    }

    return render(request, "myapp/index.html", context)
