# -*- coding: utf-8 -*-
"""Modulo contendo as views REST designadas para o projeto"""
from __future__ import unicode_literals
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .serializers import cidadeserializer


class CidadeApi(APIView):
    """Gerencia todos os requests do padrao cities/(parametro)"""

    def post(self, request, nomecidade):
        """Inclui uma cidade a partir do seu nome"""
        del request
        from .models import Cidade

        try:
            cidade = Cidade.objects.nova(nomecidade)
            return Response(cidadeserializer(cidade))
        except (ValueError, ValidationError) as erro:
            return Response({'erro': unicode(erro)},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, nomecidade):
        """Exclui uma cidade e todas as temperaturas
        associadas a partir de seu nome"""
        del request
        from .models import Cidade

        try:
            Cidade.objects.deletar(nomecidade)
        except ObjectDoesNotExist as erro:
            return Response(
                {'erro': unicode(
                    u"Cidade {0} não está cadastrada".format(nomecidade))},
                status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, ValidationError) as erro:
            return Response({'erro': unicode(erro)},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"OK"})

    def get(self, request, nomecidade):
        """Obtem as últimas trinta temperaturas registradas da cidade"""
        del request
        from .models import Cidade
        try:
            cidade = Cidade.objects.obter(nomecidade)
            return Response(cidadeserializer(cidade))
        except ObjectDoesNotExist as erro:
            return Response(
                {'erro': unicode(
                    u"Cidade {0} não está cadastrada".format(nomecidade))},
                status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, ValidationError) as erro:
            return Response({'erro': unicode(erro)},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def nova_cidade_por_cep(request, cep):
    """Inclui uma cidade a partir do seu nome"""
    del request
    from .models import Cidade

    try:
        cidade = Cidade.objects.novaporcep(cep)
        return Response(cidadeserializer(cidade))
    except (ValueError, ValidationError) as erro:
        return Response({'erro': unicode(erro)},
                        status=status.HTTP_400_BAD_REQUEST)
