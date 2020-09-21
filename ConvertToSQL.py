# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 20:58:56 2020

@author: jorge

Cria script para SqlServer
"""
_INPUT_PATH_ = '' #"C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_OUTPUT_PATH_ = '' #"C:/Users/jorge/Desktop/tcc/official/sincrifi/conversao/teste"
_CASO_PREFIX_ = ''# "001-MPF-000001-18"

#classe que contém a definição de cada linha do arquivo CONTAS
class Conta:
    def __init__(self):
        self.NUMERO_BANCO = ""            #numerico de 3
        self.NUMERO_AGENCIA = ""          #numerico de 4
        self.NUMERO_CONTA = ""            #texto de 20
        self.TIPO_CONTA = ""              #numerico de 1
        self.DATA_ABERTURA_CONTA = ""     #data 8
        self.DATA_ENCERRAMENTO_CONTA = "" #data 8
        self.MOVIMENTACAO_CONTA = ""      #numerico de 1

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
        

   
def convertToSqlServer():
    #ORIGEM DESTINO
    origemDesetino = []
    
    file = open(_INPUT_PATH_+"/"+"/"+_CASO_PREFIX_+"_ORIGEM_DESTINO.TXT", "r")
        
    for line in file.read().split("\n"):
        columns = line.split("\t")
        
        if len(columns) == 1:
            continue
        
        o = OrigemDestino()
        
        if  columns[0]:
            o.CODIGO_CHAVE_OD = columns[0]
        else:
            o.CODIGO_CHAVE_OD =""

        if  columns[1]:
            o.CODIGO_CHAVE_EXTRATO = columns[1]
        else:
            o.CODIGO_CHAVE_EXTRATO = ""

        if  columns[2]:
            o.VALOR_TRANSACAO = columns[2]
        else:
            o.VALOR_TRANSACAO = ""

        if  columns[3]:
            o.NUMERO_DOCUMENTO_TRANSACAO = columns[3]
        else:
            o.NUMERO_DOCUMENTO_TRANSACAO = ""

        if  columns[4]:
            o.NUMERO_BANCO_OD = columns[4]
        else:
            o.NUMERO_BANCO_OD = ""

        if  columns[5]:
            o.NUMERO_AGENCIA_OD = columns[5]
        else:
            o.NUMERO_AGENCIA_OD = ""

        if  columns[6]:
            o.NUMERO_CONTA_OD = columns[6]
        else:
            o.NUMERO_CONTA_OD = ""

        if  columns[7]:
            o.TIPO_CONTA_OD = columns[7]
        else:
            o.TIPO_CONTA_OD = ""

        if  columns[8]:
            o.TIPO_PESSOA_OD = columns[8]
        else:
            o.TIPO_PESSOA_OD =""

        if  columns[9]:
            o.CPF_CNPJ_OD = columns[9]
        else:
            o.CPF_CNPJ_OD = ""

        if  columns[10]:
            o.NOME_PESSOA_OD = columns[10]
        else: 
            o.NOME_PESSOA_OD =""

        if  columns[11]:
            o.NOME_DOC_IDENTIFICACAO_OD = columns[11]
        else:
            o.NOME_DOC_IDENTIFICACAO_OD = ""

        if  columns[12]:
            o.NUMERO_DOC_IDENTIFICACAO_OD = columns[12]
        else:
            o.NUMERO_DOC_IDENTIFICACAO_OD = ""

        if  columns[13]:
            o.CODIGO_DE_BARRAS = columns[13]
        else:
            o.CODIGO_DE_BARRAS = ""

        if  columns[14]:
            o.NOME_ENDOSSANTE_CHEQUE = columns[14]
        else:
            o.NOME_ENDOSSANTE_CHEQUE = ""

        if  columns[15]:
            o.DOC_ENDOSSANTE_CHEQUE = columns[15]
        else:
            o.DOC_ENDOSSANTE_CHEQUE =""

        if  columns[16]:
            o.SITUACAO_IDENTIFICACAO = columns[16]
        else:
            o.SITUACAO_IDENTIFICACAO = ""

        if  columns[17]:
            o.OBSERVACÃO = columns[17]
        else:
            o.OBSERVACÃO = ""

        origemDesetino.append(o)

    file.close()
    
    #Extrato
    extrato = []

    file = open(_INPUT_PATH_+"/"+"/"+_CASO_PREFIX_+"_EXTRATO.TXT")

    for line in file.read().split("\n"):
        columns = line.split("\t")
        
        if len(columns) == 1:
            continue

        e = Extrato()

        if  columns[0]:
            e.CODIGO_CHAVE_EXTRATO = columns[0]
        else:
            e.CODIGO_CHAVE_EXTRATO = ""

        if  columns[1]:
            e.NUMERO_BANCO = columns[1]
        else:
            e.NUMERO_BANCO = ""

        if  columns[2]:
            e.NUMERO_AGENCIA = columns[2]
        else:
            e.NUMERO_AGENCIA = ""

        if  columns[3]:
            e.NUMERO_CONTA = columns[3]
        else:
            e.NUMERO_CONTA = ""

        if  columns[4]:
            e.TIPO_CONTA = columns[4]
        else:
            e.TIPO_CONTA = ""

        if  columns[5]:
            e.DATA_LANCAMENTO = columns[5]
        else:
            e.DATA_LANCAMENTO = ""

        if  columns[6]:
            e.NUMERO_DOCUMENTO = columns[6]
        else:
            e.NUMERO_DOCUMENTO = ""

        if  columns[7]:
            e.DESCRICAO_LANCAMENTO = columns[7]
        else:
            e.DESCRICAO_LANCAMENTO = ""

        if  columns[8]:
            e.TIPO_LANCAMENTO = columns[8]
        else:
            e.TIPO_LANCAMENTO = ""

        if  columns[9]:
            e.VALOR_LANCAMENTO = columns[9]
        else:
            e.VALOR_LANCAMENTO = ""

        if  columns[10]:
            e.NATUREZA_LANCAMENTO = columns[10]
        else:
            e.NATUREZA_LANCAMENTO = ""

        if  columns[11]:
            e.VALOR_SALDO = columns[11]
        else:
            e.VALOR_SALDO = ""

        if  columns[12]:
            e.NATUREZA_SALDO = columns[12]
        else:
            e.NATUREZA_SALDO = ""

        if  columns[13]:
            e.LOCAL_TRANSACAO = columns[13]
        else:
            e.LOCAL_TRANSACAO = ""

        extrato.append(e)

    file.close()

    #Titular

    titular = []

    file = open(_INPUT_PATH_+"/"+"/"+_CASO_PREFIX_+"_TITULARES.TXT")

    for line in file.read().split("\n"):
        columns = line.split("\t")
        
        if len(columns) == 1:
            continue

        t = Titular()

        if  columns[0]:
            t.NUMERO_BANCO = columns[0]
        else:
            t.NUMERO_BANCO = ""

        if  columns[1]:
            t.NUMERO_AGENCIA = columns[1]
        else:
            t.NUMERO_AGENCIA = ""

        if  columns[2]:
            t.NUMERO_CONTA = columns[2]
        else:
            t.NUMERO_CONTA = ""

        if  columns[3]:
            t.TIPO_CONTA = columns[3]
        else:
            t.TIPO_CONTA = ""

        if  columns[4]:
            t.TIPO_TITULAR = columns[4]
        else:
            t.TIPO_TITULAR = ""

        if  columns[5]:
            t.PESSOA_INVESTIGADA = columns[5]
        else:
            t.PESSOA_INVESTIGADA = ""

        if  columns[6]:
            t.TIPO_PESSOA_TITULAR = columns[6]
        else:
            t.TIPO_PESSOA_TITULAR = ""

        if  columns[7]:
            t.CPF_CNPJ_TITULAR = columns[7]
        else:
            t.CPF_CNPJ_TITULAR = ""

        if  columns[8]:
            t.NOME_TITULAR = columns[8]
        else:
            t.NOME_TITULAR = ""

        if  columns[9]:
            t.NOME_DOC_IDENTIFICACAO = columns[9]
        else:
            t.NOME_DOC_IDENTIFICACAO = ""

        if  columns[10]:
            t.NUMERO_DOC_IDENTIFICACAO = columns[10]
        else:
            t.NUMERO_DOC_IDENTIFICACAO = ""
            
        if  columns[11]:
            t.ENDERECO_LOGRADOURO = columns[11]
        else:
            t.ENDERECO_LOGRADOURO = ""

        if  columns[12]:
            t.ENDERECO_CIDADE = columns[12]
        else:
            t.ENDERECO_CIDADE = ""

        if  columns[13]:
            t.ENDERECO_UF = columns[13]
        else:
            t.ENDERECO_UF = ""

        if  columns[14]:
            t.ENDERECO_PAIS = columns[14]
        else:
            t.ENDERECO_PAIS = ""

        if  columns[15]:
            t.ENDERECO_CEP = columns[15]
        else:
            t.ENDERECO_CEP = ""

        if  columns[16]:
            t.TELEFONE_PESSOA = columns[16]
        else:
            t.TELEFONE_PESSOA = ""

        if  columns[17]:
            t.VALOR_RENDA = columns[17]
        else:
            t.VALOR_RENDA = ""

        if  columns[18]:
            t.DATA_ATUALIZACAO_RENDA = columns[18]
        else:
            t.DATA_ATUALIZACAO_RENDA = ""

        if  columns[19]:
            t.DATA_INICIO_RELACIONAMENTO  = columns[19]
        else:
            t.DATA_INICIO_RELACIONAMENTO  = ""

        if  columns[20]:
            t.DATA_FIM_RELACIONAMENTO = columns[20]
        else:
            t.DATA_FIM_RELACIONAMENTO = ""
        
        titular.append(t)

    file.close()

    #Agencia

    agencia = []

    file = open(_INPUT_PATH_+"/"+"/"+_CASO_PREFIX_+"_AGENCIAS.TXT")

    for line in file.read().split("\n"):
        columns = line.split("\t")
        
        if len(columns) == 1:
            continue

        a = Agencia()

        if  columns[0]:
            a.NUMERO_BANCO = columns[0]
        else:
            a.NUMERO_BANCO = "" 
            
        if  columns[1]:
            a.NUMERO_AGENCIA = columns[1]
        else:
            a.NUMERO_AGENCIA = "" 
            
        if  columns[2]:
            a.NOME_AGENCIA = columns[2]
        else:
            a.NOME_AGENCIA = "" 
            
        if  columns[3]:
            a.ENDERECO_LOGRADOURO = columns[3]
        else:
            a.ENDERECO_LOGRADOURO = ""
            
        if  columns[4]:
            a.ENDERECO_CIDADE = columns[4]
        else:
            a.ENDERECO_CIDADE = "" 
            
        if  columns[5]:
            a.ENDERECO_UF = columns[5]
        else:
            a.ENDERECO_UF = ""
            
        if  columns[6]:
            a.ENDERECO_PAIS = columns[6]
        else:
            a.ENDERECO_PAIS = "" 
            
        if  columns[7]:
            a.ENDERECO_CEP = columns[7]
        else:
            a.ENDERECO_CEP = "" 
            
        if  columns[8]:
            a.TELEFONE_AGENCIA = columns[8]
        else:
            a.TELEFONE_AGENCIA = "" 
            
        if  columns[9]:
            a.DATA_ABERTURA_AGENCIA = columns[9]
        else:
            a.DATA_ABERTURA_AGENCIA = "" 
            
        if  columns[10]:
            a.DATA_FECHAMENTO_AGENCIA = columns[10]
        else:
            a.DATA_FECHAMENTO_AGENCIA = "" 
            

        agencia.append(a)
    
    file.close()

    #Conta 
    conta = []

    file = open(_INPUT_PATH_+"/"+"/"+_CASO_PREFIX_+"_CONTAS.TXT", "r")
    
    for line in file.read().split("\n"):
        columns = line.split('\t')
        
        if len(columns) == 1:
            continue

        c = Conta()

        if  columns[0]:
            c.NUMERO_BANCO = columns[0]
        else:
            c.NUMERO_BANCO = ""           

        if  columns[1]:
            c.NUMERO_AGENCIA = columns[1]
        else:
            c.NUMERO_AGENCIA = ""         

        if  columns[2]:
            c.NUMERO_CONTA = columns[2]
        else:
            c.NUMERO_CONTA = ""           

        if  columns[3]:
            c.TIPO_CONTA = columns[3]
        else:
            c.TIPO_CONTA = ""             

        if  columns[4]:
            c.DATA_ABERTURA_CONTA = columns[4]
        else:
            c.DATA_ABERTURA_CONTA = ""    

        if  columns[5]:
            c.DATA_ENCERRAMENTO_CONTA = columns[5]
        else:
            c.DATA_ENCERRAMENTO_CONTA = ""

        if  columns[6]:
            c.MOVIMENTACAO_CONTA = columns[6]
        else:
            c.MOVIMENTACAO_CONTA = ""     

        conta.append(c)

    file.close()

    #ORIGEM_DESTINO
    sql = ""
    sql += "INSERT INTO ORIGEM_DESTINO\nVALUES\n"

    for row in origemDesetino:
        sql += "(" +  row.CODIGO_CHAVE_OD + ","
        sql += row.CODIGO_CHAVE_EXTRATO + "," if row.CODIGO_CHAVE_EXTRATO else "0,"
        sql += row.VALOR_TRANSACAO.replace(",", ".") + "," if row.VALOR_TRANSACAO else "0,"
        sql += "'" + row.NUMERO_DOCUMENTO_TRANSACAO + "'," 
        sql += row.NUMERO_BANCO_OD + ","  if row.NUMERO_BANCO_OD else "0,"
        sql += row.NUMERO_AGENCIA_OD + "," if row.NUMERO_AGENCIA_OD else "0,"
        sql += "'" + row.NUMERO_CONTA_OD  + "',"
        sql += row.TIPO_CONTA_OD + "," if row.TIPO_CONTA_OD else "0,"
        sql += row.TIPO_PESSOA_OD  + "," if row.TIPO_PESSOA_OD else "0,"
        sql += row.CPF_CNPJ_OD + "," if row.CPF_CNPJ_OD else "0,"
        sql += ("'" + row.NOME_PESSOA_OD + "'," +
            "'" + row.NOME_DOC_IDENTIFICACAO_OD + "',"+
            "'" + row.NUMERO_DOC_IDENTIFICACAO_OD + "'," +
            "'" + row.CODIGO_DE_BARRAS + "'," +
            "'" + row.NOME_ENDOSSANTE_CHEQUE + "'," +
            "'" + row.DOC_ENDOSSANTE_CHEQUE + "'," +
            "'" + row.SITUACAO_IDENTIFICACAO + "'," +
            "'" + row.OBSERVACÃO + "'),\n")

    #remove a virular que sobra 
    sql = sql[:-2]
    sql += ";"

    #EXTRATO
    
    sql += "\n\nINSERT INTO EXTRATO \nVALUES\n"
    
    for row in extrato:
        sql += "(" 
        sql += row.CODIGO_CHAVE_EXTRATO  + "," if row.CODIGO_CHAVE_EXTRATO else "0,"
        sql += row.NUMERO_BANCO  + "," if row.NUMERO_BANCO else "0,"
        sql += row.NUMERO_AGENCIA  + "," if row.NUMERO_AGENCIA else "0,"
        sql += "'" + row.NUMERO_CONTA  + "'," 
        sql += row.TIPO_CONTA  + "," if row.TIPO_CONTA else "0,"
        sql += "convert(date,'" + row.DATA_LANCAMENTO[4:]+'-'+row.DATA_LANCAMENTO[2:4]+'-'+row.DATA_LANCAMENTO[:2] + "')," if row.DATA_LANCAMENTO else "null,"
        sql += "'" + row.NUMERO_DOCUMENTO  + "'," 
        sql += "'" + row.DESCRICAO_LANCAMENTO  + "'," 
        sql += row.TIPO_LANCAMENTO  + "," if row.TIPO_LANCAMENTO else "0,"
        sql += row.VALOR_LANCAMENTO[:-2]+'.'+row.VALOR_LANCAMENTO[-2:]  + "," if row.VALOR_LANCAMENTO else "0,"
        sql += "'" + row.NATUREZA_LANCAMENTO  + "'," 
        sql += row.VALOR_SALDO[:-2]+'.'+row.VALOR_SALDO[-2:]  + "," if row.VALOR_SALDO else "0,"
        sql += "'" + row.NATUREZA_SALDO  + "'," 
        sql += "'" + row.LOCAL_TRANSACAO  + "'),\n" 

    #remove a ultima virgula
    sql = sql[:-2]
    sql += ";"

    #Titular:

    sql += "\n\nINSERT INTO TITULARES \nVALUES\n"

    for row in titular:
        sql += "(" 
        sql += row.NUMERO_BANCO + "," if row.NUMERO_BANCO else "0,"
        sql += row.NUMERO_AGENCIA + "," if row.NUMERO_AGENCIA else "0,"
        sql += "'" + row.NUMERO_CONTA + "',"
        sql += row.TIPO_CONTA + "," if row.TIPO_CONTA else "0,"
        sql += "'" + row.TIPO_TITULAR + "',"
        sql += row.PESSOA_INVESTIGADA + "," if row.PESSOA_INVESTIGADA else "0,"
        sql += row.TIPO_PESSOA_TITULAR + "," if row.TIPO_PESSOA_TITULAR else "0,"
        sql += row.CPF_CNPJ_TITULAR + "," if row.CPF_CNPJ_TITULAR else "0,"
        sql += ("'" + row.NOME_TITULAR + "'," +
            "'" + row.NOME_DOC_IDENTIFICACAO + "'," +
            "'" + row.NUMERO_DOC_IDENTIFICACAO + "'," +
            "'" + row.ENDERECO_LOGRADOURO + "'," + 
            "'" + row.ENDERECO_CIDADE + "'," + 
            "'" + row.ENDERECO_UF + "'," +
            "'" + row.ENDERECO_PAIS + "'," +
            "'" + row.ENDERECO_CEP + "'," +
            "'" + row.TELEFONE_PESSOA + "'," )
        sql += row.VALOR_RENDA.replace(",", ".") + "," if row.VALOR_RENDA else "0,"
        
        
        sql += "convert(date,'" + row.DATA_ATUALIZACAO_RENDA[4:]+'-'+row.DATA_ATUALIZACAO_RENDA[2:4]+'-'+row.DATA_ATUALIZACAO_RENDA[:2] + "')," if row.DATA_ATUALIZACAO_RENDA else "null,"
        sql += "convert(date,'" + row.DATA_INICIO_RELACIONAMENTO[4:]+'-'+row.DATA_INICIO_RELACIONAMENTO[2:4]+'-'+row.DATA_INICIO_RELACIONAMENTO[:2]  + "')," if row.DATA_INICIO_RELACIONAMENTO else "null,"
        sql += "convert(date,'" + row.DATA_FIM_RELACIONAMENTO[4:]+'-'+row.DATA_FIM_RELACIONAMENTO[2:4]+'-'+row.DATA_FIM_RELACIONAMENTO[:2] + "'))," if row.DATA_FIM_RELACIONAMENTO else "null),\n"
    
    sql = sql[:-2]
    sql += ";"

    #CONTA:
    sql += "\n\nINSERT INTO CONTAS \nVALUES\n"

    for row in conta:
        sql += "("
        sql += row.NUMERO_BANCO + "," if row.NUMERO_BANCO else "0,"
        sql += row.NUMERO_AGENCIA + "," if row.NUMERO_AGENCIA else "0,"
        sql += "'" + row.NUMERO_CONTA + "',"
        sql += row.TIPO_CONTA + "," if row.TIPO_CONTA else "0,"
        sql += "convert(date,'" + row.DATA_ABERTURA_CONTA[4:]+'-'+row.DATA_ABERTURA_CONTA[2:4]+'-'+row.DATA_ABERTURA_CONTA[:2] + "')," if row.DATA_ABERTURA_CONTA else "null,"
        sql += "convert(date, '" + row.DATA_ENCERRAMENTO_CONTA[4:]+'-'+row.DATA_ENCERRAMENTO_CONTA[2:4]+'-'+row.DATA_ENCERRAMENTO_CONTA[:2] + "')," if row.DATA_ENCERRAMENTO_CONTA else "null,"
        sql += row.MOVIMENTACAO_CONTA + "),\n"

    sql = sql[:-2]
    sql += ";"

    #Agencia
    sql += "\n\nINSERT INTO AGENCIAS \nVALUES\n"
    for row in agencia:
        sql += "("
        sql += row.NUMERO_BANCO + "," if row.NUMERO_BANCO else "0," #numero de 3
        sql += row.NUMERO_AGENCIA + "," if row.NUMERO_AGENCIA else "0," #numero de 4
        sql += ("'" + row.NOME_AGENCIA + "'," + #texto 50
            "'" + row.ENDERECO_LOGRADOURO + "'," + #texto 80
            "'" + row.ENDERECO_CIDADE + "'," + #texto 40
            "'" + row.ENDERECO_UF + "'," + #texto 2
            "'" + row.ENDERECO_PAIS + "'," + #texto 40
            "'" + row.ENDERECO_CEP + "'," + #texto 8
            "'" + row.TELEFONE_AGENCIA + "',") #texto 20
        sql += "convert(date, '" + row.DATA_ABERTURA_AGENCIA[4:]+'-'+row.DATA_ABERTURA_AGENCIA[2:4]+'-'+row.DATA_ABERTURA_AGENCIA[:2] + "')," if row.DATA_ABERTURA_AGENCIA else "null," #data 8
        sql += "convert(date, '" + row.DATA_FECHAMENTO_AGENCIA[4:]+'-'+row.DATA_FECHAMENTO_AGENCIA[2:4]+'-'+row.DATA_FECHAMENTO_AGENCIA[:2] + "'))," if row.DATA_FECHAMENTO_AGENCIA else "null),\n" #data 8


    sql = sql[:-2]
    sql += ";"


    #file = open(_OUTPUT_PATH_+'/'+_CASO_PREFIX_+'/'+_CASO_PREFIX_+"_DATA.sql", "w+")

    #file.close()

    return sql




def startConvertions(inp, output, prefix):
    try:
        global _INPUT_PATH_
        global _OUTPUT_PATH_
        global _CASO_PREFIX_

        _INPUT_PATH_ = inp
        _OUTPUT_PATH_ = output
        _CASO_PREFIX_ = prefix

        sql = convertToSqlServer()
        
        #monta o arquivo completo
        file = open(_OUTPUT_PATH_ +'/' + "SINCRIFI_DATABASE.sql", "w+")
        file.write(sql)

        return True
    except:
        return False
        
    