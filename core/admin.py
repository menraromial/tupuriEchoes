from core.models import Band, Member
from django.contrib import admin


class MemberAdmin(admin.ModelAdmin):
    """Customize the look of the auto-generated admin for the Member model"""

    list_display = ("name", "instrument")
    list_filter = ("band",)

admin.site.register(Band)  # Use the default options
admin.site.register(Member, MemberAdmin)  # Use the customized options