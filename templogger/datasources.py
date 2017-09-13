"""
Modulo que condensa as classes que acessarao servicos externos de dados de
cidade e CEP
"""


class ConsultaCidade(object):
    """
    Classe que permite a consulta da API remota de dados de temperatura de
    Cidades
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

        informacoes = retorno.json()

        self.dados = {
            'cidade': informacoes['results']['city_name'],
            'data': informacoes['results']['date'],
            'hora': informacoes['results']['time'],
            'temperatura': informacoes['results']['temp'],
        }
