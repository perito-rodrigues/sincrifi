# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:25:02 2020

@author: jorge
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pyodbc
import networkx as nx
from plotly.graph_objs import *
import chart_studio.plotly as py

DB = {'servername': 'JORGE-NT\SQLEXPRESS',
      'database': 'SINCRIFI'}

# create the connection
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + DB['servername'] + ';DATABASE=' + DB['database'] + ';User Id=admin;Password=admin;Trusted_Connection=yes')

df_grafo_transacoes = pd.read_sql("""
                        SELECT 
                        o.CODIGO_CHAVE_OD,
                        CONVERT(CHAR, e.NUMERO_AGENCIA) AS 'AGENCIA_A', 
                        CONVERT(CHAR, e.NUMERO_CONTA) AS 'CONTA_A',
                        CONVERT(CHAR, o.NUMERO_AGENCIA_OD) AS 'AGENCIA_B', 
                        CONVERT(CHAR, o.NUMERO_CONTA_OD) 'CONTA_B', 
                        e.TIPO_LANCAMENTO,
                        o.VALOR_TRANSACAO,
                        t.DESCRICAO,
                        CONVERT(VARCHAR, e.DATA_LANCAMENTO, 103) AS 'DATA_LANCAMENTO'
                        FROM ORIGEM_DESTINO o
                        INNER JOIN EXTRATO e ON e.CODIGO_CHAVE_EXTRATO = o.CODIGO_CHAVE_EXTRATO
                        INNER JOIN TIPO_LANCAMENTO t ON e.TIPO_LANCAMENTO = t.CODIGO
                        ORDER BY DATA_LANCAMENTO
                                  """,conn)

transacoes = []
#organiza as conexões de acordo com o tipo de operação (Debito, ou Credito)
for  index, transacao in df_grafo_transacoes.iterrows():
    a = ''
    b = ''
    
    if(int(transacao["TIPO_LANCAMENTO"]) > 200):
       a = (transacao['AGENCIA_B'].strip() +'/'+ transacao['CONTA_B'].strip())
       b = (transacao['AGENCIA_A'].strip() +'/'+ transacao['CONTA_A'].strip())
        
    else:
        a = (transacao['AGENCIA_A'].strip()+'/'+transacao['CONTA_A'].strip())
        b = (transacao['AGENCIA_B'].strip()+'/'+transacao['CONTA_B'].strip())
             
    transacoes.append({
        'emissor' : a,
        'destinatario' : b ,
        'valor' : float(transacao['VALOR_TRANSACAO']),
        'tipo' : transacao['DESCRICAO'],
        'data' : transacao['DATA_LANCAMENTO'],
        'id' : transacao['CODIGO_CHAVE_OD']
    })
        
#objeto organizado entre emissario e destinatario


df = pd.DataFrame(transacoes, columns=['emissor', 'destinatario', 'valor', 'tipo', 'data', 'id'])



#obtem o peso e soma as transacoes
emissorDestinatario = df.groupby(['emissor','destinatario']).valor.agg('sum').to_frame('total').reset_index()

emissorDestinatario['peso'] = df.groupby(['emissor','destinatario']).emissor.agg('count').to_frame('count').reset_index()['count']

#cria os links
#soma os valores e os pesos

edges = []
emissorDestinatario['used'] = 0

for  index, transacao in emissorDestinatario.iterrows():
    #se o indice já foi usado pula para o proximo
    if(emissorDestinatario.iloc[index]['used'] == 1):
        continue
        
    #busca outra transação com os mesmo envolvidos no sentido oposto
    atual = emissorDestinatario.query('emissor.str.contains("'+transacao['destinatario']+'") and destinatario.str.contains("'+transacao['emissor']+'")')
    #busca o id para atualizar o status do registro
    id = emissorDestinatario.query('emissor.str.contains("'+transacao['destinatario']+'") and destinatario.str.contains("'+transacao['emissor']+'")').index
    
    if(atual.size == 5):
        total = atual.iloc[0]['total'] + transacao['total']
        peso = atual.iloc[0]['peso'] + transacao['peso']
        
        edges.append({
            'emissor' : atual.iloc[0]['emissor'],
            'destinatario' : atual.iloc[0]['destinatario'] ,
            'valor' : total,
            'peso' : peso
        })
    else:#se não há correspondencias 
        edges.append({
            'emissor' : transacao['emissor'],
            'destinatario' : transacao['destinatario'] ,
            'valor' : transacao['total'],
            'peso' : transacao['peso']
        })
   
    emissorDestinatario.loc[id, 'used'] = 1
    


    






   
