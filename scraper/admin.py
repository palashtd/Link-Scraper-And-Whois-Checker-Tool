from django.contrib import admin
from .models import Link, WhosBanner, ScraperBanner

# Register your models here.


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']


@admin.register(ScraperBanner)
class ScraperBannerAdmin(admin.ModelAdmin):
    list_display = ['image']


@admin.register(WhosBanner)
class WhosBannerAdmin(admin.ModelAdmin):
    list_display = ['image']
