# Utilização do extrator

- Baixar dependências

      ~$ wget http://pylockfile.googlecode.com/files/lockfile-0.8.tar.gz

- Instalar dependências

      ~$ sudo apt-get install python2.7
      ~$ sudo apt-get install python-daemon uno

- Instalar lockfile

- Entre em python-damon e altere requirements para 'lockfile==0.8'

- Instalar distribute para python 3.2

      ~$ cd /usr/lib/python3.2
      ~$ sudo wget http://python-distribute.org/distribute_setup.py
      ~$ sudo /usr/bin/python3.2 distribute_setup.py

- Instalar virtualenv

      ~$ sudo /usr/local/bin/easy_install virtualenv
      ~$ sudo /usr/local/bin/virtualenv /srv/lightbase-neo

- Baixar e instalar API

      ~$ sudo svn co http://10.0.0.150/svn/lightbase-neo/trunk/
      ~$ cd trunk/src/liblightbase
      ~$ sudo ../../../bin/python3.2 setup.py install //Obs: Certifique-se que deu certo (tente denovo caso não dê)
      ~$ cd ../LBGenerator
      ~$ sudo ../../../bin/python3.2 setup.py install

- Instalar e configurar o apache

      ~$ sudo apt-get install apache2

- Adicione a seguinte linha no arquivo /etc/apache2/apache2.conf

      ServerName localhost

- Instalar mod-wsgi

      ~$ sudo apt-get install libapache2-mod-wsgi-py3

Certifique-se de dar permissão ao usuário na pasta

    ~$ sudo chown neolight -R /srv/lightbase-neo

- Digite o seguinte no arquivo /etc/apache2/sites-enabled/neo.lightbase.cc

## Use only 1 Python sub-interpreter.  
Multiple sub-interpreters play badly with C extensions.

    <VirtualHost *:80>
        ServerAdmin admin@lightbase.com.br
        ServerName neo.lightbase.cc

        WSGIApplicationGroup %{GLOBAL}
        WSGIPassAuthorization On
        WSGIDaemonProcess lightbase user=neolight group=neolight threads=8 \
            python-path=/srv/lightbase-neo/lib/python3.2/site-packages
        WSGIScriptAlias / /srv/lightbase-neo/trunk/lightbase.wsgi

        <Directory /srv/lightbase-neo>
            WSGIProcessGroup lightbase
            Order allow,deny
            Allow from all
        </Directory>

        ErrorLog /var/log/apache2/neo.lightbase.cc-error.log
        CustomLog /var/log/apache2/neo.lightbase.cc-access.log combined
    </VirtualHost>

- Mude a a linha abaixo, colocando o nome ou ip do seu servidor.

      ServerName neo.lightbase.cc

- Reinicie o apache

      ~$ sudo service apache2 restart


