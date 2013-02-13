from django.contrib import admin
from .models import State, GitHubToken

admin.site.register(State)
admin.site.register(GitHubToken)
