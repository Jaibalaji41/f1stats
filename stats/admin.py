from django.contrib import admin
from django.utils.html import format_html
from .models import Team, Driver, SeasonStats, RaceResult, RacePosition

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', 'name', 'country', 'team_principal', 'championships')
    search_fields = ('name', 'country', 'team_principal')
    list_filter = ('country',)
    ordering = ('-championships', 'name')

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="auto" />', obj.logo.url)
        return "No Logo"
    logo_preview.short_description = 'Logo'

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'team', 'nationality', 'number', 'championships', 'wins', 'career_points')
    search_fields = ('name', 'nationality')
    list_filter = ('team', 'nationality')
    ordering = ('-career_points', '-championships', 'name')

    def image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" height="auto" style="border-radius: 50%;" />', obj.photo.url)
        return "No Image"
    image_preview.short_description = 'Photo'

@admin.register(SeasonStats)
class SeasonStatsAdmin(admin.ModelAdmin):
    list_display = ('year', 'driver', 'team', 'championship_position', 'points', 'wins')
    search_fields = ('driver__name', 'team__name')
    list_filter = ('year', 'team')
    ordering = ('-year', 'championship_position')

@admin.register(RaceResult)
class RaceResultAdmin(admin.ModelAdmin):
    list_display = ('race_name', 'circuit', 'country', 'race_date')
    search_fields = ('race_name', 'circuit', 'country')
    list_filter = ('country', 'race_date')
    ordering = ('-race_date',)

@admin.register(RacePosition)
class RacePositionAdmin(admin.ModelAdmin):
    list_display = ('race', 'position', 'driver', 'team', 'points', 'race_time')
    search_fields = ('driver__name', 'team__name', 'race__race_name')
    list_filter = ('position',)
    ordering = ('-race__race_date', 'position')
