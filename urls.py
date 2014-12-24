from django.conf.urls.defaults import patterns,  url
from admisiones.views import *

from admisiones.views2 import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', home, name='home'),
    url(r'^usuario/$', home_2, name='home_2'),
    url(r'^por_ciclo/(?P<ciclo_id>\w+)/(?P<categoria_id>\w+)/$', por_ciclo, name='ciclo'),
    # url(r'^alumnos/', include('alumnos.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^por_reinscribir/(?P<ciclo_id>\d+)/$', por_reinscribir, name='views2.por_reinscribir'),
    url(r'^materias_genericas/(?P<ciclo_id>\d+)/$', materias_genericas, name='views2.materias_genericas'),
)
