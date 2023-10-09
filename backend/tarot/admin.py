from django.contrib import admin

from tarot.models import User, Subscription, Card, Prediction, Invoice


class SubInline(admin.TabularInline):
    model = Subscription


class PredictionInline(admin.TabularInline):
    model = Prediction


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = [
        'tg_id',
    ]
    list_display = [
        'tg_id',
    ]

    inlines = [SubInline, PredictionInline]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    search_fields = [
        'card',
        'image',
    ]
    list_display = [
        'card',
        'image',
    ]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    search_fields = [
        'user',
        'uuid',
    ]
    list_display = [
        'user',
        'uuid',
    ]
