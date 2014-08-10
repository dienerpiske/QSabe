# -*- coding: utf-8 -*-
import nltk
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.forms import ModelForm
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, logout, login
from django.template import Context, loader, RequestContext
from QSabeApp import summarize
from django.core.context_processors import csrf
from django.views.decorators.csrf import *
from django.db import IntegrityError
from QSabeApp.models import *
from taggit.models import Tag
from django.contrib.auth.decorators import login_required

def doLogout(request):
    logout(request)
    return HttpResponseRedirect('/qsabe/')

@login_required()
def goHome(request):
    return render_to_response("home.html", {'user' : request.user})

@login_required()
def goAreas(request):
    return render_to_response("areas.html", {'user' : request.user})

@login_required()
def goPergunta(request, id_pergunta):
    return render_to_response("pergunta.html", {'user' : request.user})

@csrf_exempt
@login_required()
def goPerguntar(request):
    return render_to_response("perguntar.html", {'user' : request.user})

@csrf_exempt
@login_required()
def goResponder(request, id_pergunta):
    return render_to_response("responder.html", {'user' : request.user})

@csrf_exempt
def goCadastrar(request):
    sucess_message = ''
    error_message = ''
    
    try:  
        if request.POST:
            usuario = User()
            usuario.first_name = request.POST['primeiroNome']
            usuario.last_name = request.POST['ultimoNome']
            usuario.username = request.POST['nomeUsuario']
            usuario.email = request.POST['emailUsuario']
            usuario.set_password(request.POST['senhaUsuario'])
            
            usuario.save()
            
            sucess_message = 'Usu�rio Cadastrado com Sucesso!'
    
    except IntegrityError:
        error_message = 'Usu�rio j� existe!'
        return render(request,'cadastrar.html',{'error_message' : error_message})
      
    return render(request,'cadastrar.html',{'sucess_message' : sucess_message})











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
        emtags = nltk.pos_tag(tokenizada)
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