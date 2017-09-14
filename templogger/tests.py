# -*- coding: utf-8 -*-
"""Cobertura de testes do projeto"""
from __future__ import unicode_literals

from django.test import TestCase


class ConsultaCidadeTest(TestCase):
    """Cobrira os testes relacionados ao servico de dados de cidades"""

    CIDADE = u'Rio de Janeiro'
    CIDADE_INVALIDA_BY = 'SbrublesCity'
    CIDADE_INVALIDA_KEY = '12312312313123'

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
        with self.assertRaises(ValueError):
            self.buscar_cidade_exemplo(self.CIDADE_INVALIDA_BY)
        with self.assertRaises(ValueError):
            self.buscar_cidade_exemplo(self.CIDADE_INVALIDA_KEY)


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


class IntegradoCidadePorCepTest(TestCase):
    """Testes integrando as buscas de Cidade e CEP"""
    CEP = '21940-230'
    CIDADE = 'Rio de Janeiro'

    CEP_INTEGRADO = '76811-550'
    CIDADE_INTEGRADO = 'Porto Velho'

    def test_busca_cidade_por_cep(self):
        """Verifica se é possível buscar uma cidade a partir de seu cep"""
        from .datasources import ConsultaCep, ConsultaCidade
        cep = ConsultaCep(self.CEP)
        cidade = ConsultaCidade(cep.dados['cidade'])
        self.assertEqual(self.CIDADE, cidade.dados['cidade'])

    def test_busca_por_cep_coordenado(self):
        """Utiliza o coordinator para realizar a busca por CEP"""
        from .datasources import ConsultaCidadePorCep
        cidade = ConsultaCidadePorCep(self.CEP)
        self.assertEqual(self.CIDADE, cidade.dados['cidade'])

    def test_nova_cidade_por_cep_integrado(self):
        """Adiciona uma nova cidade por cep"""
        from .models import Cidade
        cidade = Cidade.objects.novaporcep(self.CEP_INTEGRADO)
        self.assertEqual(self.CIDADE_INTEGRADO, cidade.nome)
        cidade = Cidade.objects.obter(self.CIDADE_INTEGRADO)
        self.assertEqual(self.CIDADE_INTEGRADO, cidade.nome)


class CidadeTest(TestCase):
    """Testes de CRD e validação de Cidade"""
    CIDADE = 'Rio de Janeiro'
    CIDADE_INVALIDA_KEY = '12312312313123'
    CIDADE_APAGAR = 'Sao Paulo'
    CIDADE_BUSCAR_TEMPERATURA = 'Belo Horizonte'

    def test_criacao_cidade(self):
        """testa a criacao de cidade e validacoes atreladas a criacao
        de novas cidades"""
        from .models import Cidade
        from django.core.exceptions import ValidationError, ObjectDoesNotExist

        nova_cidade = Cidade.objects.nova(self.CIDADE)
        self.assertEqual(nova_cidade.nomeinformado, self.CIDADE)
        self.assertEqual(str(nova_cidade), self.CIDADE)

        # testa a obtenção da cidade criada
        try:
            Cidade.objects.obter(self.CIDADE)
        except ObjectDoesNotExist:
            self.fail(u"""Não foi encontrada a cidade
                cadastrada anteriormente pelo seu nome""")

        # testa se não é possível achar uma cidade inexistente
        with self.assertRaises(ObjectDoesNotExist):
            Cidade.objects.obter(self.CIDADE_INVALIDA_KEY)

        # testa se, criando novamente a cidade com o mesmo nome
        # o sistema deverá lançar erro
        with self.assertRaises(ValidationError):
            Cidade.objects.nova(self.CIDADE)

    def test_delecao_cidade(self):
        """quando uma cidade for deletada seus registros devem ser apagados
        e ela não deve ser encontrada"""
        from .models import Cidade
        from django.core.exceptions import ObjectDoesNotExist

        Cidade.objects.nova(self.CIDADE_APAGAR)
        Cidade.objects.deletar(self.CIDADE_APAGAR)

        with self.assertRaises(ObjectDoesNotExist):
            Cidade.objects.obter(self.CIDADE_APAGAR)

    def test_busca_temperatura(self):
        """verificar a busca e contabilizacao de temperaturas"""
        from .models import Cidade

        cidade = Cidade.objects.nova(self.CIDADE_BUSCAR_TEMPERATURA)
        self.assertEqual(cidade.temperatura_set.count(), 0)
        cidade.buscartemperatura()
        self.assertEqual(cidade.temperatura_set.count(), 1)
        cidade.buscartemperatura()
        self.assertEqual(cidade.temperatura_set.count(), 2)
        cidade.limpartemperaturas()
        self.assertEqual(cidade.temperatura_set.count(), 0)


