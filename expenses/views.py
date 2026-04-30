from django.shortcuts import render


def index(request):
    """Simple index view for Expenses app."""
    return render(request, 'expenses/index.html')
