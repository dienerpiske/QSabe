import detectlanguage
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from QSabeApp.models import *
from django.template.loader import render_to_string
from QSabeApp.bing import MicrosoftTranslatorClient

@dajaxice_register
def traduzir(request, texto, de, para):
    detectlanguage.configuration.api_key = "f2d7fc33a7f3cb0b045d83b6a4c36ad9"
    msg = detectlanguage.simple_detect(texto)
    client = MicrosoftTranslatorClient('sabialiedufes', 'HyJ6rFaIeEPd9q7ZjrWaixrKIUuAXuxIAroGL6YpRl8=')
    t =  client.TranslateText(texto.encode('utf-8'), msg, para)
    return simplejson.dumps({'texto' : t})

@dajaxice_register
def searchperguntas(request, busca):
    perguntas = Pergunta.objects.all().filter(titulo__icontains=busca)
    listgroup = render_to_string('div_lg_perguntas.html', {'perguntas': perguntas})
    return simplejson.dumps({'listgroup': listgroup})

@dajaxice_register
def negativarpergunta(request, idp):
    pergunta = Pergunta.objects.get(id=idp)
    likes = pergunta.likes - 1
    pergunta.likes = likes
    pergunta.save()
    return simplejson.dumps({'likes': likes})

@dajaxice_register
def positivarpergunta(request, idp):
    pergunta = Pergunta.objects.get(id=idp)
    likes = pergunta.likes + 1
    pergunta.likes = likes
    pergunta.save()
    return simplejson.dumps({'likes': likes})

@dajaxice_register
def negativarresposta(request, idr):
    pergunta = Resposta.objects.get(id=idr)
    likes = pergunta.likes - 1
    pergunta.likes = likes
    pergunta.save()
    return simplejson.dumps({'likes': likes})

@dajaxice_register
def positivarresposta(request, idr):
    pergunta = Resposta.objects.get(id=idr)
    likes = pergunta.likes + 1
    pergunta.likes = likes
    pergunta.save()
    return simplejson.dumps({'likes': likes})

@dajaxice_register
def salvarcomentario(request, id_resposta, texto):
    comentario = Comentario()
    comentario.texto = texto
    comentario.resposta = Resposta.objects.get(id = id_resposta)
    comentario.criador = request.user
    comentario.save()
    return crialgmarcacao(comentario.resposta)

def crialgmarcacao(resposta):
    comentarios = resposta.comentario_set.all()
    listgroup = render_to_string('div_lg_comentarios.html', {'comentarios': comentarios})
    return simplejson.dumps({'listgroup': listgroup})