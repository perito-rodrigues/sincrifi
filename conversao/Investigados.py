# -*- coding: utf-8 -*-
"""
Created on Thu May  7 14:48:49 2020

@author: jorge
"""
_INPUT_PATH_ = "C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_OUTPUT_PATH = "C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_CASO_PREFIX_ = "001-MPF-000001-18"

class Investigado:
    def __init__(self):
        self.TIPO_PESSOA_OD = "" #numero 1
        self.CPF_CNPJ_OD = "" #numero 14
        self.NOME_PESSOA_OD = "" #texto 80
        self.POSSUI_RELACIONAMENTO = "" #numer 1
        self.POSSUI_CONTA = "" #numer 1
        self.POSSUI_BDV = "" #numer 1
        self.OBSERVACÃO = "" #texto 250
        self.DATA_INICIO_AFASTAMENTO = "" #data 8
        self.DATA_FIM_AFASTAMENTO = "" #data 8

class Investigados:
    def __init__(self, input_path, output_path,caso_prefix):
        self.input_path = input_path
        self.output_path = output_path
        self.caso_prefix = caso_prefix
        

        
    def convertToCsv(self):
        file = open(self.input_path+"/"+self.caso_prefix+"/"+self.caso_prefix+"_INVESTIGADOS.txt")
        
        content = "TIPO_PESSOA_OD;CPF_CNPJ_OD;NOME_PESSOA_OD;POSSUI_RELACIONAMENTO;POSSUI_CONTA;POSSUI_BDV;OBSERVACÃO;DATA_INICIO_AFASTAMENTO;DATA_FIM_AFASTAMENTO;\n"
        content += file.read()
        
        #fecha o arquivo CONTAS
        file.close()
        
        #cria o arquivo csv
        file = open(self.output_path+"/"+self.caso_prefix+"/"+self.caso_prefix+"_INVESTIGADOS.csv", "w+")
        
        #escreve no arquivo csv
        file.write(content.replace("\t", ";"))
        
        #fecha o arquivo criado
        file.close()

def main():
   caso01 = Investigados(_INPUT_PATH_,_OUTPUT_PATH,_CASO_PREFIX_)
   
   caso01.convertToCsv()
    
if __name__ == "__main__":
    main()
        