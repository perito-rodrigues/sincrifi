# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:07:40 2020

@author: jorge
Converte o arquivo de bancos 
"""


_INPUT_PATH_ = "C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_OUTPUT_PATH = "C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_CASO_PREFIX_ = "001-MPF-000001-18"

class Agencia:
    def __init__(self):
        self.NUMERO_BANCO = "" #numero de 3
        self.NUMERO_AGENCIA = "" #numero de 4
        self.NOME_AGENCIA = "" #texto 50
        self.ENDERECO_LOGRADOURO = "" #texto 80
        self.ENDERECO_CIDADE = "" #texto 40
        self.ENDERECO_UF = "" #texto 2
        self.ENDERECO_PAIS = "" #texto 40
        self.ENDERECO_CEP = "" #texto 8
        self.TELEFONE_AGENCIA = "" #texto 20
        self.DATA_ABERTURA_AGENCIA = "" #data 8
        self.DATA_FECHAMENTO_AGENCIA = "" #data 8
        
        
class Agencias:
    def __init__(self, input_path, output_path, caso_prefix):
        agencia = []
        self.input_path = input_path
        self.output_path = output_path 
        self.caso_prefix = caso_prefix
        
        
        
    def convertToCsv(self):
        file = open(self.input_path+"/"+self.caso_prefix+"/"+self.caso_prefix+"_AGENCIAS.TXT")
        
                
        content = "NUMERO_BANCO;NUMERO_AGENCIA;NOME_AGENCIA;ENDERECO_LOGRADOURO;ENDERECO_CIDADE;ENDERECO_UF;ENDERECO_PAIS;ENDERECO_CEP;TELEFONE_AGENCIA;DATA_ABERTURA_AGENCIA;DATA_FECHAMENTO_AGENCIA\n"
        content += file.read()
        
        #fecha o arquivo CONTAS
        file.close()
        
        #cria o arquivo csv
        file = open(self.output_path+"/"+self.caso_prefix+"/"+self.caso_prefix+"_"+"AGENCIAS.csv", "w+")
        
        #escreve no arquivo csv
        file.write(content.replace("\t", ";"))
        
        #fecha o arquivo criado
        file.close()
        
        
def main():
   caso01 = Agencias(_INPUT_PATH_,_OUTPUT_PATH,_CASO_PREFIX_)
   
   caso01.convertToCsv()
    
if __name__ == "__main__":
    main()
        