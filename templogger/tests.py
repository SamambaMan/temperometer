# -*- coding: utf-8 -*-
"""Cobertura de testes do projeto"""
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.


class ConsultaCidadeTest(TestCase):
    """Cobrira os testes relacionados ao servico de dados de cidades"""

    CIDADE = u'Sao Paulo'

    def buscar_cidade_exemplo(self):
        """busca e gera uma cidade, exemplo rio de janeiro"""
        from .datasources import ConsultaCidade
        return ConsultaCidade(self.CIDADE)

    def test_busca_cidade(self):
        """testa se os dados de cidade recebidos casam com a cidade buscada"""
        cidade = self.buscar_cidade_exemplo()
        self.assertEqual(self.CIDADE, cidade.dados['cidade'])
