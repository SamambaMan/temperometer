# -*- coding: utf-8 -*-
"""Módulo contendo os managers do domínio da aplicação"""
from django.db import models
from django.db import transaction


class CidadeManager(models.Manager):
    """Model manager de negócio de Cidade
    O manager assume que todas as consultas serão realizadas
    a partir do nome de cidade informado pelo usuário.
    """
    @staticmethod
    def nova(nomecidade):
        """cria e salva uma nova cidade a partir do nome de cidade informado
        Caso o usuário informe um nome de cidade diferente mas que gere
        conflito de nomes da base de dados do GH o sistema irá validar e
        não permitirá esta criacao"""
        from .datasources import ConsultaCidade

        cidade = ConsultaCidade(nomecidade)

        return CidadeManager._persistenovacidade(nomecidade, cidade)

    @staticmethod
    def novaporcep(cep):
        """Cria e salva uma nova cidade por CEP"""
        from .datasources import ConsultaCidadePorCep

        cidade = ConsultaCidadePorCep(cep)

        return CidadeManager._persistenovacidade(
            cidade.dados['cidade'],
            cidade)

    @staticmethod
    def _persistenovacidade(nomecidade, cidade):
        """Persiste os dados da cidade encontrada na base de dados"""
        from .models import Cidade
        from unidecode import unidecode

        nova_cidade = Cidade()
        nova_cidade.nomeinformado = unidecode(nomecidade)
        nova_cidade.nome = unidecode(cidade.dados['cidade'])

        nova_cidade.clean()
        nova_cidade.save()

        return nova_cidade

    @staticmethod
    def obter(nomecidade):
        """obtem o nome da cidade, assume que o nome possa estar separado por espaços
        ou underscore"""
        from .models import Cidade
        from django.db.models import Q
        from unidecode import unidecode

        nomecidade = unidecode(nomecidade)

        return Cidade.objects.get(
            Q(nomeinformado__iexact=nomecidade.replace(' ', '_')) |
            Q(nomeinformado__iexact=nomecidade.replace('_', ' ')) |
            Q(nome__iexact=nomecidade.replace(' ', '_')) |
            Q(nome__iexact=nomecidade.replace('_', ' ')))

    @staticmethod
    @transaction.atomic
    def deletar(nomecidade):
        """remove uma cidade e todas as suas temperaturas anexadas"""
        from .models import Cidade

        cidade = Cidade.objects.obter(nomecidade)
        cidade.delete()

