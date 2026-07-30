from django.urls import path
from . import views

urlpatterns = [


    path('loginpage/',views.login_page,name='loginpage'),

    path('logout/', views.logout_page, name='logout'),

    path('registerpage/', views.register_page, name='registerpage'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('category_list/', views.view_category, name='category_list'),

    path('create_category/',views.create_category,name='create_category'),

    path('edit_category/<int:category_id>/',views.edit_category,name='edit_category'),

    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),

    path('create_expense/',views.create_expense,name='create_expense'),

    path('view_expense/',views.view_expense,name='view_expense'),

    path('edit_expense/<int:expense_id>/',views.edit_expense,name='edit_expense'),

    path('delete_expense/<int:expense_id>/',views.delete_expense,name='delete_expense'),

    path('expense_summary/',views.expense_summary,name='expense_summary'),

    path('budget_list/', views.budget_list, name='budget_list'),

    path('edit_budget/<int:budget_id>/', views.edit_budget, name='edit_budget'),

    path('delete_budget/<int:budget_id>/', views.delete_budget, name='delete_budget'),

]

