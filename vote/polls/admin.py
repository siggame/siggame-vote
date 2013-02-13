from django.contrib import admin
from .models import Vote, Ballot, UserVoted


admin.site.register(Vote)
admin.site.register(Ballot)
admin.site.register(UserVoted)
