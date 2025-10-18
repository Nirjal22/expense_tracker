from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from expenses import views as expense_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expenses/', include('expenses.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='expenses/registration/login.html'), name='login'),
    path('logout/', expense_views.CustomLogoutView.as_view(), name='logout'),
    path('register/', expense_views.RegisterView.as_view(), name='register'),
    path('', expense_views.ExpenseListView.as_view(), name='home'),
]