from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.db.models.signals import post_save

class Questoes(models.Model):
    titulo = models.CharField(max_length=60)

    def numPostagem(self):
        return sum([t.numPostagem() for t in self.pergunta_set.all()])

    def ultimaPostagem(self):
        if self.pergunta_set.count():
            ultima = None
            for t in self.pergunta_set.all():
                l = t.ultimaResposta()
                if l:
                    if not ultima: ultima = l
                    elif l.dtCriacao > ultima.dtCriacao: ultima = l
            return ultima

    def __unicode__(self):
        return self.titulo

class Pergunta(models.Model):
    titulo = models.CharField(max_length=60)
    explicacao = models.TextField()
    dtCriacao = models.DateTimeField(auto_now_add=True)
    criador = models.ForeignKey(User, blank=False, null=False)
    questoes = models.ForeignKey(Questoes)
    tags = TaggableManager()

    def numPostagem(self):
        return self.resposta_set.count()

    def numResposta(self):
        return self.resposta_set.count() - 1

    def ultimaResposta(self):
        if self.resposta_set.count():
            return self.resposta_set.order_by("dtCriacao")[0]

    def __unicode__(self):
        return unicode(self.criador) + " - " + self.titulo

class Resposta(models.Model):
    titulo = models.CharField(max_length=60)
    dtCriacao = models.DateTimeField(auto_now_add=True)
    criador = models.ForeignKey(User, blank=False, null=False)
    pergunta = models.ForeignKey(Pergunta)
    texto = models.TextField()

    def InfoPerfil(self):
        perfil = self.criador.perfilusuario_set.all()[0]
        return perfil.postagens, perfil.especialidades

    def __unicode__(self):
        return u"%s - %s - %s" % (self.criador, self.pergunta, self.titulo)

class PerfilUsuario(models.Model):
    postagens = models.IntegerField(default=0)
    usuario = models.ForeignKey(User, unique=True)
    especialidades = TaggableManager(blank=True)

    def __unicode__(self):
        return unicode(self.usuario)

def cria_perfil_usuario(sender, **kwargs):
    """Cria im perfil para o usuario ao criar conta"""
    u = kwargs["instance"]
    if not PerfilUsuario.objects.filter(usuario=u):
        PerfilUsuario(usuario=u).save()

post_save.connect(cria_perfil_usuario, sender=User)