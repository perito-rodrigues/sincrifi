# -*- coding: utf-8 -*-
"""
Created on Thu May  7 15:04:18 2020

@author: jorge
"""
_INPUT_PATH_ = "C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_OUTPUT_PATH = "C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_CASO_PREFIX_ = "001-MPF-000001-18"

class Titular:
    def __init__(self):
        self.NUMERO_BANCO = ""
        self.NUMERO_AGENCIA = ""
        self.NUMERO_CONTA = ""
        self.TIPO_CONTA = ""
        self.TIPO_TITULAR = ""
        self.PESSOA_INVESTIGADA = ""
        self.TIPO_PESSOA_TITULAR = ""
        self.CPF_CNPJ_TITULAR = ""
        self.NOME_TITULAR = ""
        self.NOME_DOC_IDENTIFICACAO = ""
        self.NUMERO_DOC_IDENTIFICACAO = ""
        self.ENDERECO_LOGRADOURO = ""
        self.ENDERECO_CIDADE = ""
        self.ENDERECO_UF = ""
        self.ENDERECO_PAIS = ""
        self.ENDERECO_CEP = ""
        self.TELEFONE_PESSOA = ""
        self.VALOR_RENDA = ""
        self.DATA_ATUALIZACAO_RENDA = ""
        self.DATA_INICIO_RELACIONAMENTO  = ""
        self.DATA_FIM_RELACIONAMENTO = ""
        
        
class Titulares:
    def __init__(self,input_path,output_path,caso_prefix):
        self.input_path = input_path
        self.output_path = output_path 
        self.caso_prefix = caso_prefix
        
        
        
    def convertToCsv(self):
        file = open(self.input_path+"/"+self.caso_prefix+"/"+self.caso_prefix+"_TITULARES.TXT")
        
                
        content = "NUMERO_BANCO;NUMERO_AGENCIA;NUMERO_CONTA;TIPO_CONTA;TIPO_TITULAR;PESSOA_INVESTIGADA;TIPO_PESSOA_TITULAR;CPF_CNPJ_TITULAR;NOME_TITULAR;NOME_DOC_IDENTIFICACAO;NUMERO_DOC_IDENTIFICACAO;ENDERECO_LOGRADOURO;ENDERECO_CIDADE;ENDERECO_UF;ENDERECO_PAIS;ENDERECO_CEP;TELEFONE_PESSOA;VALOR_RENDA;DATA_ATUALIZACAO_RENDA;DATA_INICIO_RELACIONAMENTO;DATA_FIM_RELACIONAMENTO\n"
        content += file.read()
        
        #fecha o arquivo CONTAS
        file.close()
        
        #cria o arquivo csv
        file = open(self.output_path+"/"+self.caso_prefix+"/"+self.caso_prefix+"_TITULARES.csv", "w+")
        
        #escreve no arquivo csv
        file.write(content.replace("\t", ";"))
        
        #fecha o arquivo criado
        file.close()
        

def main():
   caso01 = Titulares(_INPUT_PATH_,_OUTPUT_PATH,_CASO_PREFIX_)
   
   caso01.convertToCsv()
    
if __name__ == "__main__":
    main()
        