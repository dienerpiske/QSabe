from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from QSabeApp.models import Questoes, Pergunta, Resposta, PerfilUsuario
from taggit.models import Tag
from QSabeApp import summarize
import nltk

def main(request):
    questoes = Questoes.objects.all()
    context = dict(questoes=questoes, user=request.user)
    return render(request, 'lista.html', context)

def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d

def questao(request, pk):
    """Lista as perguntas"""
    perguntas = Pergunta.objects.filter(questoes=pk).order_by('-dtCriacao')
    context = dict(perguntas=perguntas, pk=pk)
    return render(request, 'perguntas.html',context)

def pergunta(request, pk):
    """Lista todas as respostas de uma pergunta"""
    respostas = Resposta.objects.filter(pergunta=pk).order_by("-dtCriacao")
    titulo = Pergunta.objects.get(pk=pk).titulo
    explicacao = Pergunta.objects.get(pk=pk).explicacao
    tags = Pergunta.objects.get(pk=pk).tags
    context = dict(respostas=respostas, pk=pk, titulo=titulo, explicacao=explicacao, tags=tags)
    return render(request, 'respostas.html', context)

def perguntaPorTags(request):
    """Lista as perguntas com as tags do usuario"""
    perfil = request.user.perfilusuario_set.all()[0]
    tagssimilares = perfil.especialidades.similar_objects()
    context = dict(tagssimilares=tagssimilares)
    return render(request, 'recomendadas.html',context)

def postar(request, ptipo, pk):
    """Exibe um form de post generico"""
    acao = reverse("QSabeApp.views.%s" % ptipo, args=[pk])
    if ptipo == "nova_pergunta":
        titulo = "Nova Pergunta"
        destino = ''
    elif ptipo == "responder":
        titulo = "Responder"
        destino = "Resposta: " + Pergunta.objects.get(pk=pk).titulo
    context = dict(destino=destino,acao=acao,titulo=titulo)
    return render(request, 'postar.html', context)

def nova_pergunta(request, pk):
    """Inicia uma nova pergunta"""
    p = request.POST
    if p["destino"] and p["conteudo"]:
        questao = Questoes.objects.get(pk=pk)
        #tokenizacao, tagging, removedor de stopwords
        frase = p["destino"]
        frase = frase.lower()
        tokenizada = nltk.word_tokenize(frase)
        emtags = nltk.tag.pos_tag(tokenizada)
        stopwords = nltk.corpus.stopwords.words('portuguese')
        filtered_words = [w for w in emtags if w not in stopwords]
        #filtra apenas os substantivos
        substantivos = [word for word,pos in filtered_words if 'N' in pos]
        tags = [w for w in substantivos if w not in stopwords]
        pergunta = Pergunta.objects.create(questoes=questao, titulo=p["destino"], explicacao=p["conteudo"],
                                           criador=request.user)
        pergunta.tags.add(*tags)
    return HttpResponseRedirect(reverse("questao", args=[pk]))

def responder(request, pk):
    """Responde a uma pergunta"""
    p = request.POST
    if p["conteudo"]:
        pergunta = Pergunta.objects.get(pk=pk)
        tags = Tag.objects.filter(pergunta__id=pk)
        titulo = summarize.summarize_text(p["conteudo"])
        titulo = titulo.summaries
        titulo = titulo[0]
        resposta = Resposta.objects.create(pergunta=pergunta, titulo=titulo, texto=p["conteudo"],
                                           criador=request.user)
        #insere tag no perfil
        perfil = request.user.perfilusuario_set.all()[0]
        perfil.especialidades.add(*tags)
    return HttpResponseRedirect(reverse("pergunta", args=[pk]))