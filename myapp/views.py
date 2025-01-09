import datetime

from django.shortcuts import render, redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Sum

from .forms import ExpenseForm
from .models import Expense


# Create your views here.
def index(request):
    all_expenses = []
    total_expenses = 0
    form = ExpenseForm()

    if request.user.is_authenticated:
        if request.method == "POST":
            form = ExpenseForm(request.POST)

            if form.is_valid():
                print("form is valid")   
                expense = form.save(commit=False)
                expense.user = request.user
                expense.save()
                return redirect("index")
            else:
                print("not valid")
        
        if request.user and request.user.username == "admin":
            all_expenses = Expense.objects.all()
            total_expenses = all_expenses.aggregate(Sum("amount"))
        else:
            all_expenses = Expense.objects.filter(user=request.user)
            total_expenses = all_expenses.aggregate(Sum("amount"))

        # Calculates last 365 days expenses total amount
        last_year = datetime.date.today() - datetime.timedelta(days=365)
        last_year_query= all_expenses.filter(created__gt=last_year)
        yearly_total = last_year_query.aggregate(Sum("amount"))

        # Calculates last 30 days expenses total amount
        last_month = datetime.date.today() - datetime.timedelta(days=30)
        last_month_query = all_expenses.filter(created__gt=last_month)
        monthly_total = last_month_query.aggregate(Sum("amount"))

        # Calculates last 7 days expenses total amount
        last_week = datetime.date.today() - datetime.timedelta(weeks=1)
        last_week_query = all_expenses.filter(created__gt=last_week)
        weekly_total = last_week_query.aggregate(Sum("amount"))

        #Calculates total daily expenses
        daily_expenses = all_expenses.values("created").order_by("created").annotate(sum=Sum("amount"))

        #Calculates total expenses per category
        category_expenses = all_expenses.values("category").order_by("category").annotate(sum=Sum("amount"))

        context = {
            "form": form,
            "all_expenses": all_expenses,
            "total": total_expenses,
            "yearly_total": yearly_total,
            "monthly_total": monthly_total,
            "weekly_total": weekly_total,
            "daily_expenses": daily_expenses,
            "category_expenses": category_expenses
        }

        return render(request, "myapp/index.html", context)
    else:
        return render(request, "myapp/index.html")


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


def delete_expense(request, expense_id):
    current_expense = get_object_or_404(Expense, id=expense_id)
    current_expense.delete()
    return redirect("index")
