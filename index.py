import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import networkx as nx
import pandas as pd
import pyodbc
from plotly.graph_objs import *
import plotly.express as px
import webbrowser
from threading import Timer
from SINCRIFI import makeLayout
from ConvertToSQL import startConvertions
from datetime import datetime as dt
import datetime
import json 

#public variables
graphStartDate = ''
graphEndDate = ''

external_stylesheets = ['plotly.css', 'styles.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
app.title = 'SINCRIFI'
index_page = html.Div(
    [

        #metade da esquerda
        html.Div(
            id='main',
            style={'position' : 'absolute', 'left' : '0', 'width' : '50%', 'height' : '100%'},
            children=[
                
                html.Div(
                    style={'width' : '300px', 'height' : '250px', 'position' : 'relative', 'left' : '50%', 'top' : '40%','marginLeft' : '-150px', 'marginTop' : '-125px'},
                    children=[
                        html.H3(
                            style={'textAlign' : 'center'},
                            children='Analisar Caso'
                        ),
                        dcc.Input(
                            style={'width' : '300px'},
                            id="servidor",
                            type='text',
                            value='',
                            placeholder="Servidor SQL Server",
                        ),
                        html.Br(),
                        dcc.Input(
                            style={'marginTop' : '5px', 'width' : '300px' },
                            id="banco",
                            type='text',
                            value='',
                            placeholder="Banco de Dados",
                        ),
                        html.Br(),
                         dcc.Input(
                            style={'marginTop' : '5px', 'width' : '300px' },
                            id="usuario",
                            type='text',
                            value='',
                            placeholder="Usuário",
                        ),
                        html.Br(),
                        dcc.Input(
                            style={'marginTop' : '5px', 'width' : '300px' },
                            id="senha",
                            type='password',
                            value='',
                            placeholder="Senha",
                        ),
                        html.Br(),
                        html.Button(
                            'Analisar',
                            style={'marginTop' : '5px', 'width' : '150px', 'marginLeft' : '75px' },
                            id='analisar',
                            n_clicks=0
                        ),
                        html.Br(),
                        html.Div(id='infoplaceholder', style={'textAlign' : 'center'})
                    ]
                ),
                
            ]

        ),

        html.Div(
            style={'position' : 'absolute', 'left' : '50%', 'top' : '20%' , 'marginLeft' : '-210px', 'width' : '420px'},
            children=[
                html.Img(
                    style={'width' : '300px', 'height' : '250px', 'marginLeft' : '60px' },
                    src='assets/logo.png'
                ),
                html.Label(
                    style={'textAlign' : 'center', 'fontSize' : '16px'}, 
                    children='Sistema de Investigação de Crimes Financeiros'
                )
            ]
        ),
         
        html.Div(
            style={'position' : 'absolute', 'right' : '0', 'width' : '50%', 'height' : '100%'},
            children=[
                html.Div(
                    style={'width' : '300px', 'height' : '250px', 'position' : 'relative', 'left' : '50%', 'top' : '40%','marginLeft' : '-150px', 'marginTop' : '-125px'},
                    children=[
                        html.H3(
                            style={'textAlign' : 'center'},
                            children='Converter Caso'
                        ),
                        html.Br(),
                        dcc.Input(
                            style={'marginTop' : '5px', 'width' : '300px' },
                            id="conversao_prefix",
                            type='text',
                            value='',
                            placeholder="Caso ex: 001-MPF-000001-18",
                        ),
                        html.Br(),
                        dcc.Input(
                            style={'marginTop' : '5px', 'width' : '300px' },
                            id="conversao_entrada",
                            type='text',
                            value='',
                            placeholder="Caminho absoluto da pasta de entrada",
                        ),
                        html.Br(),
                        dcc.Input(
                            style={'marginTop' : '5px', 'width' : '300px' },
                            id="conversao_saida",
                            type='text',
                            value='',
                            placeholder="Caminho absoluto de saída",
                        ),
                        html.Br(),
                        html.Button(
                            'Converter',
                            style={'marginTop' : '5px', 'width' : '150px', 'marginLeft' : '75px' },
                            id='converter',
                            n_clicks=0
                        ),
                        html.Br(),
                        html.Div(id='conversionPlaceholder', style={'textAlign' : 'center'})
                    ]
                ),
            ]
        ),
      
    ]
)

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='layout', children=index_page)
])

servidor = None
banco = None
usuario = None
senha = None

@app.callback(
    Output('conversionPlaceholder', 'children'),
    [Input('converter', 'n_clicks')],
    [State('conversao_prefix', 'value'),
    State('conversao_entrada', 'value'),
    State('conversao_saida', 'value')]
)
def convertFiles(n_clicks, prefix, entrada, saida):
    if(n_clicks> 0):
        if(len(str(prefix).strip()) > 0 and len(str(entrada).strip()) > 0 and len(str(saida).strip()) > 0):
            if(startConvertions(entrada,saida,prefix)):
                return html.Label(style={'color' : 'green'}, children='Conversão bem sucedida!')
            else:
                return html.Label(style={'color' : 'red'}, children='Erro ao converter! \n Verifique se os dados inseridos acimas estão corretos e se todos os arquivos estão presentes e no formato esperado.')
#funções dos callbacks
@app.callback(
    Output('layout', 'children'),
    [Input('analisar', 'n_clicks')],
    [State('servidor', 'value'),
     State('banco', 'value'),
     State('usuario', 'value'),
     State('senha', 'value')]
)
def sqlInput(n_clicks, serv, banc, usua, senh):
    #  DB = {'servername': 'JORGE-NT\SQLEXPRESS',
    #   'database': 'SINCRIFI'}
   
    if(len(str(serv).strip()) > 0 and serv != None):
        if(len(str(banc).strip()) > 0 and banc != None):
            if(len(str(usua).strip()) > 0 and usua != None):
                if(len(str(senh).strip()) > 0 and senh != None):
                    try:
                        # create the connection
                        global servidor
                        global banco
                        global usuario 
                        global senha

                        servidor = serv
                        banco = banc
                        usuario = usua
                        senha = senh

                        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + servidor + ';DATABASE=' + banco + ';UID='+ usuario +';PWD='+senha)
                        
                    except:
                        return html.Label(style={'color' : 'red'}, children='Crendenciais Inválidas')

                    try:
                        pdData = pd.read_sql('SELECT CONVERT(CHAR, MIN(DATA_LANCAMENTO), 103) MINIMA, CONVERT(CHAR, MAX(DATA_LANCAMENTO), 103) AS MAXIMA FROM EXTRATO', conn)
                    except:
                        return html.Label(style={'color' : 'red'}, children='Não está sendo possível executar pesquisas no banco de dados!')
                        
                    try:    
                        return makeLayout(pdData, conn)
                    except Exception as inst:
                        print(type(inst))    # the exception instance
                        print(inst.args)     # arguments stored in .args
                        print(inst)          # __str__ allows args to be printed directly,
                       
                   
    else:
        return index_page            
                    

#gráfico de transações
@app.callback(
    Output('transacoes', 'figure'),
    [Input('transacoesPicker', 'start_date'),
    Input('transacoesPicker', 'end_date')]
)
def transacoes_graph(start, end):

    global servidor
    global banco
    global usuario 
    global senha
    global graphStartDate
    global graphEndDate 
    graphStartDate = start
    graphEndDate = end

    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + servidor + ';DATABASE=' + banco + ';UID='+ usuario +';PWD='+senha)

    df_grafo_transacoes = pd.read_sql(f"""
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
                            AND e.DATA_LANCAMENTO BETWEEN CONVERT(DATE, '{ start }') AND CONVERT(DATE, '{ end }')
                            INNER JOIN TIPO_LANCAMENTO t ON e.TIPO_LANCAMENTO = t.CODIGO
                            ORDER BY DATA_LANCAMENTO
                                    """, conn)

    transacoes = []
    # organiza as conexões de acordo com o tipo de operação (Debito, ou Credito)
    for index, transacao in df_grafo_transacoes.iterrows():
        a = ''
        b = ''

        if (int(transacao["TIPO_LANCAMENTO"]) > 200):
            a = (transacao['AGENCIA_B'].strip() + '/' + transacao['CONTA_B'].strip())
            b = (transacao['AGENCIA_A'].strip() + '/' + transacao['CONTA_A'].strip())

        else:
            a = (transacao['AGENCIA_A'].strip() + '/' + transacao['CONTA_A'].strip())
            b = (transacao['AGENCIA_B'].strip() + '/' + transacao['CONTA_B'].strip())

        transacoes.append({
            'emissor': a,
            'destinatario': b,
            'valor': float(transacao['VALOR_TRANSACAO']),
            'tipo': transacao['DESCRICAO'],
            'data': transacao['DATA_LANCAMENTO'],
            'id': transacao['CODIGO_CHAVE_OD']
        })

    # objeto organizado entre emissario e destinatario


    df = pd.DataFrame(transacoes, columns=['emissor', 'destinatario', 'valor', 'tipo', 'data', 'id'])

    # obtem o peso e soma as transacoes
    emissorDestinatario = df.groupby(['emissor', 'destinatario']).valor.agg('sum').to_frame('total').reset_index()

    emissorDestinatario['peso'] = 0
    emissorDestinatario['peso'] = df.groupby(['emissor', 'destinatario']).emissor.agg('count').to_frame('count').reset_index()['count']

    # cria os links
    # soma os valores e os pesos

    edges = []
    emissorDestinatario['used'] = 0

    for index, transacao in emissorDestinatario.iterrows():
        edges.append({
            'emissor': transacao['emissor'],
            'destinatario': transacao['destinatario'],
            'valor': transacao['total'],
            'peso': transacao['peso']
        })

    #cria os textos de cada edge
    edge_text = []
    data_text = []
    for e in edges:
        edge_text.append(f"""Total: R$ {'%.2f' % float(e['valor'])}""")
        data_text.append(e['emissor']+','+e['destinatario'])

    #intervalor para calibrar o mapa de calor da transação
    #é necessario somar com todas as transações de um mesmo conjunto de nodos
    #criar uma escala e calibrar as cores
    #minimoValor = df_grafo_transacoes.min(level='VALOR_TRANSACAO')
    #maximoValor = df_grafo_transacoes.max('VALOR_TRANSACAO')

    #obtem os nodos Agencia/Conta
    df_node = pd.read_sql("""
                        SELECT CONVERT(VARCHAR,NUMERO_AGENCIA_OD)+'/'+CONVERT(VARCHAR,NUMERO_CONTA_OD)  AS NODE
                        
                        FROM ORIGEM_DESTINO 
                        UNION 
                        SELECT CONVERT(VARCHAR,e.NUMERO_AGENCIA)+'/'+CONVERT(VARCHAR,e.NUMERO_CONTA) AS NODE
                        
                        FROM EXTRATO e 
                        
                        """,conn)

    conn.close()
    G = nx.Graph()


    #configura o objeto que define a cor e o tamanho das conexões
    graphEdges = []
    for e in edges:
        length = 1 / e['peso'] if e['peso'] > 0 else 1
        
        G.add_edge(e['emissor'],e['destinatario'], length=length, weight=e['peso'])


    #adiciona os nodos  
    nodes = df_node['NODE'].to_numpy()
    G.add_nodes_from(nodes)

    # #adiciona as conexões e suas direções respectivas

    pos=nx.fruchterman_reingold_layout(G)


    axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )

    
    Xv=[pos[k][0] for k in nodes]
    Yv=[pos[k][1] for k in nodes]
    Xed=[]
    Yed=[]
    texto_x = []
    texto_y = []
    for edge in edges:
        x = [pos[edge['emissor']][0],pos[edge['destinatario']][0], None]
        y = [pos[edge['emissor']][1],pos[edge['destinatario']][1], None]
        texto_x += [((x[0] + x[1]) / 2)]
        texto_y += [((y[0] + y[1]) / 2)]
        Xed+= x
        Yed+= y

    text_trace = Scatter(
                x=texto_x,y=texto_y, 
                mode='markers',
                name='dados da transação',
                marker=dict(symbol='circle-dot',
                                size=12,
                                color='#960200',
                                line=dict(color='#000', width=0.1)
                                ),
                text=edge_text,
                customdata=data_text,
                hoverinfo='text'
            )


    edge_trace=Scatter(x=Xed,
                y=Yed,
                mode='lines',
                name='transação',
                line=dict(color='#333', width=2),
                hoverinfo='none'
                )

    node_trace=Scatter(x=Xv,
                y=Yv,
                mode='markers+text',
                name='agência/conta',
                marker=dict(symbol='circle-dot',
                                size=40,
                                color='#e0c216',
                                line=dict(color='#000', width=0.1)
                                ),
                text=[ node[0] for node in df_node.to_numpy() ],
                hoverinfo='text',
                textposition='top center'
                )


    return {
        'data' : [edge_trace, node_trace, text_trace],
        'layout': dict(
            font= dict(size=12),
            showlegend=True,
            autosize=True,
            height=700,
            paper_bgcolor='rgba(0,0,0,0)', # transparent background
            plot_bgcolor='rgba(0,0,0,0)', # transparent background
            xaxis=XAxis(axis),
            yaxis=YAxis(axis),
            margin=Margin(
                l=40,
                r=40,
                b=10,
                t=100,
            ),
            hovermode='closest',
        )
    }
    
#gráfico de transações u turn
@app.callback(
    Output('uturn', 'figure'),
    [Input('uturnPicker', 'start_date'),
    Input('uturnPicker', 'end_date')]
)
def transacoes_u_graph(start, end):
 #busca pelas transações em U
    global servidor
    global banco
    global usuario 
    global senha
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + servidor + ';DATABASE=' + banco + ';UID='+ usuario +';PWD='+senha)

    #IDENTIFICA TRANSAÇÕES U-TURN INDIVIDUAIS
    df_transacoes = pd.read_sql(f""" SELECT 
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
                                WHERE e.DATA_LANCAMENTO BETWEEN CONVERT(DATE, '{ start }') AND CONVERT(DATE, '{ end }')
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
            if(d1 < d2):
                edgesText.append(
                f"""
                Data: { row['data'] } 
                <br>
                Débito de: { row['conta_origem'] if row['tipo'] < 200 else row['conta_destino'] }
                <br> 
                Crédito em: { row['conta_origem'] if row['tipo'] > 200 else row['conta_destino'] }
                <br>
                Valor: R${ '%.2f' % float(row['valor']) }
                <br>
                ----------------------------
                <br>
                Data: {  df_uturn.loc[id+1, 'data'] }
                <br>
                Débito de: { df_uturn.loc[id+1,'conta_origem'] if row['tipo'] < 200 else df_uturn.loc[id+1,'conta_destino'] } 
                <br>
                Crédito em: { df_uturn.iloc[id+1]['conta_origem'] if row['tipo'] > 200 else df_uturn.iloc[id+1]['conta_destino'] }
                <br>
                Valor: R${ '%.2f' % float(row['valor']) }
                """
                )
            else:
                edgesText.append(
                f"""
                Data: {  df_uturn.loc[id+1, 'data'] }
                <br>
                Débito de: { df_uturn.loc[id+1,'conta_origem'] if row['tipo'] < 200 else df_uturn.loc[id+1,'conta_destino'] } 
                <br>
                Crédito em: { df_uturn.iloc[id+1]['conta_origem'] if row['tipo'] > 200 else df_uturn.iloc[id+1]['conta_destino'] }
                <br>
                Valor: R${ '%.2f' % float(row['valor']) }
                <br>
                ---------------------------- 
                <br>
                Data: { row['data'] } 
                <br>
                Débito de: { row['conta_origem'] if row['tipo'] < 200 else row['conta_destino'] } 
                <br>
                Crédito em: { row['conta_origem'] if row['tipo'] > 200 else row['conta_destino']}
                <br>
                Valor: R${ '%.2f' % float(row['valor']) }
                """
                )

    conn.close()
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
        name='transação',
        line=dict(width=0.5, color='#333'),
        #hoverinfo='text',
        #hovertext=edgesText
        )
            

    node_trace = Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                name='agência/conta',
                marker=dict(symbol='circle-dot',
                                size=40,
                                color='#e0c216',
                                line=dict(color='#000', width=0.1)
                                ),
                text=nodes,
                hovertemplate='%{text}',
                    showlegend = False,
                    textposition='top center'
                )

    text_trace = Scatter(
                x=texto_x,y=texto_y, 
                mode='markers',
                name='dados da transação',
                marker=dict(symbol='circle-dot',
                                size=12,
                                color='#960200',
                                line=dict(color='#000', width=0.1)
                                ),
                text=edgesText,
                    hoverinfo='text'
                )
        

    return { 'data' : [edge_trace, node_trace, text_trace],
                'layout' : dict(
                    titlefont_size=16,
                    showlegend=True,
                    paper_bgcolor='rgba(0,0,0,0)', # transparent background
                    plot_bgcolor='rgba(0,0,0,0)', # transparent background
                    hovermode='closest',
                    margin=dict(b=10,l=40,r=40,t=100),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    }


@app.callback(
    [Output('graph-modal', 'is_open'),
    Output('modalbody', 'children')],
    [Input('transacoes', 'clickData')],
    [State('graph-modal', 'is_open')]
)
def showTransactionData(clickData, is_open):
    
    if(clickData != None and clickData['points'][0]['customdata']):
        data = clickData['points'][0]['customdata'].split(',')
        contaA = data[0].split('/')
        contaB = data[1].split('/')

        global graphStartDate
        global graphEndDate 

        start = datetime.datetime.strptime(graphStartDate.split('T')[0], '%Y-%m-%d').strftime('%d/%m/%Y')
        end = datetime.datetime.strptime(graphEndDate.split('T')[0], '%Y-%m-%d').strftime('%d/%m/%Y')

        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + servidor + ';DATABASE=' + banco + ';UID='+ usuario +';PWD='+senha)
        
        df = pd.read_sql(f""" SELECT 
                    DISTINCT
                    e.CODIGO_CHAVE_EXTRATO AS ID,
                    (SELECT TOP(1) NOME_TITULAR FROM TITULARES WHERE NUMERO_BANCO = e.NUMERO_BANCO AND NUMERO_AGENCIA = e.NUMERO_AGENCIA AND NUMERO_CONTA = e.NUMERO_CONTA ) AS 'TITULAR A',
                    CONCAT(e.NUMERO_BANCO,' / ',e.NUMERO_AGENCIA,' / ',e.NUMERO_CONTA) AS 'BANCO / AGÊNCIA / CONTA A',
                    DESCRICAO AS 'TIPO DE LANÇAMENTO',
                    e.DESCRICAO_LANCAMENTO AS 'DESCRIÇÃO DO LANÇAMENTO',
                    FORMAT(o.VALOR_TRANSACAO, 'C') AS VALOR,
                    CONVERT(CHAR, e.DATA_LANCAMENTO, 103) AS 'DATA',
                    o.NOME_PESSOA_OD AS 'TITULAR B',
                    CONCAT(o.NUMERO_BANCO_OD,' / ',o.NUMERO_AGENCIA_OD,' / ',o.NUMERO_CONTA_OD) AS 'BANCO / AGÊNCIA / CONTA B',
                    LOCAL_TRANSACAO AS 'LOCAL DA TRANSAÇÃO',
                    o.NOME_ENDOSSANTE_CHEQUE AS 'NOME ENDOSSANTE CHEQUE',
                    o.DOC_ENDOSSANTE_CHEQUE AS 'DOC ENDOSSANTE CHEQUE',
                    o.CODIGO_DE_BARRAS AS 'CÓDIGO DE BARRAS',
                    o.OBSERVACAO AS 'OBSERVAÇÃO'
                    FROM EXTRATO e
                    INNER JOIN ORIGEM_DESTINO o ON e.CODIGO_CHAVE_EXTRATO = o.CODIGO_CHAVE_EXTRATO
                    INNER JOIN TIPO_LANCAMENTO t ON t.CODIGO = e.TIPO_LANCAMENTO
                    WHERE 
                    (e.NUMERO_AGENCIA = '{ contaA[0] }' AND e.NUMERO_CONTA = '{ contaA[1] }' AND o.NUMERO_AGENCIA_OD = '{ contaB[0] }' AND o.NUMERO_CONTA_OD = '{ contaB[1] }') 
                    OR 
                    (e.NUMERO_AGENCIA = '{ contaB[0] }' AND e.NUMERO_CONTA = '{ contaB[1] }' AND o.NUMERO_AGENCIA_OD = '{ contaA[0] }' AND o.NUMERO_CONTA_OD = '{ contaA[1] }') 
                    AND
                    e.DATA_LANCAMENTO BETWEEN '{start}' AND '{end}'
                     """, conn)
        

        table = html.Div(
                    style={'backgroundColor' : 'white'},
                    children = [
                        html.H4(children='Transações'),
                        
                    dash_table.DataTable(
                        data=df.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df.columns],
                        style_as_list_view=True,
                        style_cell={'padding': '5px', 'textAlign' : 'left'},
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold',
                            'textAlign' : 'left'
                        }
                        
                    )
                ]),

        return True, table
    return False, ''    

   
def open_browser():
	webbrowser.open_new("http://127.0.0.1:8050/")


if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=False)