from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
from app import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registration$', views.registration),
    url(r'^profile$', views.profile),
)

from django.conf.urls.static import static

urlpatterns += static('/css/', document_root='app/static/css/')
urlpatterns += static('/images/', document_root='app/static/images/')
urlpatterns += static('/js/', document_root='app/static/js/')
urlpatterns += static('/profiles/', document_root='app/static/profiles/')
