# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:49:16 2020

@author: jorge
"""

_INPUT_PATH_ = "C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_OUTPUT_PATH = "C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_CASO_PREFIX_ = "001-MPF-000001-18"

#classe que contém a definição de cada linha do arquivo CONTAS
class CONTA:
    def __init__(self):
        self.NUMERO_BANCO = ""            #numerico de 3
        self.NUMERO_AGENCIA = ""          #numerico de 4
        self.NUMERO_CONTA = ""            #texto de 20
        self.TIPO_CONTA = ""              #numerico de 1
        self.DATA_ABERTURA_CONTA = ""     #data 8
        self.DATA_ENCERRAMENTO_CONTA = "" #data 8
        self.MOVIMENTACAO_CONTA = ""      #numerico de 1

#realiza as funções para converter o arquivo CONTAS 
class CONTAS:
    def __init__(self, input_path, output_path, caso_prefix):
        self.input_path = input_path
        self.output_path = output_path
        self.caso_prefix = caso_prefix
        
        self.contas = []
        
        self.file = open(self.input_path+'/'+self.caso_prefix+"/"+self.caso_prefix+"_CONTAS.TXT", "r")
        
        content = "NUMERO_BANCO;NUMERO_AGENCIA;NUMERO_CONTA;TIPO_CONTA;DATA_ABERTURA_CONTA;DATA_ENCERRAMENTO_CONTA;MOVIMENTACAO_CONTA\n"
        content += self.file.read()
        
        #fecha o arquivo CONTAS
        self.file.close()
        
        #cria o arquivo csv
        self.file = open(self.output_path+"/"+self.caso_prefix+"/"+self.caso_prefix+"_CONTAS.csv", "w+")
         
        #escreve no arquivo csv
        self.file.write(content.replace("\t", ";"))
        
        #fecha o arquivo criado
        self.file.close()
    
        def objetoContas():
            #lê todo o arquivo de contas e cria o array de Contas
            #TODO: prototipo para transferir para sql    
            for line in self.file:
                
                #divide a linha em tabs
                lineArray = line.split("\t")
    
                conta = CONTA()
                
                if not lineArray[0]:
                    conta.NUMERO_BANCO = ""
                else:
                    conta.NUMERO_BANCO              = lineArray[0]
                    
                if not lineArray[1]:
                     conta.NUMERO_AGENCIA = ""
                else:
                    conta.NUMERO_AGENCIA            = lineArray[1]
                    
                if not lineArray[2]:
                    conta.NUMERO_CONTA = ""
                else:                    
                    conta.NUMERO_CONTA              = lineArray[2]
                
                if not lineArray[3]:
                    conta.TIPO_CONTA = ""
                else:
                    conta.TIPO_CONTA                = lineArray[3]
                    
                if not lineArray[4]:
                    conta.DATA_ABERTURA_CONTA = ""
                else:
                    conta.DATA_ABERTURA_CONTA       = lineArray[4]
                    
                if not lineArray[5]:
                    conta.DATA_ENCERRAMENTO_CONTA = ""
                else:
                    conta.DATA_ENCERRAMENTO_CONTA   = lineArray[5]
                    
                if not lineArray[6]:
                    conta.MOVIMENTACAO_CONTA = ""
                else:
                    conta.MOVIMENTACAO_CONTA        = lineArray[6]
                
                self.contas.append(conta)
            

def main():
   caso01 = CONTAS(_INPUT_PATH_,_OUTPUT_PATH,_CASO_PREFIX_)
    
if __name__ == "__main__":
    main()
        