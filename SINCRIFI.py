# -*- coding: utf-8 -*-
"""
Created on Tue May 12 08:55:23 2020

@author: jorge
"""
import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import pyodbc
import networkx as nx
from plotly.graph_objs import *
import chart_studio.plotly as py
import plotly.express as px
import webbrowser
from threading import Timer
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
import datetime

def makeLayout(dataLimite, connection):
    conn = connection
    dtin = dataLimite.iloc[0]['MINIMA']
    dtfi = dataLimite.iloc[0]['MAXIMA']


    df_nome_do_caso = pd.read_sql("""SELECT DB_NAME() AS [Current Database];""", conn)

    df_totalEmTransacoes = pd.read_sql("select FORMAT(SUM(VALOR_TRANSACAO), 'C') AS total from ORIGEM_DESTINO", conn)
    
    #agregado de investigados 
    df_investigados = pd.read_sql(""" SELECT PESSOA_INVESTIGADA FROM TITULARES WHERE PESSOA_INVESTIGADA = 1 """, conn) 

    #Obtém os investigados e o saldo em suas contas
    df_envolvidos = pd.read_sql("""
                SELECT t.NOME_TITULAR AS NOME, 
                CASE WHEN t.PESSOA_INVESTIGADA = 1 THEN 'SIM' ELSE 'NÃO' END AS 'SIGILO AFASTADO',
                t.VALOR_RENDA AS RENDA,  
                ISNULL(
                (SELECT TOP(1) VALOR_SALDO
                    FROM EXTRATO e 
                    WHERE e.NUMERO_BANCO = t.NUMERO_BANCO 
                    AND e.NUMERO_AGENCIA = t.NUMERO_AGENCIA 
                    AND e.NUMERO_CONTA LIKE t.NUMERO_CONTA 
                    ORDER BY e.DATA_LANCAMENTO DESC) 
            , '0') AS SALDO,
                t.CPF_CNPJ_TITULAR AS 'CPF/CNPJ',  t.TELEFONE_PESSOA AS FONE,
                t.EDNDERECO_LOGRADOURO AS LOGRADOURO, t.ENDERECO_CIDADE AS CIDADE, t.ENDERECO_UF AS UF, t.ENDERECO_CEP AS CEP,
                t.NUMERO_BANCO AS BANCO, t.NUMERO_AGENCIA AS AGÊNCIA, t.NUMERO_CONTA AS CONTA
                FROM TITULARES t ORDER BY NOME
                                
                                """, conn)
                                
    figure_saldo_envolvidos = Figure(
            px.pie(df_envolvidos, values='SALDO', names='NOME', title="Saldo em conta")
    )

    figure_renda = Figure(
            px.pie(df_envolvidos, values='RENDA', names='NOME', title='Renda')
    )    


    df_bancos_envolvidos = pd.read_sql("""
                                SELECT 
                                NOME_AGENCIA AS NOME, 
                                TRIM(CONVERT(CHAR, NUMERO_BANCO))+' / '+TRIM(CONVERT(CHAR,NUMERO_AGENCIA)) AS 'BANCO/AGÊNCIA', 
                                ENDERECO_CIDADE AS CIDADE, 
                                ENDERECO_CEP AS CEP, 
                                ENDERECO_UF AS UF, 
                                ENDERECO_PAIS AS 'PAÍS', 
                                TELEFONE_AGENCIA AS FONE,
                                ISNULL(CONVERT(VARCHAR,DATA_ABERTURA_AGENCIA, 103), '-') AS ABERTURA, 
                                ISNULL(convert(VARchar,DATA_FECHAMENTO_AGENCIA, 103), '-') AS FECHAMENTO 
                                FROM AGENCIAS ORDER BY NOME_AGENCIA
                                    """
                                    ,conn)

    df_relacao_contas = pd.read_sql(""" 
                            SELECT DISTINCT t.NOME_TITULAR AS 'NOME TITULAR', 
                            NOME AS 'TIPO DE CONTA',
                            t.NUMERO_BANCO AS 'BANCO', 
                            t.NUMERO_AGENCIA AS 'AGÊNCIA', t.NUMERO_CONTA AS 'CONTA', 
                            a.NOME_AGENCIA AS 'NOME AGÊNCIA', CONVERT(CHAR, c.DATA_ABERTURA_CONTA, 103) AS 'DATA DE ABERTURA', 
                            CONVERT(CHAR, c.DATA_ENCERRAMENTO_CONTA, 103) AS 'DATA DE ENCERRAMENTO'  FROM TITULARES t
                            INNER JOIN AGENCIAS a ON a.NUMERO_BANCO = t.NUMERO_BANCO AND a.NUMERO_AGENCIA = t.NUMERO_AGENCIA
                            INNER JOIN CONTAS c ON c.NUMERO_BANCO = a.NUMERO_BANCO AND c.NUMERO_AGENCIA = t.NUMERO_AGENCIA AND t.TIPO_CONTA = c.TIPO_CONTA
                            INNER JOIN TIPO_CONTA ON ID = c.TIPO_CONTA
                            ORDER BY t.NOME_TITULAR
                            """, conn)
                            
    df_periodo = pd.read_sql("""SELECT CONVERT(CHAR, max(DATA_LANCAMENTO), 103) AS 'FIM', CONVERT(CHAR, min(DATA_LANCAMENTO), 103) AS 'INICIO' FROM extrato""",conn)

   #obtem os nodos Agencia/Conta
    df_node = pd.read_sql("""
                        SELECT CONVERT(VARCHAR,NUMERO_AGENCIA_OD)+'/'+CONVERT(VARCHAR,NUMERO_CONTA_OD)  AS NODE
                        
                        FROM ORIGEM_DESTINO 
                        UNION 
                        SELECT CONVERT(VARCHAR,e.NUMERO_AGENCIA)+'/'+CONVERT(VARCHAR,e.NUMERO_CONTA) AS NODE
                        
                        FROM EXTRATO e 
                        
                        """,conn)
    conn.close()
    #layout
   
    return html.Div(style={"textAlign": 'center'}, children=[
        dbc.Modal(
                [
                    dbc.ModalBody(html.Div(style={'padding' : '10px', 'backgroundColor' : 'white'}, id='modalbody')),
                ],
                id="graph-modal",
                scrollable=True,
                centered=True,
                is_open=False,
                size='xl'
        ),

        html.H3(children="SINCRIFI"),
        html.H4(children='Sistema de Investigação de Crimes Financeiros'),
        html.H6(children="CASO: " + df_nome_do_caso["Current Database"] ),
        
        html.Div(
                style={'display' : 'flex', 'alignItems' : 'center', 'justifyContent': 'center'},
                children=[
                    html.Div(className="mini_container",
                                children=[
                                    html.H6(style={'fontSize' : '18px'}, children=df_totalEmTransacoes['total']),
                                    html.P(style={'fontSize' : '14px'}, children="Total em transações")
                                ]),
                        
                        html.Div(className="mini_container",
                                children=[
                                    html.H6(style={'fontSize' : '18px'}, children=df_investigados.count()[0]),
                                    html.P(style={'fontSize' : '14px'}, children="Investigados")
                                ]),
                        
                        html.Div(className="mini_container",
                                children=[
                                    html.H6(style={'fontSize' : '18px'}, children=df_node.count()[0]),
                                    html.P(style={'fontSize' : '14px'}, children="Envolvidos")
                                ]),
                        
                        html.Div(className="mini_container",
                                children=[
                                    html.H6(style={'fontSize' : '18px'}, children=df_bancos_envolvidos.count()[0]),
                                    html.P(style={'fontSize' : '14px'}, children="Agências")
                                ]),
                        
                        html.Div(className="mini_container",
                                children=[
                                    html.H6(style={'fontSize' : '18px'}, children=df_periodo['INICIO']+' - ' + df_periodo['FIM']),
                                    html.P(style={'fontSize' : '14px'}, children="Período")
                                ])
                        
                ]),
        
    
        
        html.Hr(),
        
        #Saldo em conta dos investigados
        html.Div(
            style={'display' : 'flex', 'alignItems' : 'center', 'justifyContent': 'center'},
            children=[
                html.Div(
                    className="pretty_container seven columns",
                    children=[
                
                    dcc.Graph(figure=figure_saldo_envolvidos)
                    ]),
                
                html.Div(
                    className="pretty_container seven columns",
                    children=[
                        dcc.Graph(figure=figure_renda)
                        
                    ])
            ]),
        html.Div(
            style={'display' : 'flex', 'alignItems' : 'center', 'justifyContent': 'center', 'flexDirection' : 'column' },
            children=[
                #Nomes dos Investigados
                html.Div(
                    className="pretty_container nine columns",
                    style={'backgroundColor' : 'white'},
                    children = [
                        html.H4(children='Dados Pessoais'),
                        
                        
                    dash_table.DataTable(
                        data=df_envolvidos.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df_envolvidos[['NOME', 'SIGILO AFASTADO', 'CPF/CNPJ', 'FONE', 'LOGRADOURO', 'CIDADE', 'UF', 'CEP']].columns],
                        style_as_list_view=True,
                        style_cell={'padding': '5px', 'textAlign' : 'left'},
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold',
                            'textAlign' : 'left'
                        }
                        
                    )
                ]),
            
                #Agências envolvidos
                html.Div(
                    className="pretty_container nine columns",
                    style={'backgroundColor' : 'white'},
                    children=[
                        html.H4(children='Agências envolvidas'),
                        
                        dash_table.DataTable(
                            data=df_bancos_envolvidos.to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in df_bancos_envolvidos[['NOME', u'BANCO/AGÊNCIA', 'CIDADE', 'UF', u'PAÍS', 'FONE', 'CEP', 'FONE', 'ABERTURA', 'FECHAMENTO']].columns],
                            style_as_list_view=True,
                            style_cell={'padding': '5px', 'textAlign' : 'left'},
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold',
                                'textAlign' : 'left'
                            }
                            
                        )                
                    ]),
                
            
    
        
            #Relação de contas
            html.Div(
                className="pretty_container nine columns",
                style={'backgroundColor' : 'white'},
                children=[
                    html.H4(children='Relação de contas'),
                    
                    dash_table.DataTable(
                        data=df_relacao_contas.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df_relacao_contas.columns],
                        style_as_list_view=True,
                        style_cell={'padding': '5px', 'textAlign' : 'left'},
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold',
                            'textAlign' : 'left'
                        }
                        
                    )
                ]),    
            
            #grafo das transações dos investigados
            html.Div(className="pretty_container eleven columns",
                style={'backgroundColor' : 'white'},
                children=[

                html.H3(style={'textAlign' : 'center'}, children='Rede de Transações'),
                html.H5(style={'textAlign' : 'center'}, children='Período'),

                #perídodo
                dcc.DatePickerRange(
                    id='transacoesPicker',
                    display_format='DD/MM/Y',
                    min_date_allowed=dt(int(dtin[6:]), int(dtin[3:5]), int(dtin[:2])),
                    max_date_allowed=dt(int(dtfi[6:]), int(dtfi[3:5]), int(dtfi[:2])),
                    initial_visible_month=dt(int(dtin[6:]), int(dtin[3:5]), int(dtin[:2])),
                    start_date=dt(int(dtin[6:]), int(dtin[3:5]), int(dtin[:2])),
                    end_date=dt(int(dtfi[6:]), int(dtfi[3:5]), int(dtfi[:2])).date()
                ),
                #div do grafo
                html.Div(
                        children=[
                            dcc.Graph(
                                id='transacoes'
                            )    
                        ]),
                
                #painel com mais informações do click
                #html.Div(style={})
            ]),

            
            
            #grafo das transações em U individuais
            html.Div(className="pretty_container eleven columns",
                style={'backgroundColor' : 'white'},
                children=[

                html.H3(style={'textAlign' : 'center'}, children='Transações em U'),
                html.H5(style={'textAlign' : 'center'}, children='Período'),

                #perídodo
                dcc.DatePickerRange(
                    id='uturnPicker',
                    display_format='DD/MM/Y',
                    min_date_allowed=dt(int(dtin[6:]), int(dtin[3:5]), int(dtin[:2])),
                    max_date_allowed=dt(int(dtfi[6:]), int(dtfi[3:5]), int(dtfi[:2])),
                    initial_visible_month=dt(int(dtin[6:]), int(dtin[3:5]), int(dtin[:2])),
                    start_date=dt(int(dtin[6:]), int(dtin[3:5]), int(dtin[:2])),
                    end_date=dt(int(dtfi[6:]), int(dtfi[3:5]), int(dtfi[:2])).date()
                ),
                #div do grafo
                html.Div(
                        children=[
                            dcc.Graph(id='uturn')    
                        ]),
            ])

        ]), 
    ])
