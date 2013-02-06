from django.contrib import admin
from polls.models import Poll
from polls.models import Choice


class PollAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question']


admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
