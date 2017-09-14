Temperometer
============
Aplicação para o teste da Stone Pagamentos

Instruções:
___________


1.  Instalação do virtualenv (utilizando virtualenvwrapper):

        mkvirtualenv temperometer

2.  Para ativar no virtualenv criado, caso necessário:

        workon temperometer

3.  Instalação dos pacotes do projeto (utilizando pip):

        cd pasta_do_projeto
        pip install --upgrade pip
        pip install -r requirements.txt

4.  Rodando o check inicial:

        ./manage.py check

5.  Rodando as migrations iniciais e gerando a base de dados padrão:

        ./manage.py migrate

Testes:
_______

1.  Para efetuar os testes e extrair o relatório de cobertura:

        coverage run manage.py test

2.  Para gerar o report de cobertura:

        coverage report -m

3.  Para rodar o pep8:

        pep8 .

Utilização
__________

1.  Para executar o comando de atualização automática das temperaturas das cidades é necessário executar:

        workon temperometer
        ./manage.py atualizartemperaturas

Este processo pode ser cadastrado no crontab do servidor para ser executado de hora em hora.
Para obter ajuda de utilização ou para auxílio na configuração do python path diretamente na execução do comando:
        
        ./manage.py help atualizartemperaturas

2.  Para rodar o servidor de desenvolvimento local e realizar chamadas basta:
  
        ./manage.py runserver

3. Com o servidor de desenvolvimento rodando, pode-se executar os seguintes exemplos de chamadas:

        curl -X POST --data '' 'http://localhost:8000/cities/cabo_frio/'
        curl -X POST --data '' 'http://localhost:8000/cities/by_cep/21931600/
        curl -X GET --data '' 'http://localhost:8000/cities/cabo_frio/'
        curl -X DELETE --data '' 'http://localhost:8000/cities/cabo_frio/'
        curl -X DELETE --data '' 'http://localhost:8000/cities/rio_de_janeiro/temperatures/'
        curl -X GET --data '' 'http://localhost:8000/temperatures/?page=1'