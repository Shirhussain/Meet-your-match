from django.contrib import admin
from .models import Match, JobMatch, MatchList

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'percent']
    class Meta:
        model = Match


@admin.register(JobMatch)
class JobMatchAdmin(admin.ModelAdmin):
    list_display = ['user', 'job']
    
    class Meta:
        model = JobMatch


@admin.register(MatchList)
class MatchListAdmin(admin.ModelAdmin):
    class Meta:
        model = MatchList
