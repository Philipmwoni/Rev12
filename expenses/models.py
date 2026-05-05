
from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    
   

    # The owner of this category
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        help_text='The user who owns this category.'
    )

    name = models.CharField(
        max_length=100,
        help_text='e.g. Food, Transport, Entertainment'
    )

    # Colour is stored as a hex code for use in charts (e.g. '#FF5733')
    color = models.CharField(
        max_length=7,
        default='#6C63FF',
        help_text='Hex colour code for chart display.'
    )

    # Optional icon class name (e.g. 'fa-utensils') for future icon support
    icon = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text='Optional icon class name.'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'
        # Each user's category names must be unique (but two users can share a name)
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.user.username})'

    def expense_count(self):
        
        return self.expenses.count()

    def total_spent(self):
        
        from django.db.models import Sum
        result = self.expenses.aggregate(total=Sum('amount'))
        return result['total'] or 0


class Expense(models.Model):
    

    # The owner — used for all ownership checks
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )

    # Category is required — every expense must be categorised
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,   # Prevent deleting a category that has expenses
        related_name='expenses',
        help_text='Which category does this expense belong to?'
    )

    title = models.CharField(
        max_length=200,
        help_text='Short description, e.g. "Lunch at cafe"'
    )

    # DecimalField is used for money — float would cause rounding errors
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Amount in your default currency.'
    )

    # Date of the expense — not necessarily today
    date = models.DateField(
        default=timezone.now,
        help_text='When did this expense occur?'
    )

    notes = models.TextField(
        blank=True,
        help_text='Optional additional details.'
    )

    # When the record was created/modified in our system
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']  # Newest first

    def __str__(self):
        return f'{self.title} — ${self.amount} on {self.date}'
