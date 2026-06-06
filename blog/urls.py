from django.urls import path
from django.contrib.auth import views as auth_views
from.import views
urlpatterns = [
    path('', views.home, name='home'),
    path('Logout',views.logout_user, name='logout'),
    path('Notes/', views.Notes_list, name='Notes'),
    path('paper/', views.paper, name='paper'),
    path('Resource/',views.Resources_list, name='Resource'),
    path('blog/', views.blog_list, name='blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_list, name='contact'),
    path("paper/<int:paper_id>/analysis/",views.analyze_paper,name="analyze_paper"),


    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('profile', views.profile, name='profile'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),

    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    path(
        'reset_done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]
