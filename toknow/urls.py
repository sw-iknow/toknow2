from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/logout/$', logout),
)

from django.conf.urls.static import static

urlpatterns += static('/css/', document_root='app/static/css/')
urlpatterns += static('/images/', document_root='app/static/images/')
urlpatterns += static('/js/', document_root='app/static/js/')
