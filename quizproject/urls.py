from django.conf.urls import *
from django.shortcuts import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('quizapp.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^accounts/', include('quizapp.urls', namespace='accounts')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
