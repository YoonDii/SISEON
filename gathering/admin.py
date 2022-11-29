from django.contrib import admin
from .models import Gathering, GatheringComment, Vote, VoteContent
# Register your models here.



class CommentInline(admin.StackedInline):
    model = GatheringComment

class GatheringAdmin(admin.ModelAdmin):
    inlines = (
        CommentInline,
    )

admin.site.register(Gathering, GatheringAdmin)
