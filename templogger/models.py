# -*- coding: utf-8 -*-
"""Modelo de dados da aplicação"""
from __future__ import unicode_literals
from django.db import models, transaction
from .managers import CidadeManager


class Cidade(models.Model):
    """Armazena dados de cidades"""

    nome = models.CharField(max_length=100)
    nomeinformado = models.CharField(max_length=100)
    objects = CidadeManager()

    def __str__(self):
        if self.nomeinformado is not None:
            return str(self.nomeinformado)

    def clean(self):
        """valida se existe outra cidade ja cadastrada na
        base com o mesmo nome da API gerado para a cidade sendo salva"""
        from django.core.exceptions import ValidationError

        idcidade = (0 if self.id is None else self.id)

        if Cidade.objects.filter(nome=self.nome).\
                exclude(id=idcidade).count() > 0:
            raise ValidationError(
                u"Já existe cadastrada uma cidade com o nome {0}"
                .format(self.nome))

    @transaction.atomic
    def delete(self, using=None, keep_parents=False):
        """apaga a cidade e todas as temperatuaras anexadas a ela"""
        self.apagartemperaturas()
        super(Cidade, self).delete(using)

    @transaction.atomic
    def apagartemperaturas(self):
        """apaga todas as temperaturas associadas a cidade"""
        self.temperatura_set.all().delete()

    FDATA = '%d/%m/%Y %H:%M'

    @transaction.atomic
    def buscartemperatura(self):
        """armazena uma nova temperatura a partir da fonte de dados"""
        from .datasources import ConsultaCidade
        from datetime import datetime
        from django.utils.timezone import utc

        dadoscidade = ConsultaCidade(self.nome)

        nova_temperatura = Temperatura(
            cidade=self,
            data_pesquisa=datetime.utcnow().replace(tzinfo=utc),
            data=datetime.strptime("{0} {1}"
                                   .format(dadoscidade.dados['data'],
                                           dadoscidade.dados['hora']),
                                   self.FDATA).replace(tzinfo=utc),
            temperatura=int(dadoscidade.dados['temperatura'])
        )

        nova_temperatura.clean()
        nova_temperatura.save()
        return nova_temperatura

    @transaction.atomic
    def limpartemperaturas(self):
        """limpa o histórico de temperaturas de uma cidade"""
        self.temperatura_set.all().delete()


class Temperatura(models.Model):
    """Armazena as temperaturas das cidades"""
    cidade = models.ForeignKey('Cidade')
    data_pesquisa = models.DateTimeField()
    data = models.DateTimeField()
    temperatura = models.IntegerField()
