from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'accounts/register.html')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    from analysis.models import SoilReport
    import json
    
    # Fetch last 10 reports
    reports = SoilReport.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    # Prepare data for charts (reverse to show oldest to newest)
    chart_reports = reversed(reports)
    dates = []
    n_levels = []
    p_levels = []
    k_levels = []
    
    for report in chart_reports:
        dates.append(report.created_at.strftime('%Y-%m-%d'))
        n_levels.append(report.nitrogen)
        p_levels.append(report.phosphorus)
        k_levels.append(report.potassium)
        
    context = {
        'reports': reports, # For the table/list
        'dates': dates,
        'n_levels': n_levels,
        'p_levels': p_levels,
        'k_levels': k_levels,
    }
    
    return render(request, 'analysis/dashboard.html', context)
