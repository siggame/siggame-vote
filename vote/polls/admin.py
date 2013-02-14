from django.contrib import admin
from .models import Vote, Ballot


class InlineBallot(admin.TabularInline):
    model = Ballot


class VoteAdmin(admin.ModelAdmin):
    inlines = (InlineBallot, )
    filter_horizontal = ('already_voted',)


admin.site.register(Vote, VoteAdmin)
admin.site.register(Ballot)
