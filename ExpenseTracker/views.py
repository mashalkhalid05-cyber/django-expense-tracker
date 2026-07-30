from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Category , Expense , Budget
from django.db.models import Sum , Q , Count
from datetime import date

# Create your views here.


#  DashBoard 
@login_required
def dashboard(request):
    # Total Categories
    total_categories=Category.objects.filter(user=request.user).count()

    #Total Expenses
    total_expenses=Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0

    # Today Expenses
    today = date.today()

    today_expenses = Expense.objects.filter(
        user=request.user,
        date=today
        ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Monthly Expenses
    monthly_expenses = Expense.objects.filter(
    user=request.user,
    date__month=today.month,
    date__year=today.year).aggregate( Sum('amount'))['amount__sum'] or 0

    # Recent Expenses
    recent_expenses=Expense.objects.filter(user=request.user).order_by('-date')[:5]


    return render(request, 'ET/dashboard.html',
    {
        'total_categories':total_categories,
        'total_expenses':total_expenses,
        'today_expenses':today_expenses,
        'monthly_expenses':monthly_expenses,
        'recent_expenses':recent_expenses

    })

# Login Page 
def login_page(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        return render(request,'ET/loginpage.html',{'error':'Invalid Credentials'})
    return render(request,'ET/loginpage.html')


# Logout Page
def logout_page(request):
    logout(request)
    return redirect('loginpage')


# Registeration Page
def register_page(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request,'ET/registerpage.html',{'error':'Username already exists'})
        user=User.objects.create_user(username=username,password=password)
        login(request,user)
        return redirect('dashboard')
    
    return render(request,'ET/registerpage.html')


# Category Views Started

    # View Category
@login_required
def view_category(request):
    categories=Category.objects.filter(user=request.user)
    return render(request,'ET/category_list.html',{'categories':categories})

       
    # Create Category
@login_required
def create_category(request):
    if request.method=="POST":
        category_name=request.POST['name']

        Category.objects.create(
            user=request.user,
            name=category_name
        )
        return redirect('category_list')

    return render(request,'ET/create_category.html')


    # Edit Category
@login_required
def edit_category(request,category_id):
    category=get_object_or_404(Category,id=category_id,user=request.user)

    if request.method=="POST":
        category.name=request.POST['name']
        category.save()
        return redirect('category_list')

    return render(request,'ET/edit_category.html',{'category':category})

    # Delete Category
@login_required
def delete_category(request,category_id):
        category=get_object_or_404(Category,id=category_id,user=request.user)

        if request.method=="POST":
            category.delete()
            return redirect ('category_list')

        return render(request,'ET/delete_category.html',{
            'category':category
        })


# Expense Views Started
@login_required
def create_expense(request):

    categories = Category.objects.filter(user=request.user)

    if request.method=="POST":
        category = request.POST['category']
        amount = request.POST['amount']
        date = request.POST['date']
        description = request.POST['description']

        selected_category = get_object_or_404(
        Category,
        id=category,
        user=request.user
        )

            
        Expense.objects.create(
        user=request.user,
        category=selected_category,
        amount=amount,
        date=date,
        description=description
        )
        
        return redirect('view_expense')

    return render(request,'ET/create_expense.html', {
        'categories': categories
    })


@login_required
def view_expense(request):
    search=request.GET.get('search')

    selected_category = request.GET.get('category')

    from_date = request.GET.get('from_date')

    to_date = request.GET.get('to_date')

    expenses=Expense.objects.filter(user=request.user)

    categories = Category.objects.filter(user=request.user)


    if selected_category:
        expenses = expenses.filter(
        category_id=selected_category)

    if search:
        expenses=expenses.filter(
            Q(description__icontains=search)|
            Q(category__name__icontains=search)
        )

    # Date Range
    if from_date and to_date:
        expenses = expenses.filter(
        date__range=[from_date, to_date]
    )

    return render(request,'ET/view_expense.html',{'expenses':expenses ,
    'categories': categories
    })


@login_required
def edit_expense(request,expense_id):
    expense=get_object_or_404(Expense,id=expense_id,user=request.user)

    categories = Category.objects.filter(user=request.user)


    if request.method=="POST":
        
        selected_category = get_object_or_404(
        Category,
        id=request.POST['category'],
        user=request.user
        )

        expense.description=request.POST['description']
        expense.category=selected_category
        expense.amount=request.POST['amount']
        expense.date=request.POST['date']


        expense.save()
        return redirect('view_expense')

    return render(request,'ET/edit_expense.html',{'expense':expense,
    'categories':categories})


@login_required
def delete_expense(request,expense_id):
    expense=get_object_or_404(Expense,id=expense_id,user=request.user)
    if request.method=="POST":
        expense.delete()
        return redirect ('view_expense')

    return render(request,'ET/delete_expense.html',{
            'expense':expense
    })


@login_required
def expense_summary(request):
    summary=Expense.objects.filter(
        user=request.user
    ).values(
        'category__name'
    ).annotate(
        total_amount=Sum('amount'),
        total_transactions=Count('id')
    )

    return render(request,'ET/expense_summary.html',{'summary':summary})


# # Budget 
@login_required
def budget_list(request):
    categories = Category.objects.filter(user=request.user)

    budgets = Budget.objects.filter(user=request.user)

    if request.method=="POST":
        category = request.POST['category']
        amount = request.POST['amount']
        month = request.POST['month']
        year = request.POST['year']

        selected_category = get_object_or_404(
        Category,
        id=category,
        user=request.user
        )

            
        Budget.objects.create(
        user=request.user,
        category=selected_category,
        amount=amount,
        month=month,
        year=year
        )
        
        return redirect('budget_list')

    return render(request,'ET/create_budget.html',{
        'categories':categories,
        'budgets':budgets
    })
    

@login_required
def edit_budget(request, budget_id):

    budget = get_object_or_404(
        Budget,
        id=budget_id,
        user=request.user
    )

    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":

        category = request.POST['category']
        amount = request.POST['amount']
        month = request.POST['month']
        year = request.POST['year']

        selected_category = get_object_or_404(
            Category,
            id=category,
            user=request.user
        )

        budget.category = selected_category
        budget.amount = amount
        budget.month = month
        budget.year = year

        budget.save()

        return redirect('budget_list')

    return render(request, 'ET/edit_budget.html', {
        'budget': budget,
        'categories': categories
    })


@login_required
def delete_budget(request, budget_id):

    budget = get_object_or_404(
        Budget,
        id=budget_id,
        user=request.user
    )

    if request.method == "POST":
        budget.delete()
        return redirect('budget_list')

    return render(request, 'ET/delete_budget.html', {
        'budget': budget
    })



