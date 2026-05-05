
import json
from datetime import date, timedelta
from collections import defaultdict

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay, TruncMonth
from django.http import JsonResponse

from expenses.models import Expense, Category


@login_required
def home(request):
    
    today = date.today()
    current_month_start = today.replace(day=1)

    user = request.user
    base_qs = Expense.objects.filter(user=user)

    

    
    month_total = base_qs.filter(
        date__gte=current_month_start, date__lte=today
    ).aggregate(total=Sum('amount'))['total'] or 0


    week_start = today - timedelta(days=today.weekday())
    week_total = base_qs.filter(
        date__gte=week_start, date__lte=today
    ).aggregate(total=Sum('amount'))['total'] or 0


    today_total = base_qs.filter(
        date=today
    ).aggregate(total=Sum('amount'))['total'] or 0

    all_time_total = base_qs.aggregate(total=Sum('amount'))['total'] or 0

    recent_expenses = base_qs.select_related('category').order_by('-date', '-created_at')[:5]

    
    category_data = (
        base_qs
        .filter(date__gte=current_month_start, date__lte=today)
        .values('category__name', 'category__color')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    pie_labels = [item['category__name'] for item in category_data]
    pie_data = [float(item['total']) for item in category_data]
    pie_colors = [item['category__color'] for item in category_data]

    
    thirty_days_ago = today - timedelta(days=29)
    daily_data = (
        base_qs
        .filter(date__gte=thirty_days_ago, date__lte=today)
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )

    
    date_totals = {item['date']: float(item['total']) for item in daily_data}
    bar_labels = []
    bar_data = []
    for i in range(30):
        d = thirty_days_ago + timedelta(days=i)
        bar_labels.append(d.strftime('%b %d'))
        bar_data.append(date_totals.get(d, 0))

    
    six_months_ago = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    six_months_ago = six_months_ago - timedelta(days=150)

    monthly_data = (
        base_qs
        .filter(date__gte=six_months_ago)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    monthly_labels = [item['month'].strftime('%b %Y') for item in monthly_data]
    monthly_values = [float(item['total']) for item in monthly_data]

    context = {
        
        'today_total': today_total,
        'week_total': week_total,
        'month_total': month_total,
        'all_time_total': all_time_total,

        
        'recent_expenses': recent_expenses,

        
        'pie_labels': json.dumps(pie_labels),
        'pie_data': json.dumps(pie_data),
        'pie_colors': json.dumps(pie_colors),

        'bar_labels': json.dumps(bar_labels),
        'bar_data': json.dumps(bar_data),

        'monthly_labels': json.dumps(monthly_labels),
        'monthly_values': json.dumps(monthly_values),

    
        'category_data': category_data,

        
        'expense_count': base_qs.count(),
        'category_count': Category.objects.filter(user=user).count(),
    }
    return render(request, 'auth/home.html', context)


@login_required
def chart_data_api(request):
    
    period = request.GET.get('period', 'month')
    today = date.today()

    if period == 'week':
        start_date = today - timedelta(days=6)
    elif period == 'month':
        start_date = today.replace(day=1)
    elif period == 'year':
        start_date = today.replace(month=1, day=1)
    else:
        start_date = None

    expenses = Expense.objects.filter(user=request.user)
    if start_date:
        expenses = expenses.filter(date__gte=start_date, date__lte=today)

    
    cat_data = (
        expenses
        .values('category__name', 'category__color')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    
    daily = (
        expenses
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )

    return JsonResponse({
        'pie': {
            'labels': [d['category__name'] for d in cat_data],
            'data': [float(d['total']) for d in cat_data],
            'colors': [d['category__color'] for d in cat_data],
        },
        'bar': {
            'labels': [str(d['date']) for d in daily],
            'data': [float(d['total']) for d in daily],
        },
        'total': float(expenses.aggregate(total=Sum('amount'))['total'] or 0),
    })
