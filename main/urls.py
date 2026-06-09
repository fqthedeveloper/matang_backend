from django.urls import path

from . import views
from .auth_views import admin_login, current_admin
from rest_framework_simplejwt.views import (

    TokenRefreshView,
)
from .pdf_views import (
    generate_member_pdf
)

urlpatterns = [

    path(
        "auth/login/",
        admin_login
    ),
    
    path(
        "token/refresh/",
        TokenRefreshView.as_view()
    ),

    path(
        "auth/me/",
        current_admin
    ),

    path(
        "dashboard/",
        views.dashboard_stats
    ),

    # Member CRUD

    path(
        "members/",
        views.member_list
    ),

    path(
        "members/create/",
        views.create_member
    ),

    path(
        "members/<int:pk>/",
        views.member_detail
    ),

    path(
        "members/update/<int:pk>/",
        views.update_member
    ),

    path(
        "members/delete/<int:pk>/",
        views.delete_member
    ),

    # Search

    path(
        "members/search/",
        views.search_member
    ),

    # Filters

    path(
        "members/males/",
        views.male_members
    ),

    path(
        "members/females/",
        views.female_members
    ),
    
    path(
        "members/pdf/<int:pk>/",
        generate_member_pdf,
        name="member_pdf"
    ),
]