from re import template
import dash
import dash_core_components as dcc
from dash_core_components.Graph import Graph
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Br import Br
import plotly.express as px
import plotly.graph_objs as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import geopandas as gpd
from datetime import datetime as dt
import numpy as np
from datetime import timedelta

#----------

# Layout General
def alfonsoreyes():

    return html.Div([

        # Tabs
        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            
                            dbc.Tab(label = 'Conteo', tab_id = 'fichatecnica_conteo',
                                disabled = False),
                            
                            dbc.Tab(label = 'Velocidad', tab_id = 'fichatecnica_vel',
                            disabled = False),

                            dbc.Tab(label = 'Reparto Modal', tab_id = 'fichatecnica_reparto',
                            disabled = False),

                            dbc.Tab(label='Conteo y Velocidad', tab_id='alfonsoreyes_1',
                                disabled = True)
                        ],
                        id='tabs',
                        active_tab="fichatecnica_conteo",
                        card=True
                        )
                    ),
                    dbc.CardBody(
                        html.Div(id="alfonsoreyes_content")
                    )
                ]), lg=12

            ), justify = 'center'

        ),

        #Footer 
        dbc.Row([
            dbc.Col(
                html.H6('Instituto Municipal de Planeación y Gestión Urbana')),
            dbc.Col(
                html.H6('San Pedro Garza García, Nuevo León, México',
                    style = {'textAlign': 'right'}))
        ], className='px-3 py-4', style={'background-color': 'black','color': 'white'})

    ])

#----------

# Layout - BiciRuta
def alfonsoreyes_1():

    return html.Div([

        dbc.Row([

            dbc.Col([

                # Conteo y Velocidad
                dbc.RadioItems(
                    id = 'my_dropdown_0',
                    className = 'radio-group btn-group',
                    labelClassName = 'btn btn-secondary',
                    labelCheckedClassName = 'active',
                    value = 'conteo',
                    options = [
                        {'label': 'Conteo', 'value': 'conteo'},
                        {'label': 'Velocidad', 'value': 'velocidad_promedio'}
                    ]
                ),

                html.Br(),

                html.Br(),

                # Modos de transporte
                dbc.RadioItems(
                    id = 'my_dropdown',
                    className = 'btn-group',
                    labelClassName = 'btn btn-secondary',
                    labelCheckedClassName = 'active',
                    value = 'bicycle',
                    options = []
                )

            ], lg = 8),

            dbc.Col([

                html.Br(),
                
                html.Br(),

                # Calendario
                dcc.DatePickerRange(
                    id = 'calendario',
                    min_date_allowed = dt(2021, 7, 25),
                    max_date_allowed = dt(2021, 9, 19),
                    start_date = dt(2021, 7, 26),
                    end_date = dt(2021, 9, 19),
                    first_day_of_week = 1,
                    minimum_nights = 0,
                    updatemode = 'bothdates',
                    display_format = 'DD MMM YYYY',
                    style = {'float': 'right'}         
                )
            ], lg = 4)

        ], className = 'radio-group'),

        html.Br(),

        dbc.Row(

            dbc.Col(

                # Gráficas
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label='Hora', tab_id='hora',
                                disabled = False),
                            dbc.Tab(label = 'Día', tab_id = 'dia',
                                disabled = False)
                        ],
                        id='periodo',
                        active_tab="dia",
                        card=True
                        )
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id = 'conteo2',
                            figure = {},
                            config={
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    )
                ])

            )
        )

    ])

#----------

# Conexión entre dropdown de variables y dropdown de modo de transporte
def render_opciones(my_dropdown_0):

    if my_dropdown_0 == 'conteo':

        return [
            {'label': 'Bicicletas', 'value': 'bicycle'},
            {'label': 'Peatones', 'value': 'peatones'},
            {'label': 'Motocicletas', 'value': 'motorcycle'},
            {'label': 'Autobuses', 'value': 'bus'},
            {'label': 'Autos', 'value': 'autos'}
        ]   

    elif my_dropdown_0 == 'velocidad_promedio':

        return [
            {'label': 'Autos', 'value': 'avg_vel_car'},
            {'label': 'Motocicletas', 'value': 'avg_vel_motorcycle'},
            {'label': 'Autobuses', 'value': 'avg_vel_bus'}
        ]

#-------------------------------

# Visualizar gráficas de línea para conteo y velocidad
def render_conteo(periodo, my_dropdown, my_dropdown_0, start_date, end_date):

    # Diferencia en días entre fecha de inicio y fecha final
    start_date_tiempo = pd.to_datetime(start_date)
    end_date_tiempo = pd.to_datetime(end_date)
    dif_tiempo = end_date_tiempo - start_date_tiempo
    dif_tiempo = dif_tiempo / np.timedelta64(1, 'D')

    # Diferencia para el loop de semana
    dif_tiempo_loop = dif_tiempo

    # Conteo por hora
    if my_dropdown_0 == 'conteo' and periodo == 'hora':

        # Leer csv
        conteo_hora = pd.read_csv('assets/base_conteo_vel.csv')

        # Cambiar variables a string
        conteo_hora['hora'] = conteo_hora['hora'].astype(str)
        conteo_hora['fecha'] = conteo_hora['fecha'].astype(str)

        # Crear variable datetime
        conteo_hora['datetime'] = conteo_hora['fecha'] + '/' + conteo_hora['hora']
        conteo_hora['datetime'] = pd.to_datetime(conteo_hora['datetime'], 
            dayfirst = True, format = '%d/%m/%Y/%H')

        # Duplicar columna de fecha y set index
        conteo_hora['datetime1'] = conteo_hora['datetime']
        conteo_hora = conteo_hora.set_index('datetime')

        # Filtro por calendario
        conteo_hora = conteo_hora.loc[start_date:end_date]

        conteopromedio_hora = conteo_hora
        conteopromedio_hora['hora'] = conteopromedio_hora['hora'].astype(int)
        conteopromedio_hora = conteopromedio_hora.groupby('hora', as_index = False).mean()

        # Graph
        conteo2 = px.scatter(conteo_hora, x = 'datetime1', y = my_dropdown,
            template = 'plotly_white', hover_data = ['dia_semana'])

        conteo2.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>' +  conteo_hora['dia_semana'])
        conteo2.update_xaxes(showgrid = False, showline = True,
            title_text = '')
        conteo2.update_yaxes(title_text = '')
        conteo2.update_layout(hoverlabel = dict(font_size = 16),
            hoverlabel_align = 'right', hovermode = 'x unified')

        conteo3 = px.line(conteopromedio_hora, x = 'hora', y = my_dropdown,
                        template = 'plotly_white',
                        title = 'Conteo Promedio por Hora')
        
        conteo3.update_traces(mode="markers+lines", hovertemplate=None)
        conteo3.update_layout(hovermode="x unified")

        return conteo2

    # Conteo por día
    elif my_dropdown_0 == 'conteo' and periodo == 'dia':

        # Leer csv
        conteo_dia = pd.read_csv('assets/base_conteo_vel.csv')

        # Cambiar variable a datetime
        conteo_dia['fecha'] = pd.to_datetime(conteo_dia['fecha'],
            dayfirst = True)

        # Duplicar columna de fecha y set index
        conteo_dia['fecha1'] = conteo_dia['fecha']
        conteo_dia = conteo_dia.set_index('fecha')

        conteo_dia = conteo_dia.loc[start_date:end_date]
        conteo_dia.reset_index()

        conteo_dia = conteo_dia.drop(['mes', 'semana', 'dia_semana', 'hora'],
         axis = 1)
        conteo_dia = conteo_dia.loc[:, ~conteo_dia.columns.str.contains("avg")]
        conteo_dia = conteo_dia.groupby('fecha1', as_index = False).sum()
        conteo_dia['dia_semana'] = conteo_dia['fecha1'].dt.day_name()

        conteo2 = px.line(conteo_dia, x = 'fecha1', y = my_dropdown,
                    template = 'plotly_white', hover_data = ['dia_semana'])
        
        conteo2.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>' +  conteo_dia['dia_semana'])
        conteo2.update_xaxes(showgrid = False, showline = True,
            title_text = '')
        conteo2.update_yaxes(title_text = '')
        conteo2.update_layout(hoverlabel = dict(font_size = 16),
            hoverlabel_align = 'right', hovermode = 'x unified')

        return conteo2


    # Velocidad por hora
    elif my_dropdown_0 == 'velocidad_promedio' and periodo == 'hora':

        # Leer csv
        vel_hora = pd.read_csv('assets/base_conteo_vel.csv')

        # Cambiar variables a string
        vel_hora['hora'] = vel_hora['hora'].astype(str)
        vel_hora['fecha'] = vel_hora['fecha'].astype(str)

        # Crear variable datetime
        vel_hora['datetime'] = vel_hora['fecha'] + '/' + vel_hora['hora']
        vel_hora['datetime'] = pd.to_datetime(vel_hora['datetime'],
            dayfirst = True, format = '%d/%m/%Y/%H')

        # Duplicar columna de fecha y set index
        vel_hora['datetime1'] = vel_hora['datetime']
        vel_hora = vel_hora.set_index('datetime')

        # Filtro por calendario
        vel_hora = vel_hora.loc[start_date:end_date]

        # Graph
        conteo2 = px.scatter(vel_hora, x = 'datetime1', y = my_dropdown,
            template = 'plotly_white', hover_data = ['dia_semana'])

        conteo2.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>' +  vel_hora['dia_semana'])
        conteo2.update_xaxes(showgrid = False, showline = True,
            title_text = '')
        conteo2.update_yaxes(title_text = '')
        conteo2.update_layout(hoverlabel = dict(font_size = 16),
            hoverlabel_align = 'right', hovermode = 'x unified')

        return conteo2

    # Velocidad por día
    elif my_dropdown_0 == 'velocidad_promedio' and periodo == 'dia':

        # Leer csv
        vel_dia = pd.read_csv('assets/base_conteo_vel.csv')

        # Cambiar variable a datetime
        vel_dia['fecha'] = pd.to_datetime(vel_dia['fecha'],
            dayfirst = True)

        # Duplicar columna de fecha y set index
        vel_dia['fecha1'] = vel_dia['fecha']
        vel_dia = vel_dia.set_index('fecha')

        # Filtro por calendario
        vel_dia = vel_dia.loc[start_date:end_date]
        vel_dia = vel_dia.reset_index()
        
        vel_dia = vel_dia.drop(['hora', 'mes', 'semana', 'dia_semana',
                                   'child', 'hombre', 'mujer', 'peatones',
                                   'bicycle', 'motorcycle', 'car', 'pickup',
                                    'van', 'truck', 'autos', 'bus'],
         axis = 1)
        vel_dia = vel_dia.groupby('fecha1', as_index = False).mean()
        vel_dia['dia_semana'] = vel_dia['fecha1'].dt.day_name()

        # Graph
        conteo2 = px.line(vel_dia, x = 'fecha1', y = my_dropdown,
            template = 'plotly_white',hover_data = ['dia_semana'])

        conteo2.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>' +  vel_dia['dia_semana'])
        conteo2.update_xaxes(showgrid = False, showline = True, title_text = '')
        conteo2.update_yaxes(title_text = '')
        conteo2.update_layout(hoverlabel = dict(font_size = 16),
         hoverlabel_align = 'right', hovermode = 'x unified')

        return conteo2


#-------------------------------

# Layout Ficha Técnica - Conteo
def fichatecnica_conteo():
    return html.Div([

        dbc.Row([

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Bicicletas por Semana (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'bici_semana',
                            figure = fig1,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])
            ]),

            dbc.Col([
                dbc.Card([

                    dbc.CardHeader(
                        'Bicicletas por Día de la Semana (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'bici_diasemana',
                            figure = fig11,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])
            ])
        ]),

        html.Br(),

        dbc.Row([
            
           dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Bicicletas por Día (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'bici_dia',
                            figure = fig2,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])
            ]),

            dbc.Col([
                dbc.Card([

                    dbc.CardHeader(
                        'Bicicletas por Hora (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'bici_hora',
                            figure = fig3,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])
            ]) 
        ]),

        html.Br(),

        dbc.Row([

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Peatones por Semana (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'peatones_semana',
                            figure = fig4,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])
            ]),

            dbc.Col([
                dbc.Card([

                    dbc.CardHeader(
                        'Peatones por Día de la Semana (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'peatones_diasemana',
                            figure = fig12,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])
            ])
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Peatones por Día (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'peatones_dia',
                            figure = fig5,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])
            ]),

            dbc.Col([
                dbc.Card([

                    dbc.CardHeader(
                        'Peatones por Hora (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'peatones_hora',
                            figure = fig6,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])
            ])
        ]),

        html.Br(),

        dbc.Row([

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Vehículos Motorizados por Semana (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'motorizados_semana',
                            figure = fig7,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])
            ]),

            dbc.Col([
                dbc.Card([

                    dbc.CardHeader(
                        'Vehículos Motorizados por Día de la Semana (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'motorizados_diasemana',
                            figure = fig13,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])
            ])
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Vehículos Motorizados por Día (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'motorizados_dia',
                            figure = fig8,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])
            ]),

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Vehículos Motorizados por Hora (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'motorizados_hora',
                            figure = fig9,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])
            ])
        ]),

        html.Br(),

        dbc.Row([

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Información Adicional'
                    ),

                    dbc.CardBody([
                        'La información proviene de los datos reportados entre el 26 de julio y el 19 de septiembre en el cruce de Alfonso Reyes y Las Sendas.'
                    ])
                ])
            ])
        ])
    ])

ficha_alfonso = pd.read_csv('assets/base_conteo_vel.csv')
ficha_alfonso = ficha_alfonso[ficha_alfonso['dia_semana'] != 'sábado']
ficha_alfonso = ficha_alfonso[ficha_alfonso['dia_semana'] != 'domingo']

#Datos de conteo semanales
semana_alfonso = ficha_alfonso.drop(['mes', 'hora', 'dia_semana', 'fecha'], axis = 1)
semana_alfonso = semana_alfonso.loc[:, ~semana_alfonso.columns.str.contains("avg")]
semana_alfonso = semana_alfonso.groupby('semana', as_index = False).sum()
semana_alfonso['motorizados'] = semana_alfonso['motorcycle'] + semana_alfonso['autos'] + semana_alfonso['bus']

#Datos de conteo por día de la semana

diasemana_alfonso = ficha_alfonso.drop(['mes', 'semana', 'dia_semana', 'hora'], axis = 1)
diasemana_alfonso = diasemana_alfonso.loc[:, ~diasemana_alfonso.columns.str.contains("avg")]
diasemana_alfonso['fecha'] = pd.to_datetime(diasemana_alfonso['fecha'], dayfirst = True)
diasemana_alfonso = diasemana_alfonso.groupby('fecha', as_index = False).sum()
diasemana_alfonso['dia_semana'] = diasemana_alfonso['fecha'].dt.day_name()
diasemana_alfonso = diasemana_alfonso.drop('fecha', axis = 1)
diasemana_alfonso['dia_semana'] = diasemana_alfonso['dia_semana'].astype(str)
diasemana_alfonso = diasemana_alfonso.groupby('dia_semana', as_index = False, sort = False).mean()
diasemana_alfonso['motorizados'] = diasemana_alfonso['motorcycle'] + diasemana_alfonso['autos'] + diasemana_alfonso['bus']

#Datos de conteo diarios
dias_alfonso = ficha_alfonso.drop(['mes', 'semana', 'dia_semana', 'hora'], axis = 1)
dias_alfonso = dias_alfonso.loc[:, ~dias_alfonso.columns.str.contains("avg")]
dias_alfonso['fecha'] = pd.to_datetime(dias_alfonso['fecha'], dayfirst = True)
dias_alfonso = dias_alfonso.groupby('fecha', as_index = False).sum()
dias_alfonso['dia_semana'] = dias_alfonso['fecha'].dt.day_name()
dias_alfonso['motorizados'] = dias_alfonso['motorcycle'] + dias_alfonso['autos'] + dias_alfonso['bus']

#Datos de conteo promedio por hora del día
dias_promedio = ficha_alfonso.drop(['mes', 'semana', 'dia_semana', 'fecha'], axis = 1)
dias_promedio = dias_promedio.loc[:, ~dias_promedio.columns.str.contains("avg")]
dias_promedio = dias_promedio.groupby('hora', as_index = False).mean()
dias_promedio['motorizados'] = dias_promedio['motorcycle'] + dias_promedio['autos'] + dias_promedio['bus']

#Gráfica de Conteo por Semana de Bicicletas es fig1
fig1 = px.line(semana_alfonso, x = 'semana', y = 'bicycle',
       labels = {'fecha': 'Fecha', 'bicycle': 'Bicicletas'},
       template = 'plotly_white')

fig1.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig1.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig1.update_yaxes(title_text = '')
fig1.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#Gráfica de conteo por día de bicicletas es fig2
fig2 = px.line(dias_alfonso, x = 'fecha', y = 'bicycle',
       labels = {'fecha': 'Fecha', 'bicycle': 'Bicicletas'},
       template = 'plotly_white',
       hover_data = ['dia_semana'])

fig2.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>' +  dias_alfonso['dia_semana'])
fig2.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig2.update_yaxes(title_text = '')
fig2.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#Gráfica de conteo promedio por hora del día de bicicletas es fig3
fig3 = px.line(dias_promedio, x = 'hora', y = 'bicycle',
       labels = {'fecha': 'Fecha', 'bicycle': 'Bicicletas'},
       template = 'plotly_white')

fig3.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig3.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig3.update_yaxes(title_text = '')
fig3.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#Gráfica de Conteo por Semana de Peatones es fig4
fig4 = px.line(semana_alfonso, x = 'semana', y = 'peatones',
       labels = {'fecha': 'Fecha', 'peatones': 'Peatones'},
       template = 'plotly_white')

fig4.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig4.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig4.update_yaxes(title_text = '')
fig4.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#Gráfica de conteo por día de peatones es fig5
fig5 = px.line(dias_alfonso, x = 'fecha', y = 'peatones',
       labels = {'fecha': 'Fecha', 'peatones': 'Peatones'},
       template = 'plotly_white',
       hover_data = ['dia_semana'])

fig5.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>' +  dias_alfonso['dia_semana'])
fig5.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig5.update_yaxes(title_text = '')
fig5.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#Gráfica de conteo promedio por hora del día de peatones es fig6
fig6 = px.line(dias_promedio, x = 'hora', y = 'peatones',
       labels = {'fecha': 'Fecha', 'bicycle': 'Peatones'},
       template = 'plotly_white')

fig6.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig6.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig6.update_yaxes(title_text = '')
fig6.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#Gráfica de Conteo por Semana de Motorizados es fig7
fig7 = px.line(semana_alfonso, x = 'semana', y = 'motorizados',
       labels = {'fecha': 'Fecha', 'motorizados': 'Vehículos Motorizados'},
       template = 'plotly_white')

fig7.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig7.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig7.update_yaxes(title_text = '')
fig7.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#Gráfica de conteo por día de motorizados es fig8
fig8 = px.line(dias_alfonso, x = 'fecha', y = 'motorizados',
       labels = {'fecha': 'Fecha', 'motorizados': 'Vehículos Motorizados'},
       template = 'plotly_white',
       hover_data = ['dia_semana'])

fig8.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>' +  dias_alfonso['dia_semana'])
fig8.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig8.update_yaxes(title_text = '')
fig8.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#Gráfica de conteo promedio por hora del día de motorizados es fig9
fig9 = px.line(dias_promedio, x = 'hora', y = 'motorizados',
       labels = {'fecha': 'Fecha', 'motorizados': 'Vehículos Motorizados'},
       template = 'plotly_white')

fig9.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig9.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig9.update_yaxes(title_text = '')
fig9.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

fig11 = px.line(diasemana_alfonso, x = 'dia_semana', y = 'bicycle',
                labels = {'dia_semana': 'Día de la Semana', 'bicycle': 'Bicicletas'},
                template = 'plotly_white')

fig11.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig11.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig11.update_yaxes(title_text = '')
fig11.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

fig12 = px.line(diasemana_alfonso, x = 'dia_semana', y = 'peatones',
                labels = {'dia_semana': 'Día de la Semana', 'peatones': 'Peatones'},
                template = 'plotly_white')

fig12.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig12.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig12.update_yaxes(title_text = '')
fig12.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

fig13 = px.line(diasemana_alfonso, x = 'dia_semana', y = 'motorizados',
                labels = {'dia_semana': 'Día de la Semana', 'motorizados': 'Vehículos Motorizados'},
                template = 'plotly_white')

fig13.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig13.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig13.update_yaxes(title_text = '')
fig13.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#-----------------------------------

# Layout Ficha Técnica - Velocidad
def fichatecnica_vel():
    return html.Div([

        dbc.Row([

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Velocidad - Auto Particular (Entre Semana)'
                    ),

                    dbc.CardBody(

                        dcc.Graph(

                            id = 'indic_velocidad',
                            figure = indic,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False}
                        )
                    )
                ])
            ]),

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Velocidad Promedio de Autos Particulares por Hora (Entre Semana)'
                    ),

                    dbc.CardBody(

                        dcc.Graph(
                            id = 'velocidad_autos',
                            figure = fig10,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    )
                ])
            ])
        ]),

        html.Br(),

        dbc.Row([

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Información Adicional'
                    ),

                    dbc.CardBody([
                        'La información proviene de los datos reportados entre el 26 de julio y el 19 de septiembre en el cruce de Alfonso Reyes y Las Sendas.'
                    ])
                ])
            ])
        ])
    ])


vel_alfonso = ficha_alfonso.drop(['fecha', 'mes', 'semana', 'dia_semana',
                                   'child', 'hombre', 'mujer', 'peatones',
                                   'bicycle', 'motorcycle', 'autos', 'pickup',
                                    'van', 'truck', 'autos', 'bus'], axis = 1)
vel_alfonso = vel_alfonso.groupby('hora', as_index = False).mean()

fig10 = px.line(vel_alfonso, x = 'hora', y = 'avg_vel_car',
       labels = {'avg_vel_car': 'Velocidad Promedio (km/h)', 'hora': 'Hora'},
       template = 'plotly_white')

fig10.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig10.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig10.update_yaxes(title_text = '')
fig10.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

indic = go.Figure(go.Indicator(
    mode = "number",
    value = 67,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {"text": "Velocidad Promedio<br><span style='font-size:0.8em;color:gray'>"}
))
indic.update_layout(
     margin = dict(t=0, l=0, r=0, b=0))

indic.update_traces(
    number_suffix='km/h', 
    selector=dict(type='indicator'))

#------------------------------

# Layout Reparto Modal

def fichatecnica_reparto():
    return html.Div([

        dbc.Row([

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Reparto Modal (Entre Semana)'
                    ),

                    dbc.CardBody(

                        dcc.Graph(
                            id = 'reparto_modal',
                            figure = bar_reparto,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    )
                ])
            ]),

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Género de Peatones (Entre Semana)'
                    ),

                    dbc.CardBody(

                        dcc.Graph(
                            id = 'gender_peatones',
                            figure = pie_peatones,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    )
                ])
            ])
        ])
    ])

mes_alfonso = ficha_alfonso.drop(['semana', 'fecha', 'dia_semana', 'hora', 'child', 'mujer', 'hombre', 
                      'car', 'pickup', 'van', 'truck', 'bus'], axis = 1)
mes_alfonso = mes_alfonso.loc[:, ~mes_alfonso.columns.str.contains("avg")]
mes_alfonso = mes_alfonso.groupby('mes', as_index = False, sort = False).sum()

peatones = sum(mes_alfonso['peatones'])
bici = sum(mes_alfonso['bicycle'])
moto = sum(mes_alfonso['motorcycle'])
autos = sum(mes_alfonso['autos'])
total = peatones + bici + moto + autos

peatones = [peatones / total]
bici = [bici / total]
moto = [moto / total]
autos = [autos / total]

reparto_modal = pd.DataFrame()
reparto_modal['peatones'] = peatones
reparto_modal['bicicletas'] = bici
reparto_modal['motocicletas'] = moto
reparto_modal['autos'] = autos

reparto_modal['peatones'] = reparto_modal['peatones'] * 100
reparto_modal['bicicletas'] = reparto_modal['bicicletas'] * 100
reparto_modal['motocicletas'] = reparto_modal['motocicletas'] * 100
reparto_modal['autos'] = reparto_modal['autos'] * 100

reparto_modal['peatones'] = reparto_modal['peatones'].round(2)
reparto_modal['bicicletas'] = reparto_modal['bicicletas'].round(2)
reparto_modal['motocicletas'] = reparto_modal['motocicletas'].round(2)
reparto_modal['autos'] = reparto_modal['autos'].round(2)

bar_reparto = px.bar(reparto_modal.T, template = 'plotly_white')

bar_reparto.update_layout(xaxis={'categoryorder':'total descending'},
                          showlegend = False,
                          uniformtext_minsize = 8,
                          uniformtext_mode = 'hide')

bar_reparto.update_xaxes(showgrid = False,
                         showline = True, 
                         title_text = '')

bar_reparto.update_yaxes(title_text = '')

bar_reparto.update_traces(texttemplate='<b>%{y}</b>%',
                          textposition='outside',
                          hovertemplate = None,
                          hoverinfo = 'skip')

#----------------

mes_peatones = ficha_alfonso.drop(['semana', 'fecha', 'dia_semana', 'hora', 'child', 
                      'car', 'pickup', 'van', 'truck', 'bus'], axis = 1)
mes_peatones = mes_peatones.loc[:, ~mes_peatones.columns.str.contains("avg")]
mes_peatones = mes_peatones.groupby('mes', as_index = False, sort = False).sum()

genero = [sum(mes_peatones['hombre']), sum(mes_peatones['mujer'])]

genero_peatones = pd.DataFrame()
genero_peatones['genero'] = ['hombre', 'mujer']
genero_peatones['cuenta'] = genero

pie_peatones = px.pie(genero_peatones, values = 'cuenta', names = 'genero')

#----------

# Display tabs
def render_alfonsoreyes(tab):
    if tab == 'alfonsoreyes_1':
        return alfonsoreyes_1()
    elif tab == 'fichatecnica_conteo':
        return fichatecnica_conteo()
    elif tab == 'fichatecnica_vel':
        return fichatecnica_vel()
    elif tab == 'fichatecnica_reparto':
        return fichatecnica_reparto()










