from django.shortcuts import render, redirect
from django.shortcuts import get_list_or_404, get_object_or_404
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


def edit_expense(request, expense_id):
    current_expense = get_object_or_404(Expense, id=expense_id)
    edit_form = ExpenseForm(instance=current_expense)

    if request.method == "POST":
        edit_form = ExpenseForm(request.POST, instance=current_expense)

        if edit_form.is_valid():
            edit_form.save()
            return redirect("index")

    context = {
        "expense": current_expense,
        "form": edit_form,
        "is_edit_form": True,
    }

    return render(request, "myapp/edit_expense.html", context)
