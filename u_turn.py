import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pyodbc
import networkx as nx
from plotly.graph_objs import *
import chart_studio.plotly as py
import plotly.express as px
import webbrowser
from threading import Timer
import plotly.offline as pyo
import datetime

pyo.init_notebook_mode()

#app configuration
# parameters
DB = {'servername': 'JORGE-NT\SQLEXPRESS',
      'database': 'SINCRIFI'}

# create the connection
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + DB['servername'] + ';DATABASE=' + DB['database'] + ';User Id=admin;Password=admin;Trusted_Connection=yes')

#IDENTIFICA TRANSAÇÕES U-TURN INDIVIDUAIS
df_transacoes = pd.read_sql(""" SELECT 
                            o.CODIGO_CHAVE_EXTRATO, 
                            CONVERT(INT, e.TIPO_LANCAMENTO) AS TIPO_LANCAMENTO, 
                            CONVERT(CHAR, e.DATA_LANCAMENTO, 103) AS DATA_LANCAMENTO,
                            CONVERT(CHAR, o.VALOR_TRANSACAO) AS VALOR_TRANSACAO,
                            CONVERT(CHAR, e.NUMERO_BANCO) AS NUMERO_BANCO, 
                            CONVERT(CHAR, e.NUMERO_AGENCIA) AS NUMERO_AGENCIA, 
                            CONVERT(CHAR, e.NUMERO_CONTA) AS NUMERO_CONTA,
                            t.NOME_TITULAR,
                            CONVERT(CHAR, o.NUMERO_BANCO_OD) AS NUMERO_BANCO_OD, 
                            CONVERT(CHAR, o.NUMERO_AGENCIA_OD) AS NUMERO_AGENCIA_OD, 
                            CONVERT(CHAR, o.NUMERO_CONTA_OD) AS NUMERO_CONTA_OD, 
                            CONVERT(CHAR, o.NOME_PESSOA_OD) AS NOME_PESSOA_OD 
                            FROM EXTRATO e
                            INNER JOIN ORIGEM_DESTINO o ON e.CODIGO_CHAVE_EXTRATO = o.CODIGO_CHAVE_EXTRATO
                            INNER JOIN TITULARES t ON e.NUMERO_BANCO = t.NUMERO_BANCO AND e.NUMERO_AGENCIA = t.NUMERO_AGENCIA  
                            AND e.NUMERO_CONTA = t.NUMERO_CONTA
                            ORDER BY e.DATA_LANCAMENTO
                    """,conn)


df_transacoes['used'] = 0

#cria o DF que irá armazenar o par de transações u-turn
df_uturn = pd.DataFrame(columns=['id', 'conta_origem', 'conta_destino', 'valor', 'tipo', 'descricao', 'data'])

count = 1
for ia, transacao in df_transacoes.iterrows():
    #verifica se esta transação já foi utilizada
    if(transacao['used'] == 1):
        continue

    valor = transacao['VALOR_TRANSACAO']
    tipo_transacao = transacao['TIPO_LANCAMENTO']
    df_transacoes.loc[ia, 'used'] = 1
    
    for ib, b in df_transacoes.iterrows():
        #mesmo objetivo da verificaçao anterior
        if(b['used'] == 1):
            continue
            
        #se for uma transação de Débito e a transação verificada também for
        if(tipo_transacao < 200):
            if(b['TIPO_LANCAMENTO'] < 200):
                continue
        else:#se a transação for de Crédito e a verificada também for 
            if(b['TIPO_LANCAMENTO'] > 200):
                continue
        
        #se chegou aqui significa que há uma transação de Débito e outra de Crédito
        if(valor == b['VALOR_TRANSACAO']):
            #se houver uma transações u-turn então cria 2 registros para identifica-las no grafo
            
            #busca o nome do tipo de lançamento
            nome_lancamento = pd.read_sql("""SELECT DESCRICAO 
                                             FROM TIPO_LANCAMENTO 
                                             WHERE CODIGO = """ + str(tipo_transacao), conn)
            
            dt_lancamento_b = pd.read_sql(""" SELECT CONVERT(CHAR, e.DATA_LANCAMENTO, 103) AS DATA_LANCAMENTO 
                                          FROM ORIGEM_DESTINO o 
                                          INNER JOIN EXTRATO e ON e.CODIGO_CHAVE_EXTRATO = o.CODIGO_CHAVE_EXTRATO 
                                          WHERE o.CODIGO_CHAVE_EXTRATO = """ + str(b['CODIGO_CHAVE_EXTRATO']).strip(), conn)
            conta_a = str(transacao['NUMERO_BANCO']).strip() + '/' + str(transacao['NUMERO_AGENCIA']).strip() + '/' + str(transacao['NUMERO_CONTA']).strip()
            conta_b = str(b['NUMERO_BANCO_OD']).strip() + '/' + str(b['NUMERO_AGENCIA_OD']).strip() + '/' + str(b['NUMERO_CONTA_OD']).strip()
            
            #lancamento 1
            df_uturn = df_uturn.append({
                'id' : count,
                'conta_origem' : conta_a if tipo_transacao < 200 else conta_b,
                'conta_destino' : conta_b if tipo_transacao < 200 else conta_a, 
                'valor' : valor,
                'tipo' : transacao['TIPO_LANCAMENTO'],
                'descricao' : nome_lancamento.loc[0, 'DESCRICAO'],
                'data' : transacao['DATA_LANCAMENTO'] if tipo_transacao < 200 else dt_lancamento_b.loc[0, 'DATA_LANCAMENTO']
            }, ignore_index=True)
            
             #lancamento 2
            df_uturn = df_uturn.append({
                 'id' : count,
                 'conta_origem' : conta_a if tipo_transacao > 200 else conta_b,
                 'conta_destino' : conta_b if tipo_transacao > 200 else conta_a, 
                 'valor' : valor,
                 'tipo' : transacao['TIPO_LANCAMENTO'],
                 'descricao' : nome_lancamento.loc[0, 'DESCRICAO'],
                 'data' : transacao['DATA_LANCAMENTO'] if tipo_transacao > 200 else dt_lancamento_b.loc[0, 'DATA_LANCAMENTO']
             }, ignore_index=True)
                      
            #marca os registro atuais como usados para não serem computados novamente

            #marca os registro atuais como usados para não serem computados novamente
            df_transacoes.loc[ib, 'used'] = 1
                                 
            
            count += 1
                                 
            #fecha o loop atual
            break
        
G=nx.Graph()

#lista os nodos
nodes = []
for row in df_uturn['conta_origem']:
    if row not in nodes:
        nodes.append(row)
        
for row in df_uturn['conta_destino']:
    if row not in nodes:
        nodes.append(row)

G.add_nodes_from(nodes)        
        

usedId = []#previne a inserção da mesma relação duas vezes
edgesText = []
for id, row in df_uturn.iterrows():
    if row['id'] not in usedId:
        G.add_edge(row['conta_origem'], row['conta_destino'], text=row['id'])
        usedId.append(row['id'])
        str1 = str(row['data']).strip()
        str2 = str(df_uturn.loc[id+1, 'data']).strip()
        
        d1 = datetime.datetime.strptime(str1, '%d/%m/%Y')
        d2 = datetime.datetime.strptime(str2, '%d/%m/%Y')
        if(d1 > d2):
            edgesText.append(
            f"""
            Data: { row['data'] } 
            <br>
            Conta: { row['conta_origem'] if row['tipo'] < 200 else row['conta_destino'] } para Conta: { row['conta_origem'] if row['tipo'] > 200 else row['conta_destino']}
            <br>
            Valor: R${ '%.2f' % float(row['valor']) }
            <br>
            ----------------------------
            <br>
            Data: {  df_uturn.loc[id+1, 'data'] }
            <br>
            Conta: { df_uturn.loc[id+1,'conta_origem'] if row['tipo'] < 200 else df_uturn.loc[id+1,'conta_destino'] } para Conta: { df_uturn.iloc[id+1]['conta_origem'] if row['tipo'] > 200 else df_uturn.iloc[id+1]['conta_destino'] }
            <br>
            Valor: R${ '%.2f' % float(row['valor']) }
            """
            )
        else:
             edgesText.append(
            f"""
            Data: {  df_uturn.loc[id+1, 'data'] }
            <br>
            Conta: { df_uturn.loc[id+1,'conta_origem'] if row['tipo'] < 200 else df_uturn.loc[id+1,'conta_destino'] } para Conta: { df_uturn.iloc[id+1]['conta_origem'] if row['tipo'] > 200 else df_uturn.iloc[id+1]['conta_destino'] }
            <br>
            Valor: R${ '%.2f' % float(row['valor']) }
            <br>
            ----------------------------
            <br>
            Data: { row['data'] } 
            <br>
            Conta: { row['conta_origem'] if row['tipo'] < 200 else row['conta_destino'] } para Conta: { row['conta_origem'] if row['tipo'] > 200 else row['conta_destino']}
            <br>
            Valor: R${ '%.2f' % float(row['valor']) }
            """
            )
pos=nx.fruchterman_reingold_layout(G)


node_x=[pos[k][0] for k in nodes]
node_y=[pos[k][1] for k in nodes]

#posiçãos das edges
edge_x=[]
edge_y=[]
texto_x = []
texto_y = []
for id, edge in df_uturn.iterrows():
    if(id % 2 == 0):
        continue
        
    x = [pos[edge['conta_origem']][0],pos[edge['conta_destino']][0], None]
    y = [pos[edge['conta_origem']][1],pos[edge['conta_destino']][1], None]
    edge_x += x
    edge_y += y
    #encontra o ponto médio entre dois nodos para aprensentar as informações da linha
    texto_x += [((x[0] + x[1]) / 2)]
    texto_y += [((y[0] + y[1]) / 2)]
    
edge_trace = Scatter(
    x=edge_x, y=edge_y,
    mode='lines',
    line=dict(width=0.5, color='#888'),
    #hoverinfo='text',
    #hovertext=edgesText
    )
        

node_trace = Scatter(
    x=node_x, y=node_y,
   mode='markers',
               name='agência/conta',
               marker=dict(symbol='circle-dot',
                             size=40,
                             color='#FFF',
                             line=dict(color='#000', width=0.1)
                             ),
               text=nodes,
               hovertemplate='%{text}',
                showlegend = False
            )

text_trace = Scatter(
              x=texto_x,y=texto_y, 
               mode='markers',
               name='',
               marker=dict(symbol='circle-dot',
                             size=12,
                             color='#FFF',
                             line=dict(color='#000', width=0.1)
                             ),
               text=edgesText,
                hoverinfo='text'
             )
    

fig = Figure(data=[edge_trace, node_trace, text_trace],
             layout=Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

fig.show()