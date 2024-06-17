from django.db import models


class Pessoa(models.Model):
    id_pessoa = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=20)
    def __str__(self):
        return self.nome


class Carteira(models.Model):
    id_carteira = models.AutoField(primary_key=True)
    nome_carteira = models.CharField(max_length=100)
    valor_total_carteira = models.DecimalField(max_digits=10, decimal_places=2)
    descricao_carteira = models.TextField(blank=True, null=True)
    id_pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='carteiras')

    def __str__(self):
        return self.nome_carteira


class CategoriaAtivo(models.Model):
    id_categoria_ativo = models.AutoField(primary_key=True)
    nome_categoria_ativo = models.CharField(max_length=100)
    descricao_categoria_ativo = models.TextField(blank=True, null=True)
    classe_risco = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_categoria_ativo


class News(models.Model):
    id_news = models.AutoField(primary_key=True)
    data_publicacao = models.DateField()
    arquivos_news = models.URLField()

    def __str__(self):
        return self.arquivos_news


class Setor(models.Model):
    id_setor = models.AutoField(primary_key=True)
    nome_setor = models.CharField(max_length=100)
    descricao_setor = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_setor


class Ativo(models.Model):
    ticker = models.AutoField(primary_key=True)
    id_news = models.ForeignKey(News, on_delete=models.CASCADE)
    id_setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    id_categoria_ativo = models.ForeignKey(CategoriaAtivo, on_delete=models.CASCADE)


class Operacao(models.Model):
    id_operacao = models.AutoField(primary_key=True)
    data_operacao = models.DateField()
    valor_un_operacao = models.DecimalField(max_digits=10, decimal_places=2)
    qtd_operacao = models.IntegerField()
    tipo_operacao = models.CharField(max_length=50)
    ticker = models.ForeignKey(Ativo, on_delete=models.CASCADE)


class CarteiraOperacao(models.Model):
    id_carteira_ativo = models.AutoField(primary_key=True)
    data_insercao = models.DateField()
    valor_total_ativo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_medio_ativo = models.DecimalField(max_digits=10, decimal_places=2)
    id_carteira = models.ForeignKey(Carteira, on_delete=models.CASCADE)
    id_operacao = models.ForeignKey(Operacao, on_delete=models.CASCADE)


Carteira.operacoes = models.ManyToManyField(Operacao, through=CarteiraOperacao)
