from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from .models import Expense
from .forms import ExpenseForm, RegistrationForm

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been successfully logged out.")
        return redirect('login')

class UserAccessMixin(LoginRequiredMixin):
    """Custom mixin to ensure users can only access their own data"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class ExpenseListView(UserAccessMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    
    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by date range
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__range=[start_date, end_date])
            except ValueError:
                pass
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate total for current month - FIXED VERSION
        today = timezone.now().date()
        first_day = today.replace(day=1)
        
        # Get all expenses for the current user in the current month
        monthly_expenses = Expense.objects.filter(
            user=self.request.user,
            date__year=today.year,
            date__month=today.month
        )
        
        # Calculate the sum
        monthly_total = monthly_expenses.aggregate(total=Sum('amount'))['total']
        
        # If no expenses, set to 0
        if monthly_total is None:
            monthly_total = 0
        
        context['monthly_total'] = monthly_total
        context['categories'] = Expense.CATEGORY_CHOICES
        return context

class ExpenseCreateView(UserAccessMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Expense added successfully!')
        return super().form_valid(form)

class ExpenseUpdateView(UserAccessMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense-list')
    
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Expense updated successfully!')
        return super().form_valid(form)

class ExpenseDeleteView(UserAccessMixin, DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expense-list')
    
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Expense deleted successfully!')
        return super().delete(request, *args, **kwargs)

class RegisterView(View):
    template_name = 'expenses/registration/register.html'
    
    def get(self, request):
        # If user is already authenticated, redirect to expenses page
        if request.user.is_authenticated:
            return redirect('expense-list')
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        # If user is already authenticated, redirect to expenses page
        if request.user.is_authenticated:
            return redirect('expense-list')
            
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, self.template_name, {'form': form})
            
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
        
        return render(request, self.template_name, {'form': form})