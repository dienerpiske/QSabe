from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib import admin
admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
    (r'^qsabe/', include('QSabeApp.urls')),
    (dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    #url(r'^$', 'django.contrib.auth.views.login', {'template_name':'index.html'}),
    url(r'^accounts/profile/', include(admin.site.urls)),
    url(r'^listagem/', 'QSabeApp.views.main', name='main'),
    url(r'^(?P<pk>[0-9]+)/perguntas/$', 'QSabeApp.views.questao', name='questao'),
    url(r'^(?P<pk>[0-9]+)/respostas/$', 'QSabeApp.views.pergunta', name='pergunta'),
    url(r"^postar/(nova_pergunta|responder)/(\d+)/$", 'QSabeApp.views.postar',name='postar'),
    url(r"^responder/(\d+)/$", 'QSabeApp.views.responder',name='responder'),
    url(r"^recomendadas/", 'QSabeApp.views.perguntaPorTags',name='recomendadas'),
    url(r"^nova_pergunta/(\d+)/$", 'QSabeApp.views.nova_pergunta', name='nova_pergunta'),
)

urlpatterns += staticfiles_urlpatterns()