from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm,  UserCreationForm
from django.contrib.auth.models import Group
from .models import User , OtpCode , Profile
from rest_framework.authtoken.models import Token
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = [ProfileInline]

    list_display = ("phone_number","email","date_joined","is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None , {"fields":("phone_number","email","password")}) , 
        ("Permissions",{"fields":("is_admin",)})
    )

    add_fieldsets = (
        (None , {"fields":("phone_number","email","password","password2"),"classes":("wide")}),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = []




admin.site.register(User,UserAdmin)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)


admin.site.unregister(Group)
admin.site.register(OtpCode)