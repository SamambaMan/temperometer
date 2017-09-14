# -*- coding: utf-8 -*-
"""Serializadores JSON para as interfaces REST"""


def cidadeserializer(cidade):
    """Serializa uma cidade"""

    FDATA = '%Y-%m-%d %H:%M:%S'

    retorno = {'city': str(cidade.nomeinformado)}
    temperaturas = []
    for temperatura in cidade.temperatura_set.all().order_by('data')[:30]:
        temperaturas += [{'date': temperatura.data.strftime(FDATA),
                          'temperature': temperatura.temperatura}]
    retorno['temperatures'] = temperaturas

    return retorno
