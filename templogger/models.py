# -*- coding: utf-8 -*-
"""Modelo de dados da aplicação"""
from __future__ import unicode_literals
from django.db import models


class CidadeManager(models.Manager):
    """Model manager de negócio de Cidade
    O manager assume que todas as consultas serão realizadas
    a partir do nome de cidade informado pelo usuário.
    """
    @staticmethod
    def criarcidade(nomecidade):
        """cria e salva uma nova cidade a partir do nome de cidade informado
        Caso o usuário informe um nome de cidade diferente mas que gere
        conflito de nomes da base de dados do GH o sistema irá validar e
        não permitirá esta criacao"""
        from .datasources import ConsultaCidade

        cidade = ConsultaCidade(nomecidade)

        nova_cidade = Cidade()
        nova_cidade.nomeinformado = nomecidade
        nova_cidade.nome = cidade.dados['cidade']

        nova_cidade.clean()
        nova_cidade.save()

        return nova_cidade


class Cidade(models.Model):
    """Armazena dados de cidades"""

    nome = models.CharField(max_length=100)
    nomeinformado = models.CharField(max_length=100)
    objects = CidadeManager()

    def clean(self):
        """valida se existe outra cidade ja cadastrada na
        base com o mesmo nome da API gerado para a cidade sendo salva"""
        from django.core.exceptions import ValidationError

        idcidade = (0 if self.id is None else self.id)

        if Cidade.objects.filter(nome=self.nome).exclude(id=idcidade).count() > 0:
            raise ValidationError(
                "Já existe cadastrada uma cidade com o nome {0}"
                .format(self.nome))



class Temperatura(models.Model):
    """Armazena as temperaturas das cidades"""

    cidade = models.ForeignKey('Cidade')
    data_pesquisa = models.DateField()
    data = models.DateField()
    temperatura = models.IntegerField()
