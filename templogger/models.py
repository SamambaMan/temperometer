# -*- coding: utf-8 -*-
"""Modelo de dados da aplicação"""
from __future__ import unicode_literals
from django.db import models


class Cidade(models.Model):
    """Armazena dados de cidades"""

    nome = models.CharField(max_length=100)
    nomeinformado = models.CharField(max_length=100)


class Temperatura(models.Model):
    """Armazena as temperaturas das cidades"""

    cidade = models.ForeignKey('Cidade')
    data_pesquisa = models.DateField()
    data = models.DateField()
    temperatura = models.IntegerField()
