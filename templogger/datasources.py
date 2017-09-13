# -*- coding: utf-8 -*-
"""
Modulo que condensa as classes que acessarao servicos externos de dados de
Cidade e CEP
"""


class ConsultaCidade(object):
    """
    Classe que permite a consulta da API remota de dados de temperatura de
    Cidades a partir da base do HGBrasil
    """
    def __init__(self, cidade=None):
        """Constroi os atributos da classe e busca os dados da cidade caso seja
        informada"""
        self.dados = None

        if cidade:
            self.recuperardados(cidade)

    def recuperardados(self, cidade):
        """
        Busca na API do HGBrasil os dados de temperatura da cidade e armazena-o
        """
        import requests
        from django.conf import settings
        from django.utils.http import urlquote

        urlapi = settings.HGBRASIL['url']
        chave = settings.HGBRASIL['chave']

        url = '{0}?format=json&city_name={1}&key={2}'
        url = url.format(urlapi, urlquote(cidade), chave)

        retorno = requests.get(url)
        if retorno.status_code != 200:
            raise Exception(
                u"Retorno da chamada ap HGBrasil com código {0}"
                .format(retorno.status_code))

        informacoes = retorno.json()

        # é obrigatório que a consulta seja pelo nome da cidade
        # e que a chave procurada é válida
        if not informacoes['valid_key'] or\
           informacoes['by'] != u'city_name':
            raise ValueError(
                "A cidade '{0}' não foi encontrada".format(cidade))

        self.dados = {
            'cidade': informacoes['results']['city_name'],
            'data': informacoes['results']['date'],
            'hora': informacoes['results']['time'],
            'temperatura': informacoes['results']['temp'],
        }


class ConsultaCep(object):
    """
    Permite a consulta e armazenamento dos dados de CEP e Nome da Cidade
    a partir da base do ViaCEP
    """
    def __init__(self, cep=None):
        """Constroi os atributos da classe e pesquisa pelo CEP caso
        informado"""
        self.dados = None

        if cep:
            self.recuperardados(cep)

    def recuperardados(self, cep):
        """Efetua a busca na API da ViaCEP"""
        import requests
        from django.conf import settings

        urlapi = settings.VIACEP
        url = urlapi.format(cep)

        retorno = requests.get(url)
        if retorno.status_code != 200:
            raise Exception(
                u"Retorno da chamada a ViaCEP com código {0}"
                .format(retorno.status_code))

        informacoes = retorno.json()

        if 'erro' in informacoes:
            raise ValueError(
                """A busca pelo CEP {0} não foi encontrada
                ou gerou um erro remoto""".format(cep))

        self.dados = {
            'cidade': informacoes['localidade'],
            'cep': informacoes['cep']
        }
