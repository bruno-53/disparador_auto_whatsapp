from selenium import webdriver
import re
import unicodedata
import time as time

#CONFIGURAR O SELENIUM
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys


servico = Service(GeckoDriverManager().install())
navegador = webdriver.Firefox(service=servico)

# CONFIGURAR LISTA DE NUMEROS E NOMES
arquivo_numeros = open('numeros.txt','r')
nomes = []
numeros = []

for linha in arquivo_numeros:
    linha = linha.strip()
    linha = unicodedata.normalize("NFD",linha).encode("ascii","ignore").decode("utf-8") # NORMALIZA TEXTO PARA RETIRAR ACENTO DE NOMES ETC.
    numero = re.compile("[0-9]{11}").search(linha).group()
    nome = re.compile("[A-Za-z]+").search(linha).group()
    nomes.append(nome)
    numeros.append(numero)

arquivo_numeros.close()

# ABRE ARQUIVO DE RESULTADOS
arquivo_resultado = open('resultado.txt','w')
resultado = []


#VALIDAR SE O LOGIN FOI FEITO
navegador.get('https://web.whatsapp.com/');
navegador.implicitly_wait(5.0)
validador = navegador.find_element('xpath','/html/body/div[1]/div/div/div[3]/div[2]/div[1]').is_displayed()



# VALIDAR NUMERO
if validador is True:
    print('-----------------------------------')
    print('ATENÇÃO: FAÇA O LOGIN E TECLE ENTER')
    print('-----------------------------------')
    input('...')
    contador = 0
    enviado = 0
    nao_enviado = 0

    for numero in numeros:
        mensagem = ("Atenção! {} esse é um teste automático enviado para você! Desculpe o incômodo").format(nomes[contador])
        navegador.get('https://web.whatsapp.com/send/?phone=55'+ numero +'&text='+ mensagem + '&type=phone_number')
        contador += 1
        navegador.implicitly_wait(20.0)

        # VERIFICA SE É E SALVA EM NOVO ARQUIVO O RESULTADO

        try:
            navegador.find_element('xpath','/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').send_keys(Keys.ENTER)
            time.sleep(5)
            navegador.find_element('xpath','/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').is_displayed()
            print("Resultado: {}... MENSAGEM ENVIADA".format(numero))
            resultado.append("Numero: ")
            resultado.append(numero)
            resultado.append(" - Status: ENVIADO \n")
            enviado += 1
        except:
            mensagem_erro = navegador.find_element('xpath','/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div').is_displayed()
            print("Resultado: {}... NÃO ENVIADO - Numero não whatsapp".format(numero))
            resultado.append("Numero: ")
            resultado.append(numero)
            resultado.append(" - Status: NAO ENVIADO - NAO WHATSAPP \n")
            nao_enviado += 1



print('\n--- RESULTADO ---')
print("TOTAL DE NUMEROS: {}\nENVIADO: {}\nNÃO ENVIADO: {}".format((enviado+nao_enviado),enviado,nao_enviado))
print('----------------')
arquivo_resultado.writelines(resultado)
arquivo_resultado.close()