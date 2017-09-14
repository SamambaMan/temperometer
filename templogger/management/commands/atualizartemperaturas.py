# -*- coding: utf-8 -*-
"""
Módulo que pode ser executado para atualizar a temperatura de todas
as cidades cadastradas na base de dados"""

from django.core.management import BaseCommand


class Command(BaseCommand):
    """Atualiza as temperaturas das cidades cadastradas"""
    help = "Atualiza as temperaturas das cidades cadastradas"

    def handle(self, *args, **options):
        from templogger.models import Cidade

        # Não efetua o processo transacionado por
        # cidade, já que o método de atualização dos dados
        # encapsula a transação necessária.
        # Também evita parar caso ocorra um erro na atualização
        # da temperatura de uma cidade, para que o processo
        # corra atualizando a temperatura de todas as cidades
        # que conseguir trazer informações dos serviços.

        for cidade in Cidade.objects.all():
            try:
                cidade.buscartemperatura()
            except Exception as error:
                print error
                print cidade
                # TODO: Logar a cidade e o problema que possa ter acontecido

        self.stdout.write(
            self.style.SUCCESS("Temperaturas das cidades atualizadas"))
