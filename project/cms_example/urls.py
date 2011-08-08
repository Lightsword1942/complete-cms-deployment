from django.conf.urls.defaults import *
from django.contrib import admin

import haystack

admin.autodiscover()

haystack.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
)

urlpatterns += patterns('',
    url(r'^tinymce/', include('tinymce.urls')),
)

urlpatterns += patterns('',
    url(r'^', include('cms.urls')),
)
