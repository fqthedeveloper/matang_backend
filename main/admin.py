from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "gender",
        "mobile",
        "age",
        "occupation",
        "created_at",
    )

    search_fields = (
        "full_name",
        "mobile",
        "father_name",
    )

    list_filter = (
        "gender",
        "created_at",
    )

    ordering = ("-id",)