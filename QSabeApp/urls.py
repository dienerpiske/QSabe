from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^accounts/profile/', include(admin.site.urls)),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name':'index.html'}),
    url(r'^logout/', 'QSabeApp.views.doLogout', name='doLogout'),
    url(r'^home/', 'QSabeApp.views.goHome', name='goHome'),
    
    
    
    
    
    url(r'^listagem/', 'QSabeApp.views.main', name='main'),
    url(r'^(?P<pk>[0-9]+)/perguntas/$', 'QSabeApp.views.questao', name='questao'),
    url(r'^(?P<pk>[0-9]+)/respostas/$', 'QSabeApp.views.pergunta', name='pergunta'),
    url(r"^postar/(nova_pergunta|responder)/(\d+)/$", 'QSabeApp.views.postar',name='postar'),
    url(r"^responder/(\d+)/$", 'QSabeApp.views.responder',name='responder'),
    url(r"^recomendadas/", 'QSabeApp.views.perguntaPorTags',name='recomendadas'),
    url(r"^nova_pergunta/(\d+)/$", 'QSabeApp.views.nova_pergunta', name='nova_pergunta'),
)
