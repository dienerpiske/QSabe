from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django import forms
from QSabeApp.models import *

# Register your models here.
class FormPerguntas(forms.ModelForm):
    class Meta:
        model = Pergunta

    tags = forms.CharField(max_length=30, required=False)

class PerguntaAdmin(admin.ModelAdmin):
    form = FormPerguntas

class ComentarioAdmin(admin.ModelAdmin):
    search_fields = ["texto", "criador"]
    list_display = ["texto", "resposta", "criador", "dtCriacao"]

class RespostaAdmin(admin.ModelAdmin):
    search_fields = ["texto", "criador"]
    list_display = ["texto", "pergunta", "criador", "dtCriacao"]

class UsuarioAdmin(admin.ModelAdmin):
    search_fields = ["user"]
    list_display = ["user","sobre"]

admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Resposta, RespostaAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Area)
admin.site.register(Tarefa)