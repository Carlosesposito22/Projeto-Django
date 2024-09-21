from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Modalidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Clube(models.Model):
    id = models.AutoField(primary_key=True)
    moderador = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    modalidade = models.ForeignKey('Modalidade', on_delete=models.SET_NULL, null=True, blank=True, default='Sem modalidade')
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True, default='Sem categoria')
    descricao = models.TextField(null=True, blank=True)
    numeroMembros = models.IntegerField(null=True, blank=True, default=1)
    privado = models.BooleanField(default=False)
    favoritado = models.BooleanField(default=False)
    dataDeCriacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} | {self.moderador} | {self.dataDeCriacao.strftime("%d/%m/%Y %H:%M")}'

    def get_absolute_url(self):
        return reverse('club-Detail', args=[str(self.id)])

    def total_avaliacoes(self):
        return self.avaliacao_set.count()  # Total de avaliações
    
    def calcular_media_avaliacoes(self):
        avaliacoes = self.avaliacao_set.all()
        if avaliacoes.exists():
            total = sum(avaliacao.valor for avaliacao in avaliacoes)
            return total / avaliacoes.count()
        return 0  # Retorna 0 se não houver avaliações


class Avaliacao(models.Model):
    clube = models.ForeignKey(Clube, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.IntegerField()

    def __str__(self):
        return f'Avaliação de {self.usuario.username} para {self.clube.titulo} com valor {self.valor}'


class Membro(models.Model):
    clube = models.ForeignKey('Clube', on_delete=models.CASCADE, related_name="membros")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    dataDeEntrada = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=False)
    motivo_recusa = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.clube.titulo}"
