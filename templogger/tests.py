# -*- coding: utf-8 -*-
"""Cobertura de testes do projeto"""
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.


class ConsultaCidadeTest(TestCase):
    """Cobrira os testes relacionados ao servico de dados de cidades"""

    CIDADE = u'Rio de Janeiro'
    CIDADE_INVALIDA = 'SbrublesCity'
    CIDADE_PADRAO = 'Sao Paulo'

    @staticmethod
    def buscar_cidade_exemplo(exemplo):
        """busca e gera uma cidade exemplo"""
        from .datasources import ConsultaCidade
        return ConsultaCidade(exemplo)

    def test_busca_cidade(self):
        """testa se os dados de cidade recebidos casam com a cidade buscada"""
        cidade = self.buscar_cidade_exemplo(self.CIDADE)
        self.assertEqual(self.CIDADE, cidade.dados['cidade'])

    def test_busca_cidade_invalida(self):
        """Testa se na busca de uma cidade inválida o resultado alem de
        ser diferente do informado, é igual ao padrão 'Sao Paulo'"""
        cidade = self.buscar_cidade_exemplo(self.CIDADE_INVALIDA)
        self.assertNotEqual(self.CIDADE_INVALIDA, cidade.dados['cidade'])
        self.assertEqual(self.CIDADE_PADRAO, cidade.dados['cidade'])


class ConsutaCepTest(TestCase):
    """Cobrira os testes de busca de CEP no ViaCEP"""

    CEP = '21940-230'
    CEP_INVALIDO = '9232'
    CEP_INEXISTENTE = '99999999'

    @staticmethod
    def busca_cep_exemplo(exemplo):
        """busca um cep de exemplo na base do ViaCEP"""
        from .datasources import ConsultaCep
        return ConsultaCep(exemplo)

    def test_busca_cep(self):
        """testa se o cep informado é o mesmo do retornado"""
        cep = self.busca_cep_exemplo(self.CEP)
        self.assertEqual(self.CEP, cep.dados['cep'])

    def test_cpf_invalido(self):
        """testa se CPF invalido informado gera Código 400"""
        with self.assertRaises(Exception):
            self.busca_cep_exemplo(self.CEP_INVALIDO)

    def testa_cpf_nao_encontrado(self):
        """Dado um cep inexistente, checa o lancamentode ValueError"""
        with self.assertRaises(ValueError):
            self.busca_cep_exemplo(self.CEP_INEXISTENTE)


class IntegradoCidadePorCep(TestCase):
    """Testes integrando as buscas de Cidade e CEP"""
    CEP = '21940-230'
    CIDADE = 'Rio de Janeiro'

    def test_busca_cidade_por_cep(self):
        """Verifica se é possível buscar uma cidade a partir de seu cep"""
        from .datasources import ConsultaCep, ConsultaCidade
        cep = ConsultaCep(self.CEP)
        cidade = ConsultaCidade(cep.dados['cidade'])
        self.assertEqual(self.CIDADE, cidade.dados['cidade'])