from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate_account"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("notes/", views.notes_list, name="Notes"),
    path("papers/", views.paper, name="paper"),
    path("resources/", views.resources_list, name="Resource"),
    path("blog/", views.blog_list, name="blog"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact_list, name="contact"),
    path("papers/<int:paper_id>/analysis/", views.analyze_paper, name="analyze_paper"),
    path("chatbot/", views.chatbot, name="chatbot"),
    path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
