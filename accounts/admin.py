from django.contrib import admin
from accounts.models import *
from bitfield import BitField

from bitfield.forms import BitFieldCheckboxSelectMultiple


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user',)
    search_fields = ('email', 'name')
    formfield_overrides = {
        BitField: {
            'widget': BitFieldCheckboxSelectMultiple},
    }


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(TempToken)
admin.site.register(Funds)
