# trabalhos-gerencia-redes

Trabalhos para a disciplina de Gerencia de Redes da UFRGS

Utiliza Python com as bibliotecas Easy SNMP e Tkinter

Comando para criar os usuarios SNMP

/etc/snmpd.conf
- rouser MD5User
- rwuser MD5DESUser

/var/lib/snmp/
- createUser MD5User MD5 "minhasenha"
- createUser MD5DESUser MD5 "minhasenha" DES

Links úteis:
 - https://tkdocs.com/tutorial/index.html
 - https://easysnmp.readthedocs.io/en/latest/
