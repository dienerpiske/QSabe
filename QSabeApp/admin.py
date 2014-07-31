from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django import forms
from QSabeApp.models import *

# Register your models here.
class FormPerguntas(forms.ModelForm):
    class Meta:
        model = Pergunta

    tags = forms.CharField(max_length=30, required=False)

class QuestoesAdmin(admin.ModelAdmin):
    pass

class PerguntaAdmin(admin.ModelAdmin):
    form = FormPerguntas

class RespostaAdmin(admin.ModelAdmin):
    search_fields = ["titulo", "criador"]
    list_display = ["titulo", "pergunta", "criador", "dtCriacao"]

class PerfilUsuarioAdmin(admin.ModelAdmin):
    search_fields = ["especialidades"]
    list_display = ["usuario", "postagens", "especialidades"]

admin.site.register(Questoes, QuestoesAdmin)
admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Resposta, RespostaAdmin)
admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)