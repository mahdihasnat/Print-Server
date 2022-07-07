"""printserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from users.views import status_view, home_view
from django.contrib.auth import views as auth_views

from prints.views import pdf_view, submit_view
urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Login and Logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='home'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Client facing pages
    path('', home_view, name='home'),
    path('submit/', submit_view, name='submit'),
    path('status/', status_view, name='status'),

    path('pdf/<int:print_id>.pdf', pdf_view, name='pdf'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
