from django.contrib import admin
from .models import UserInfo, HistoryRecord

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['username', 'age', 'gender', 'weight', 'height']

    def username(self, obj):
        return obj.user.username

# Register your models here.
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(HistoryRecord)