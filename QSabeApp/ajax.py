import detectlanguage
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from QSabeApp.models import *
from django.template.loader import render_to_string
from QSabeApp.bing import MicrosoftTranslatorClient

@dajaxice_register
def traduzir(request, titulo, descricao):
    detectlanguage.configuration.api_key = "f2d7fc33a7f3cb0b045d83b6a4c36ad9"
    de = detectlanguage.simple_detect(titulo)
    client = MicrosoftTranslatorClient('sabialiedufes', 'HyJ6rFaIeEPd9q7ZjrWaixrKIUuAXuxIAroGL6YpRl8=')
    t =  client.TranslateText(titulo.encode('utf-8'), de, 'pt')
    d =  client.TranslateText(descricao.encode('utf-8'), de, 'pt')
    return simplejson.dumps({'titulo' : t, 'descricao':d})

@dajaxice_register
def searchminhasperguntas(request, busca):
    perguntas = Pergunta.objects.filter(criador = request.user).filter(titulo__icontains=busca)
    listgroup = render_to_string('div_lg_minhas_perguntas.html', {'perguntas': perguntas})
    return simplejson.dumps({'listgroup': listgroup})

@dajaxice_register
def searchperguntas(request, busca, idArea):
    perguntas = Pergunta.objects.filter(titulo__icontains=busca)
    if idArea is not None:
        perguntas = perguntas.filter(area = Area.objects.get(id = idArea))
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