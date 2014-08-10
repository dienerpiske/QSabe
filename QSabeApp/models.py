from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.db.models.signals import post_save

class Area(models.Model):
    nome = models.CharField(max_length=100)
    
    def especialistas(self):
        return ["",""] #TODO
    
    def recomendarQuestao(self, Pergunta):
        a = "usuario Especialista recebe questao"
        
    def __unicode__(self):
        return self.nome

class Pergunta(models.Model):
    titulo = models.TextField()
    descricao = models.TextField()
    dtCriacao = models.DateTimeField(auto_now_add=True)
    criador = models.ForeignKey(User, blank=False, null=False)
    likes = models.IntegerField()
    area = models.ForeignKey(Area)
    
    def ultimaResposta(self):
        if self.resposta_set.count():
            return self.resposta_set.order_by("dtCriacao")[0]

    def __unicode__(self):
        return u"{%s - %s}" % (self.criador, self.titulo)
    
class Resposta(models.Model):
    texto = models.TextField()
    fonte = models.CharField(max_length=200)
    dtCriacao = models.DateTimeField(auto_now_add=True)
    criador = models.ForeignKey(User, blank=False, null=False)
    pergunta = models.ForeignKey(Pergunta)
    
    def __unicode__(self):
        return u"{%s - %s - %s}" % (self.criador, self.pergunta, self.texto)

class Comentario(models.Model):
    texto = models.TextField()
    dtCriacao = models.DateTimeField(auto_now_add=True)
    criador = models.ForeignKey(User, blank=False, null=False)
    resposta = models.ForeignKey(Resposta)
    
    def __unicode__(self):
        return u"{%s - %s - %s}" % (self.criador, self.resposta, self.texto)

class PerfilUsuario(models.Model):
    usuario = models.ForeignKey(User, unique=True)
    lattes = models.CharField(max_length=100)
    sobre = models.TextField()

    def especialidade(self):
        return "" #TODO
    
    def __unicode__(self):
        return unicode(self.usuario)

def cria_perfil_usuario(sender, **kwargs):
    """Cria im perfil para o usuario ao criar conta"""
    u = kwargs["instance"]
    if not PerfilUsuario.objects.filter(usuario=u):
        PerfilUsuario(usuario=u).save()

post_save.connect(cria_perfil_usuario, sender=User)