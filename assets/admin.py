from django.contrib import admin

from . import models
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Register your models here.

class Check_TimeView(admin.ModelAdmin):
    list_display = ('check_time',)
    list_editable = ('check_time',)
class AssetInfo_TimeView(admin.ModelAdmin):
    list_display = ('asset_id','sn','mac_addr','buy_time','create_time','up_time')
    list_editable = ('buy_time','create_time','up_time')

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('username','email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.UserProfile
        fields = ('username', 'password', 'email', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','email',  'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email','office_place','store_place')}),
        ('Permissions', {'fields': ('is_admin','groups','user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email',  'password1', 'password2')}
        ),
    )
    search_fields = ('username',)
    ordering = ('email',)
    filter_horizontal = ('groups','user_permissions')

# Now register the new UserAdmin...
admin.site.register(models.UserProfile, UserProfileAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.



# admin.site.register(TimeView)
admin.site.register(models.Level)
admin.site.register(models.AssetInfo,AssetInfo_TimeView)
admin.site.register(models.AssetModel)
admin.site.register(models.AssetName)
admin.site.register(models.AssetProvider)
admin.site.register(models.AssetAttr)
admin.site.register(models.DeviceModel)
admin.site.register(models.InOutReasons)
admin.site.register(models.OfficePlace)
admin.site.register(models.ProductConf)
admin.site.register(models.StorePlace)
admin.site.register(models.AssetStatus)
admin.site.register(models.Supplier)
admin.site.register(models.InStock)
admin.site.register(models.NonStock)
admin.site.register(models.UseType)
admin.site.register(models.InReasons)
admin.site.register(models.OutReasons)
admin.site.register(models.CheckInfo,Check_TimeView)
admin.site.register(models.OperationLogs)
