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
        from .models import Cidade
        from .datasources import ConsultaCidade

        cidade = ConsultaCidade(nomecidade)

        nova_cidade = Cidade()
        nova_cidade.nomeinformado = nomecidade
        nova_cidade.nome = cidade.dados['cidade']

        nova_cidade.clean()
        nova_cidade.save()

        return nova_cidade

    @staticmethod
    def obter(nomecidade):
        """Obtem uma cidade a partir do nome informado pelo usuário no momento
        do cadastro"""
        from .models import Cidade
        return Cidade.objects.get(nomeinformado=nomecidade)

    @staticmethod
    @transaction.atomic
    def deletar(nomecidade):
        """remove uma cidade e todas as suas temperaturas anexadas"""
        from .models import Cidade

        cidade = Cidade.objects.obter(nomecidade)
        cidade.delete()

