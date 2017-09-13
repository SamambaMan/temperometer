Temperometer
============
Aplicação para o teste da Stone Pagamentos

Instruções:
___________


1. Instalação do virtualenv (utilizando virtualenvwrapper):
    :
        $mkvirtualenv temperometer

2. Para ativar no virtualenv criado, caso necessário:
    :
        workon temperometer

3. Instalação dos pacotes do projeto (utilizando pip):
    :
        cd $(pasta do projeto)
        pip install --upgrade pip
        pip install -r requirements.txt



Testes:
_______
Para efetuar os testes e extrair o relatório de cobertura:
    :
        coverage run manage.py test