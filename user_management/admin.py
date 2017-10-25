from user_management.models import CustomUser,UserProfile,UserAddress
from user_management.forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        #(_('Personal info'), {'fields': ('first_name', 'last_name', 'address1', 'address2','area_code','country_code')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    list_display = ('email', 'is_staff','is_superuser')

    search_fields = ('email',)
    ordering = ('email',)


class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('email','first_name','last_name','gender','date_of_birth','activation_key','key_expires')}),
        ]
    
    list_display = ('email', 'first_name','last_name')
    search_fields = ('first_name',)
    ordering = ('first_name','last_name','email',)

class UserAddressAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ('email','address_contact','address_line1','address_line2','land_mark','city','state','pin_code','mobile_no','is_primary',)}),
        ]
    
    list_display = ('email','address_contact','address_line1','address_line2','land_mark','city','state','pin_code','mobile_no','is_primary',)
    search_fields = ('email',)
    ordering = ('address_contact',)
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(UserAddress,UserAddressAdmin)