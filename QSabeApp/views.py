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
    u = request.user
    perfil = u.usuario_set.all()[:0]
    perguntas = u.pergunta_set.all()
    interessantes = Pergunta.objects.all()[:5]
    tarefas = u.tarefa_set.all()
    return render_to_response("home.html", {'user' : u,'perfil' : perfil, 'tarefas' : tarefas, 'interessantes':interessantes, 'perguntas':perguntas})

@login_required()
def goAreas(request):
    areas = Area.objects.all()
    perguntas = Pergunta.objects.all()[:10]
    area = None
    return render_to_response("areas.html", {'user' : request.user,'areas' : areas, 'area':area, 'perguntas':perguntas})

@login_required()
def goArea(request, idArea):
    areas = Area.objects.all()
    area = Area.objects.get(id = idArea)
    perguntas = area.pergunta_set.all()
    return render_to_response("areas.html", {'user' : request.user,'areas' : areas, 'area':area, 'perguntas':perguntas})

@login_required()
def goPergunta(request, idPergunta):
    pergunta = Pergunta.objects.get(id= idPergunta)
    semelhantes = Pergunta.objects.all()[:5]
    return render_to_response("pergunta.html", {'user' : request.user, 'pergunta': pergunta, 'semelhantes': semelhantes})

def gerarTags(frase):
    frase = frase.lower()
    tokenizada = nltk.word_tokenize(frase)
    emtags = nltk.pos_tag(tokenizada)
    stopwords = nltk.corpus.stopwords.words('portuguese')
    filtered_words = [w for w in emtags if w not in stopwords]
    #filtra apenas os substantivos
    substantivos = [word for word,pos in filtered_words if 'N' in pos]
    tags=""
    for w in substantivos:
        if w not in stopwords:
            tags+=" " + w
    #tags = [w for w in substantivos if w not in stopwords]
    return tags

@csrf_exempt
@login_required()
def goPerguntar(request, idArea):
    message = ''
    
    try:  
        if request.POST:
            post = request.POST
            p = Pergunta()
            p.titulo = post['tbxpergunta']
            p.descricao = post['tbxinfo']
            p.criador = request.user
            p.likes = 0
            p.tags = gerarTags(p.titulo)
            p.area = Area.objects.get(id = idArea)
            p.save()
            
            sucess_message = 'pergunta enviada com sucesso!'
            return HttpResponseRedirect(reverse("goPergunta", args=[p.id]))
    
    except IntegrityError:
        message = 'Desculpe ocorreu um erro! Tente novamente.'
        return render(request,'peguntar.html',{'error_message' : message})
    
    return render_to_response("perguntar.html", {'user' : request.user, 'sucess_message' : message, 'idArea': idArea})

@csrf_exempt
@login_required()
def goResponder(request, idPergunta):
    message = ''
    perg = Pergunta.objects.get(id=idPergunta)
    try:  
        if request.POST:
            post = request.POST
            r = Resposta()
            r.texto = post['tbxresposta']
            r.fonte = post['tbxfonte']
            r.criador = request.user
            r.likes = 0
            r.tags = gerarTags(r.texto)
            r.pergunta = perg
            r.save()
            
            sucess_message = 'Resposta enviada com sucesso!'
            return HttpResponseRedirect(reverse("goPergunta", args=[perg.id]))
    except IntegrityError:
        message = 'Desculpe ocorreu um erro! Tente novamente.'
        return render(request,'responder.html',{'user' : request.user, 'error_message' : message, 'pergunta': perg})
    
    return render_to_response("responder.html", {'user' : request.user, 'pergunta': perg, 'sucess_message' : message})

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
            
            perfil = usuario.usuario_set.all()[0]
            perfil.lattes = request.POST['lattes']
            perfil.sobre = request.POST['dadosAdicionais']
            perfil.save()
            
            sucess_message = 'Usuário Cadastrado com Sucesso!'
    
    except IntegrityError:
        error_message = 'Usuário já existe!'
        return render(request,'cadastrar.html',{'error_message' : error_message})
      
    return render(request,'cadastrar.html',{'sucess_message' : sucess_message})


def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d






""""

def main(request):
    questoes = Questoes.objects.all()
    context = dict(questoes=questoes, user=request.user)
    return render(request, 'lista.html', context)



def questao(request, pk):
    #Lista as perguntas
    perguntas = Pergunta.objects.filter(questoes=pk).order_by('-dtCriacao')
    context = dict(perguntas=perguntas, pk=pk)
    return render(request, 'perguntas.html',context)

def pergunta(request, pk):
    #Lista todas as respostas de uma pergunta
    respostas = Resposta.objects.filter(pergunta=pk).order_by("-dtCriacao")
    titulo = Pergunta.objects.get(pk=pk).titulo
    explicacao = Pergunta.objects.get(pk=pk).explicacao
    tags = Pergunta.objects.get(pk=pk).tags
    context = dict(respostas=respostas, pk=pk, titulo=titulo, explicacao=explicacao, tags=tags)
    return render(request, 'respostas.html', context)

def perguntaPorTags(request):
    #Lista as perguntas com as tags do usuario
    perfil = request.user.perfilusuario_set.all()[0]
    tagssimilares = perfil.especialidades.similar_objects()
    context = dict(tagssimilares=tagssimilares)
    return render(request, 'recomendadas.html',context)

def postar(request, ptipo, pk):
    #Exibe um form de post generico
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
    #Inicia uma nova pergunta
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
    #Responde a uma pergunta
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
    
    """