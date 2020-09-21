# -*- coding: utf-8 -*-
"""
Created on Thu May  7 15:12:19 2020

@author: jorge
"""
_INPUT_PATH_ = "C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_OUTPUT_PATH = "C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_CASO_PREFIX_ = "001-MPF-000001-18"


class Extrato:
    def __init__(self):
        self.CODIGO_CHAVE_EXTRATO = ""
        self.NUMERO_BANCO = ""
        self.NUMERO_AGENCIA = ""
        self.NUMERO_CONTA = ""
        self.TIPO_CONTA = ""
        self.DATA_LANCAMENTO = ""
        self.NUMERO_DOCUMENTO = ""
        self.DESCRICAO_LANCAMENTO = ""
        self.TIPO_LANCAMENTO = ""
        self.VALOR_LANCAMENTO = ""
        self.NATUREZA_LANCAMENTO = ""
        self.VALOR_SALDO = ""
        self.NATUREZA_SALDO = ""
        self.LOCAL_TRANSACAO = ""

class Extratos:
    def __init__(self, input_path, output_path, caso_prefix):
        self.input_path = input_path
        self.output_path = output_path 
        self.caso_prefix = caso_prefix
        
        
        
    def convertToCsv(self):
        file = open(self.input_path+"/"+self.caso_prefix+"/"+self.caso_prefix+"_EXTRATO.TXT")
        
                
        content = "CODIGO_CHAVE_EXTRATO;NUMERO_BANCO;NUMERO_AGENCIA;NUMERO_CONTA;TIPO_CONTA;DATA_LANCAMENTO;NUMERO_DOCUMENTO;DESCRICAO_LANCAMENTO;TIPO_LANCAMENTO;VALOR_LANCAMENTO;NATUREZA_LANCAMENTO;VALOR_SALDO;NATUREZA_SALDO;LOCAL_TRANSACAO\n"
        content += file.read()
        
        #fecha o arquivo CONTAS
        file.close()
        
        #cria o arquivo csv
        file = open(self.output_path+"/"+self.caso_prefix+"/"+self.caso_prefix+"_EXTRATO.csv", "w+")
        
        #escreve no arquivo csv
        file.write(content.replace("\t", ";"))
        
        #fecha o arquivo criado
        file.close()
        
def main():
   caso01 = Extratos(_INPUT_PATH_,_OUTPUT_PATH,_CASO_PREFIX_)
   
   caso01.convertToCsv()
    
if __name__ == "__main__":
    main()
        

