#!/bin/bash

printf '\nTeste de insercao de cidade '
curl -s -o /dev/null -w "%{http_code}" -X POST   'http://localhost:8000/cities/são%20goncalo/'

printf "\nTeste de obtecao de cidade "
curl -s -o /dev/null -w "%{http_code}" -X GET    'http://localhost:8000/cities/são%20goncalo/'

printf "\nTeste de inclusao por CEP "
curl -s -o /dev/null -w "%{http_code}" -X POST   'http://localhost:8000/cities/by_cep/21931600/'

printf "\nTeste de delecao de temperaturas "
curl -s -o /dev/null -w "%{http_code}" -X DELETE 'http://localhost:8000/cities/rio_de_janeiro/temperatures/'

printf "\nTeste de delecao de cidade do monitoramento "
curl -s -o /dev/null -w "%{http_code}" -X DELETE 'http://localhost:8000/cities/rio_de_janeiro/'

printf "\nTeste de lista de temperaturas paginadas "
curl -s -o /dev/null -w "%{http_code}" -X GET    'http://localhost:8000/temperatures/?page=1'

echo

