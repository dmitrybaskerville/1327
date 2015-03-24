from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile


class UserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required fields, plus a repeated password."""
	password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
	password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

	class Meta:
		model = UserProfile
		fields = ('username', 'email', 'first_name', 'last_name')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(_("Passwords don't match"))
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on the user, but replaces the password field with admin's password hash display field."""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = UserProfile
		fields = ('username', 'password', 'email', 'first_name', 'last_name', 'is_active', 'is_admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]


class UserProfileAdmin(UserAdmin):
	# The forms to add and change user instances
	form = UserChangeForm
	add_form = UserCreationForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin', 'is_superuser')
	list_filter = ('is_admin',)
	fieldsets = (
		(None, {'fields': ('username', 'email', 'password')}),
		('Personal info', {'fields': ('first_name','last_name',)}),
		('Permissions', {'fields': ('is_admin','is_superuser', 'groups', 'user_permissions',)}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')}
		),
	)
	search_fields = ('username',)
	ordering = ('username',)

# Now register the new UserAdmin...
admin.site.register(UserProfile, UserProfileAdmin)


class GroupAdminForm(forms.ModelForm):
	"""
		Adapted Group Admin Form that allows to select users belonging to each group and also mimics that standard
		permissions are only default permissions
		based on: https://djangosnippets.org/snippets/2452/

	"""
	users = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all(),
										   widget=FilteredSelectMultiple(_('Users'), False),
										   required=False)

	class Meta:
		exclude = []
		model = Group

	def __init__(self, *args, **kwargs):
		instance = kwargs.get('instance', None)
		if instance is not None:
			initial = kwargs.get('initial', {})
			initial['users'] = instance.user_set.all()
			initial['default_permissions'] = instance.permissions.all()
			kwargs['initial'] = initial
		super(GroupAdminForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		group = super(GroupAdminForm, self).save(commit=commit)

		if commit:
			group.user_set = self.cleaned_data['users']
		else:
			old_save_m2m = self.save_m2m
			def new_save_m2m():
				old_save_m2m()
				group.user_set = self.cleaned_data['users']
			self.save_m2m = new_save_m2m
		return group


class MyGroupAdmin(GroupAdmin):
	form = GroupAdminForm

admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)
