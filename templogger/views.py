# -*- coding: utf-8 -*-
"""Modulo contendo as views REST designadas para o projeto"""
from __future__ import unicode_literals
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .serializers import cidadeserializer

MSG_CIDADE_INEXISTENTE = u"Cidade {0} não está cadastrada"


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
                    MSG_CIDADE_INEXISTENTE.format(nomecidade))},
                status=status.HTTP_404_NOT_FOUND)
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
                    MSG_CIDADE_INEXISTENTE.format(nomecidade))},
                status=status.HTTP_404_NOT_FOUND)
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


@api_view(['DELETE'])
def apagar_temperaturas(request, nomecidade):
    """Apaga todas as temperaturas registradas de uma cidade"""
    del request
    from .models import Cidade

    try:
        cidade = Cidade.objects.obter(nomecidade)
        cidade.limpartemperaturas()
        return Response(cidadeserializer(cidade))
    except ObjectDoesNotExist as erro:
        return Response(
            {'erro': unicode(
                MSG_CIDADE_INEXISTENTE.format(nomecidade))},
            status=status.HTTP_404_NOT_FOUND)
    except (ValueError, ValidationError) as erro:
        return Response({'erro': unicode(erro)},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def retornar_cidades(request):
    """Retorna uma lista paginável de cidades"""
    from .models import Cidade
    from django.db.models import Max
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    todas_cidades = Cidade.objects.all()
    todas_cidades = todas_cidades.annotate(
        max_data=Max('temperatura__data')).\
        order_by('-max_data')

    pagina = request.GET.get('page', '1')

    paginator = Paginator(todas_cidades, 10)

    try:
        todas_cidades = paginator.page(pagina)
    except PageNotAnInteger:
        todas_cidades = paginator.page(1)
    except EmptyPage:
        todas_cidades = paginator.page(paginator.num_pages)

    return Response(map(cidadeserializer, todas_cidades))
