# -*- coding: utf-8 -*-
"""Cobertura de testes das views"""
from __future__ import unicode_literals
from rest_framework.test import APITestCase


class CidadeViewTest(APITestCase):
    """Testa as views de CRD de Cidade"""

    INEXISTENTE = 'sbrubles'
    CIDADE = 'sao lourenco'
    CIDADE_APAGAR = 'marica'
    CIDADE_TEMPERATURAS = 'campinas'
    CEP = '23914-000'
    CIDADE_CEP = 'Angra dos Reis'

    def test_inclusao(self):
        """testa a inclusao de cidades"""
        response = self.client.post('/cities/{0}/'.format(self.CIDADE))
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/cities/{0}/'.format(self.CIDADE))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['city'], self.CIDADE)
        response = self.client.post('/cities/{0}/'.format(self.CIDADE))
        self.assertEquals(response.status_code, 400)

    def test_inexistente(self):
        """testa obtencao de cidade inexistente"""
        response = self.client.get('/cities/{0}/'.format(self.INEXISTENTE))
        self.assertEquals(response.status_code, 404)

    def test_delecao(self):
        """testa a remocao de cidades"""
        response = self.client.post('/cities/{0}/'.format(self.CIDADE_APAGAR))
        self.assertEquals(response.status_code, 200)
        response = self.client.delete('/cities/{0}/'.format(self.CIDADE_APAGAR))
        self.assertEquals(response.status_code, 200)
        response = self.client.delete('/cities/{0}/'.format(self.CIDADE_APAGAR))
        self.assertEquals(response.status_code, 404)

    def test_obtencao_temperaturas(self):
        """testa para saber se o sistema tras as temperaturas como esperado"""
        from .management.commands.atualizartemperaturas import Command
        response = self.client.post('/cities/{0}/'.format(self.CIDADE_TEMPERATURAS))
        self.assertEquals(response.status_code, 200)
        atualizador = Command()
        atualizador.handle()
        response = self.client.get('/cities/{0}/'.format(self.CIDADE_TEMPERATURAS))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(response.json()['temperatures']), 1)
        response = self.client.get('/temperatures/')
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/temperatures/?page=1')
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/temperatures/?page=10')
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/temperatures/?page=a')
        self.assertEquals(response.status_code, 200)
        response = self.client.delete('/cities/{0}/temperatures/'.format(self.CIDADE_TEMPERATURAS))
        self.assertEquals(response.status_code, 200)

    def test_cep(self):
        response = self.client.post('/cities/by_cep/{0}/'.format(self.CEP))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['city'], self.CIDADE_CEP)
        response = self.client.post('/cities/by_cep/{0}/'.format(self.CEP))
        self.assertEquals(response.status_code, 400)

