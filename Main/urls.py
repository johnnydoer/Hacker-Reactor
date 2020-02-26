# from django.urls import path, re_path, include
#
# from . import views
#
# urlpatterns = [
#     path('', views.index, name='M_index'),
#     path('signup/', views.signup, name='M_signup'),
#     path('login/', views.login, name='M_login'),
# ]


from django.conf.urls import url
from django.urls import path,include, re_path
from . import views
from django.conf import settings

# import social_django
app_name = "Main"

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_display, name='login'),

    path('register/', views.register_display, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/reset_password/', views.reset_password, name='reset'),
    url(r'display_reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.display_reset_password, name='display_reset_password'),
    url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='activate'),
    path('save_password/',views.save_password,name='save_password'),
    ]