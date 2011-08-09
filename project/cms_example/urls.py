from django.conf.urls.defaults import *

from django.contrib import admin
import haystack

admin.autodiscover()
haystack.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^', include('cms.urls')),
)
