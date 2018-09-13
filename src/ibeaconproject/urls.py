"""ibeaconproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^$',
        RedirectView.as_view(url=reverse_lazy('beacons:beacon-list')), 
        name='home'),
    url(r'^beacons/', include('ibeaconapp.urls', namespace='beacons')),

    url(r'^accounts/', include('registration.backends.simple.urls')),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
