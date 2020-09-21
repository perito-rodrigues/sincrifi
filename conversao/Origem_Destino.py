# -*- coding: utf-8 -*-
"""
Created on Thu May  7 15:38:49 2020

@author: jorge
"""
_INPUT_PATH_ = "C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_OUTPUT_PATH = "C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_CASO_PREFIX_ = "001-MPF-000001-18"

class OrigemDestino:
    def __init__(self):
        self.CODIGO_CHAVE_OD = ""
        self.CODIGO_CHAVE_EXTRATO = ""
        self.VALOR_TRANSACAO = ""
        self.NUMERO_DOCUMENTO_TRANSACAO = ""
        self.NUMERO_BANCO_OD = ""
        self.NUMERO_AGENCIA_OD = ""
        self.NUMERO_CONTA_OD = ""
        self.TIPO_CONTA_OD = ""
        self.TIPO_PESSOA_OD = ""
        self.CPF_CNPJ_OD = ""
        self.NOME_PESSOA_OD = ""
        self.NOME_DOC_IDENTIFICACAO_OD = ""
        self.NUMERO_DOC_IDENTIFICACAO_OD = ""
        self.CODIGO_DE_BARRAS = ""
        self.NOME_ENDOSSANTE_CHEQUE = ""
        self.DOC_ENDOSSANTE_CHEQUE = ""
        self.SITUACAO_IDENTIFICACAO = ""
        self.OBSERVACÃO = ""
        
        
class OrigemDestinos:
    def __init__(self, input_path, output_path, caso_prefix):
        self.input_path = input_path
        self.output_path = output_path 
        self.caso_prefix = caso_prefix
        
        
        
    def convertToCsv(self):
        file = open(self.input_path+"/"+self.caso_prefix+"/"+self.caso_prefix+"_ORIGEM_DESTINO.TXT")
        
                
        content = "CODIGO_CHAVE_OD;CODIGO_CHAVE_EXTRATO;VALOR_TRANSACAO;NUMERO_DOCUMENTO_TRANSACAO;NUMERO_BANCO_OD;NUMERO_AGENCIA_OD;NUMERO_CONTA_OD;TIPO_CONTA_OD;TIPO_PESSOA_OD;CPF_CNPJ_OD;NOME_PESSOA_OD;NOME_DOC_IDENTIFICACAO_OD;NUMERO_DOC_IDENTIFICACAO_OD;CODIGO_DE_BARRAS;NOME_ENDOSSANTE_CHEQUE;DOC_ ENDOSSANTE_CHEQUE;SITUACAO_IDENTIFICACAO;OBSERVACÃO\n"
        content += file.read()
        
        #fecha o arquivo CONTAS
        file.close()
        
        #cria o arquivo csv
        file = open(self.output_path+"/"+self.caso_prefix+"/"+self.caso_prefix+"_ORIGEM_DESTINO.csv", "w+")
        
        #escreve no arquivo csv
        file.write(content.replace("\t", ";"))
        
        #fecha o arquivo criado
        file.close()        

def main():
   caso01 = OrigemDestinos(_INPUT_PATH_,_OUTPUT_PATH,_CASO_PREFIX_)
   
   caso01.convertToCsv()
    
if __name__ == "__main__":
    main()
        

