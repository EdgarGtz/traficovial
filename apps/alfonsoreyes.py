from re import template
import dash
from dash_bootstrap_components._components.Card import Card
from dash_bootstrap_components._components.CardBody import CardBody
from dash_bootstrap_components._components.Row import Row
from dash_bootstrap_components._components.Tab import Tab
import dash_core_components as dcc
from dash_core_components.Graph import Graph
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Br import Br
from dash_html_components.Col import Col
from dash_html_components.Div import Div
from dash_html_components.H3 import H3
from dash_html_components.H5 import H5
from dash_html_components.I import I
from dash_html_components.P import P
from dash_html_components.Span import Span
from dash_html_components.Table import Table
import plotly.express as px
import plotly.graph_objs as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import geopandas as gpd
from datetime import datetime as dt
import numpy as np
from datetime import timedelta
import shapely.geometry
import base64

#------------------------------------------------------------------------------

## Layout General

def alfonsoreyes():

    return html.Div([

        # Tabs
        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            
                            # Indicadores Generales
                            dbc.Tab(label = 'Inicio',
                                    tab_id = 'fichatecnica_inicio',
                                    disabled = False),
                            
                            # Datos Bicicletas
                            dbc.Tab(
                                label = 'Bicicletas',
                                tab_id = 'fichatecnica_bicicletas',
                                disabled = False
                            ),

                            # Datos Peatones
                            dbc.Tab(
                                label = 'Peatones',
                                tab_id = 'fichatecnica_peatones',
                                disabled = False
                            ),

                            # Datos Veh??culos Motorizados
                            dbc.Tab(
                                label = 'Veh??culos Motorizados',
                                tab_id = 'fichatecnica_motorizados',
                                disabled = False
                            ),
                                                        
                            # Gr??ficas de Reparto Modal
                            dbc.Tab(label = 'Reparto Modal',
                                    tab_id = 'fichatecnica_reparto',
                                    disabled = False),

                            # Gr??ficas de Velocidad Promedio
                            dbc.Tab(label = 'Velocidad',
                                    tab_id = 'fichatecnica_vel',
                                    disabled = False),

                            # Hechos Viales
                            dbc.Tab(label = 'Hechos Viales',
                                    tab_id = 'fichatecnica_hv',
                                    disabled = False),
                            
                            # Gr??ficas Pre-JL
                            #dbc.Tab(label = 'Conteo y Velocidad',
                            #        tab_id = 'alfonsoreyes_1',
                            #        disabled = True)
                        ],
                        id='tabs',
                        active_tab = 'fichatecnica_inicio',
                        card = True
                        )
                    ),
                    dbc.CardBody(
                        html.Div(id = 'alfonsoreyes_content')
                    )
                ]), lg = 12

            ), justify = 'center'

        ),

        # Footer 
        dbc.Row([
            dbc.Col(
                html.H6('Instituto Municipal de Planeaci??n y Gesti??n Urbana')),
            dbc.Col(
                html.H6('San Pedro Garza Garc??a, Nuevo Le??n, M??xico',
                        style = {'textAlign': 'right'}))
        ],
        className='px-3 py-4',
        style={'background-color': 'black',
                'color': 'white'})

    ])


#------------------------------------------------------------------------------

## Display Tabs

def render_alfonsoreyes(tab):
    if tab == 'fichatecnica_inicio':
        return fichatecnica_inicio()
    elif tab == 'fichatecnica_bicicletas':
        return fichatecnica_bicicletas()
    elif tab == 'fichatecnica_peatones':
        return fichatecnica_peatones()
    elif tab == 'fichatecnica_motorizados':
        return fichatecnica_motorizados()
    elif tab == 'fichatecnica_vel':
        return fichatecnica_vel()
    elif tab == 'fichatecnica_reparto':
        return fichatecnica_reparto()
    elif tab == 'fichatecnica_hv':
        return fichatecnica_hv()
    #elif tab == 'alfonsoreyes_1':
    #    return alfonsoreyes_1()

#------------------------------------------------------------------------------

## Fotos

# Bot??n de info
img2 = 'assets/informacion.png' # replace with your own image
encoded_img2 = base64.b64encode(open(img2, 'rb').read()).decode('ascii')

#------------------------------------------------------------------------------

## Layout Ficha T??cnica - Inicio

def fichatecnica_inicio():
    return html.Div([
        
        dbc.Row([
            
            # Tarjetas con Indicadores
            dbc.Col([
                
                # Indicador de Bicicletas
                dbc.Row([

                    dbc.Col([

                        dbc.Card([

                            dbc.CardBody([

                                html.Div([
                                    
                                    # Bot??n de m??s informaci??n
                                    html.Span([
                                        
                                        dbc.Button(
                                            html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_bici", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                className='rounded-circle'
                                        ),  
                                    ], id = 'tooltip-target-bici'),

                                    dbc.Tooltip(
                                        'M??s informaci??n',
                                        target = 'tooltip-target-bici'
                                    ),

                                    dbc.Modal([

                                        dbc.ModalHeader(html.B('Bicicletas por D??a')),

                                        dbc.ModalBody([
                                            html.P(
                                                'Promedio de bicicletas por d??a tomado de la semana anterior (Lunes a Domingo).'
                                            ),
                                            html.P(
                                                'El cambio porcentual se obtiene comparando el promedio de la semana anterior contra el de hace 2 semanas.'
                                            )
                                        ]),

                                        dbc.ModalFooter([
                                            dbc.Button(
                                                "Cerrar", 
                                                id="close1_bici", 
                                                className="ml-auto btn btn-secondary", 
                                                n_clicks=0
                                            )
                                        ])
                                    ],
                                    id="modal_bici",
                                    centered=True,
                                    size="lg",
                                    is_open=False),

                                    html.P(
                                        ' Bicicletas por D??a', style={'width':'90%','float':'left'}, className='pl-1'
                                    )
                                ]),

                                # Indicador
                                html.Div([
                                    html.H1(str(int(dias_alfonso['bicycle'].iloc[-5:].mean().round())),
                                    style = {'float': 'left'}
                                    ),
                                    html.H6(
                                    str(int((((dias_alfonso['bicycle'].iloc[-5:].mean() / dias_alfonso['bicycle'].iloc[-10:-5].mean()) - 1) * 100).round())) + '%',
                                    style = {'color': 'green',
                                            'float': 'left'},
                                    className = 'pt-4 pl-2'
                                    )
                                ])
                            ])
                        ])
                    ])
                ]),

                html.Br(),

                # Indicador de Peatones
                dbc.Row([

                    dbc.Col([

                        dbc.Card([

                            dbc.CardBody([

                               html.Div([
                                    
                                    # Bot??n de m??s informaci??n
                                    html.Span([
                                        
                                        dbc.Button(
                                            html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_peatones", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                className='rounded-circle'
                                        ),  
                                    ], id = 'tooltip-target-peatones'),

                                    dbc.Tooltip(
                                        'M??s informaci??n',
                                        target = 'tooltip-target-peatones'
                                    ),

                                    dbc.Modal([

                                        dbc.ModalHeader(html.B('Peatones por D??a')),

                                        dbc.ModalBody([
                                            html.P(
                                                'Promedio de peatones por d??a tomado de la semana anterior (Lunes a Domingo).'
                                            ),
                                            html.P(
                                                'El cambio porcentual se obtiene comparando el promedio de la semana anterior contra el de hace 2 semanas.'
                                            )
                                        ]),

                                        dbc.ModalFooter([
                                            dbc.Button(
                                                "Cerrar", 
                                                id="close1_peatones", 
                                                className="ml-auto btn btn-secondary", 
                                                n_clicks=0
                                            )
                                        ])
                                    ],
                                    id="modal_peatones",
                                    centered=True,
                                    size="lg",
                                    is_open=False),

                                    html.P(
                                        ' Peatones por D??a', style={'width':'90%','float':'left'}, className='pl-1'
                                    )
                                ]),

                                # Indicador
                                html.Div([
                                    html.H1(str(int(dias_alfonso['peatones'].iloc[-5:].mean().round())),
                                    style = {'float': 'left'}),
                                    html.H6(
                                    str(int((((dias_alfonso['peatones'].iloc[-5:].mean() / dias_alfonso['peatones'].iloc[-10:-5].mean()) - 1) * 100).round())) + '%',
                                    style = {'color': 'green',
                                             'float': 'left'},
                                    className = 'pt-4 pl-2'
                                    )
                                ])  
                            ])
                        ])
                    ]) 
                ]),

                html.Br(),

                # Indicador de Bicicletas
                dbc.Row([

                    dbc.Col([

                        dbc.Card([

                            dbc.CardBody([

                                html.Div([
                                    
                                    # Bot??n de m??s informaci??n
                                    html.Span([
                                        
                                        dbc.Button(
                                            html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_vel", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                className='rounded-circle'
                                        ),  
                                    ], id = 'tooltip-target-vel'),

                                    dbc.Tooltip(
                                        'M??s informaci??n',
                                        target = 'tooltip-target-vel'
                                    ),

                                    dbc.Modal([

                                        dbc.ModalHeader(html.B('Velocidad Promedio de Autos')),

                                        dbc.ModalBody([
                                            html.P(
                                                'Velocidad promedio de autos por d??a tomado de la semana anterior (Lunes a Domingo).'
                                            ),
                                            html.P(
                                                'El cambio porcentual se obtiene comparando el promedio de la semana anterior contra el de hace 2 semanas.'
                                            )
                                        ]),

                                        dbc.ModalFooter([
                                            dbc.Button(
                                                "Cerrar", 
                                                id="close1_vel", 
                                                className="ml-auto btn btn-secondary", 
                                                n_clicks=0
                                            )
                                        ])
                                    ],
                                    id="modal_vel",
                                    centered=True,
                                    size="lg",
                                    is_open=False),

                                    html.P(
                                        'Velocidad Promedio de Autos', style={'width':'90%','float':'left'}, className='pl-1'
                                    )
                                ]),

                                # Indicador
                                html.Div([

                                    html.H1(str(int(vel_dia['avg_vel_car'].iloc[-5:].mean().round())) + ' km/h',
                                    style = {'float': 'left'}),
                                    html.H6(
                                    '+' + str(int((((vel_dia['avg_vel_car'].iloc[-5:].mean() / vel_dia['avg_vel_car'].iloc[-10:-5].mean()) - 1) * 100).round())) + '%',
                                    style = {'color': 'red', 'float': 'left'},
                                    className = 'pt-4 pl-2'
                                    )
                                ]) 
                            ])
                        ])
                    ])  
                ]),

                html.Br(),

                # Periodo de Datos
                dbc.Row([

                    dbc.Col([

                        dbc.Card([

                            dbc.CardBody(
                                'Datos del 26 de julio al 19 de septiembre del 2021, capturados desde las 5 am hasta las 12 am (19 horas).',
                                style = {'fontSize': 13.5}
                            )
                        ])
                    ])
                ])
            ]),

            # Mapa
            dbc.Col([

                dbc.Card([

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'mapa_vialibre',
                            figure = mapa_vialibre,
                            config = {
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False,
                                'displayModeBar': False
                            },
                            className = 'h-100 w-100'
                        )
                    ], style={'padding':'10px'})
                ])
            ], width = 9)
        ])
    ])

#------------------------------------------------------------------------------

## Figuras Ficha T??cnica - Inicio

# MODALS PARA TARJETAS DE INDICADORES

def toggle_modal_bici(open1_bici, close1_bici, modal_bici):
    if open1_bici or close1_bici:
        return not modal_bici
    return modal_bici

def toggle_modal_peatones(open1_peatones, close1_peatones, modal_peatones):
    if open1_peatones or close1_peatones:
        return not modal_peatones
    return modal_peatones


def toggle_modal_vel(open1_vel, close1_vel, modal_vel):
    if open1_vel or close1_vel:
        return not modal_vel
    return modal_vel

# MAPA

# Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

# Lectura de Datos
sendas_punto = gpd.read_file('assets/las_sendas.geojson')
vialibre_linea = gpd.read_file('assets/vialibre.geojson')

# Limpieza y Procesamiento de L??neas
lats = []
lons = []
names = []

for feature, name in zip(vialibre_linea.geometry, vialibre_linea.name):
    if isinstance(feature, shapely.geometry.linestring.LineString):
        linestrings = [feature]
    elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
        linestrings = feature.geoms
    else:
        continue
    for linestring in linestrings:
        x, y = linestring.xy
        lats = np.append(lats, y)
        lons = np.append(lons, x)
        names = np.append(names, [name]*len(y))
        lats = np.append(lats, None)
        lons = np.append(lons, None)
        names = np.append(names, None)

# Mapa con L??nea
mapa_vialibre = go.Figure(
    px.line_mapbox(
        lat = lats,
        lon = lons,
        hover_name = names,
        zoom = 14,
        center = {
            'lat': 25.65499,
            'lon': -100.4035
        }
    )
)

mapa_vialibre.update_traces(
    hovertemplate = '<b>V??a Libre (Fase 1)</b><br><extra></extra>',
    showlegend = True,
    name = 'V??a Libre (Fase 1)'
)

# Mapa con Punto
sendas = px.scatter_mapbox(
    sendas_punto,
    lat = sendas_punto.geometry.y,
    lon = sendas_punto.geometry.x
)

sendas.update_traces(
    hovertemplate = '<b>Alfonso Reyes con Las Sendas</b><br><extra></extra>',
    showlegend = True,
    name = 'C??mara Vial Inteligente'
)

# Juntamos Capas
mapa_vialibre.add_trace(sendas.data[0])

mapa_vialibre.update_layout(
    mapbox = dict(
        accesstoken = mapbox_access_token,
        style = 'dark'
    ),
    height = 800,
    hovermode = 'closest',
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
)

mapa_vialibre.update_traces(
    marker_color="#c6cc14",
    marker_size = 20
)

mapa_vialibre.update_layout(
    legend = dict(
        yanchor = "top",
        y = 0.99,
        xanchor = "right",
        x = 0.99,
        font = dict(
            family = 'Helvetica',
            color = 'white'
        ),
        bgcolor = 'rgba(128, 128, 128, 0.4)'
    ),
    margin = dict(autoexpand = False),
    autosize = True
)


#------------------------------------------------------------------------------

## Layout Ficha T??cnica - Bicicletas

def fichatecnica_bicicletas():
    return html.Div([
        
        # Gr??fica de Bicicletas por Semana
        dbc.Row([

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Bicicletas por Semana (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'bici_semana',
                            figure = bici_semana,
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
            
            # Gr??fica de Bicicletas por D??a de la Semana
            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Bicicletas por D??a de la Semana (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'bici_diasemana',
                            figure = bici_diasemana,
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

            # Gr??fica de Bicicletas por Hora
            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Bicicletas por Hora (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'bici_hora',
                            figure = bici_hora,
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
        ])
    ])

#------------------------------------------------------------------------------

## Layout Ficha T??cnica - Peatones

def fichatecnica_peatones():
    return html.Div([
        
        # Gr??fica de Peatones por Semana
        dbc.Row([

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Peatones por Semana (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'peatones_semana',
                            figure = peatones_semana,
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
            
            # Gr??fica de Peatones por D??a de la Semana
            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Peatones por D??a de la Semana (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'peatones_diasemana',
                            figure = peatones_diasemana,
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

            # Gr??fica de Peatones por Hora
            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Peatones por Hora (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'peatones_hora',
                            figure = peatones_hora,
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
                        'G??nero de Peatones (Entre Semana)'
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
            ]),

            dbc.Col([])
        ])
    ])


#------------------------------------------------------------------------------

## Layout Ficha T??cnica - Motorizados

def fichatecnica_motorizados():
    return html.Div([
        
        # Gr??fica de Motorizados por Semana
        dbc.Row([

            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Veh??culos Motorizados por Semana (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'motorizados_semana',
                            figure = motorizados_semana,
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
            
            # Gr??fica de Motorizados por D??a de la Semana
            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Veh??culos Motorizados por D??a de la Semana (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'motorizados_diasemana',
                            figure = motorizados_diasemana,
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

            # Gr??fica de Motorizados por Hora
            dbc.Col([

                dbc.Card([

                    dbc.CardHeader(
                        'Veh??culos Motorizados por Hora (Entre Semana)'
                    ),

                    dbc.CardBody([

                        dcc.Graph(
                            id = 'motorizados_hora',
                            figure = motorizados_hora,
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
        ])
    ])

#------------------------------------------------------------------------------

## Figuras - Ficha T??nica - Conteo de Bicicletas, Peatones y Motorizados

# Lectura de datos de la ficha t??cnica
ficha_alfonso = pd.read_csv('assets/base_conteo_vel.csv')

# Filtrado entre semana
ficha_alfonso = ficha_alfonso[ficha_alfonso['dia_semana'] != 's??bado']
ficha_alfonso = ficha_alfonso[ficha_alfonso['dia_semana'] != 'domingo']

# Datos de conteo semanales
semana_alfonso = ficha_alfonso.drop(['mes', 'semana', 'dia_semana', 'hora'], axis = 1)
semana_alfonso = semana_alfonso.loc[:, ~semana_alfonso.columns.str.contains("avg")]
semana_alfonso['fecha'] = pd.to_datetime(semana_alfonso['fecha'], dayfirst = True)
semana_alfonso = semana_alfonso.groupby('fecha', as_index = False).sum()
semana_alfonso['motorizados'] = semana_alfonso['motorcycle'] + semana_alfonso['autos'] + semana_alfonso['bus']

semana_alfonso['semana'] = semana_alfonso['fecha'].dt.isocalendar().week + 1
semana_alfonso = semana_alfonso.groupby(['semana', 'fecha'], as_index = False).sum()

df_fechas = semana_alfonso['fecha']
df_fechas = df_fechas.dt.strftime('%m-%d')

semana_alfonso = semana_alfonso.drop('fecha', axis = 1)
semana_alfonso = semana_alfonso.groupby('semana', as_index = False).sum()

fecha_inicio = df_fechas.iloc[::5]
fecha_fin = df_fechas.iloc[4::5]
fecha_inicio = fecha_inicio.reset_index()
fecha_fin = fecha_fin.reset_index()
fecha_inicio = fecha_inicio.drop('index', axis = 1)
fecha_fin = fecha_fin.drop('index', axis = 1)

semana_alfonso['fecha_inicio'] = fecha_inicio['fecha']
semana_alfonso['fecha_fin'] = fecha_fin['fecha']
semana_alfonso['semana_fecha'] = semana_alfonso['fecha_inicio'].astype(str) + ' - ' + semana_alfonso['fecha_fin'].astype(str)
semana_alfonso = semana_alfonso.drop(['semana', 'fecha_inicio', 'fecha_fin'], axis = 1)

# Datos de conteo por d??a de la semana
diasemana_alfonso = ficha_alfonso.drop(['mes', 'semana', 'dia_semana', 'hora'], axis = 1)
diasemana_alfonso = diasemana_alfonso.loc[:, ~diasemana_alfonso.columns.str.contains("avg")]
diasemana_alfonso['fecha'] = pd.to_datetime(diasemana_alfonso['fecha'], dayfirst = True)
diasemana_alfonso = diasemana_alfonso.groupby('fecha', as_index = False).sum()
diasemana_alfonso['dia_semana'] = diasemana_alfonso['fecha'].dt.day_name()
diasemana_alfonso = diasemana_alfonso.drop('fecha', axis = 1)
diasemana_alfonso['dia_semana'] = diasemana_alfonso['dia_semana'].astype(str)
diasemana_alfonso = diasemana_alfonso.groupby('dia_semana', as_index = False, sort = False).mean()
diasemana_alfonso['motorizados'] = diasemana_alfonso['motorcycle'] + diasemana_alfonso['autos'] + diasemana_alfonso['bus']

# Datos de conteo promedio por hora del d??a
dias_promedio = ficha_alfonso.drop(['mes', 'semana', 'dia_semana', 'fecha'], axis = 1)
dias_promedio = dias_promedio.loc[:, ~dias_promedio.columns.str.contains("avg")]
dias_promedio = dias_promedio.groupby('hora', as_index = False).mean()
dias_promedio['motorizados'] = dias_promedio['motorcycle'] + dias_promedio['autos'] + dias_promedio['bus']

# Datos de conteo diarios
dias_alfonso = ficha_alfonso.drop(['mes', 'semana', 'dia_semana', 'hora'], axis = 1)
dias_alfonso = dias_alfonso.loc[:, ~dias_alfonso.columns.str.contains("avg")]
dias_alfonso['fecha'] = pd.to_datetime(dias_alfonso['fecha'], dayfirst = True)
dias_alfonso = dias_alfonso.groupby('fecha', as_index = False).sum()
dias_alfonso['dia_semana'] = dias_alfonso['fecha'].dt.day_name()
dias_alfonso['motorizados'] = dias_alfonso['motorcycle'] + dias_alfonso['autos'] + dias_alfonso['bus']

### GR??FICAS BICICLETAS

# Gr??fica de Conteo por Semana de Bicicletas
bici_semana = px.line(semana_alfonso, x = 'semana_fecha', y = 'bicycle', 
                      labels = {'fecha': 'Fecha',
                                'bicycle': 'Bicicletas'},
                      template = 'plotly_white')

bici_semana.update_traces(mode = 'markers+lines', fill = 'tozeroy',
                          hovertemplate = '<b>%{y}</b><br>')

bici_semana.update_xaxes(showgrid = False, showline = True,
                         title_text = '')

bici_semana.update_yaxes(title_text = '')

bici_semana.update_layout(hoverlabel = dict(font_size = 16),
                          hoverlabel_align = 'right',
                          hovermode = 'x unified',
                          margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                        )

# Gr??fica de Conteo por D??a de la Semana de Bicicletas
bici_diasemana = px.line(diasemana_alfonso, x = 'dia_semana', y = 'bicycle',
                         labels = {'dia_semana': 'D??a de la Semana',
                         'bicycle': 'Bicicletas'},
                         template = 'plotly_white')

bici_diasemana.update_traces(mode = 'markers+lines', fill='tozeroy',
                             hovertemplate = '<b>%{y}</b><br>')

bici_diasemana.update_xaxes(showgrid = False,
                            showline = True,
                            title_text = '')

bici_diasemana.update_yaxes(title_text = '')

bici_diasemana.update_layout(hoverlabel = dict(font_size = 16),
                             hoverlabel_align = 'right',
                             hovermode = 'x unified',
                             margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                            )

# Gr??fica de Conteo por D??a de Bicicletas
bici_dia = px.line(dias_alfonso, x = 'fecha', y = 'bicycle',
                   labels = {'fecha': 'Fecha',
                             'bicycle': 'Bicicletas'},
                   template = 'plotly_white',
                   hover_data = ['dia_semana'])

bici_dia.update_traces(mode = 'markers+lines', fill = 'tozeroy',
                       hovertemplate = '<b>%{y}</b><br>' + dias_alfonso['dia_semana'])

bici_dia.update_xaxes(showgrid = False, showline = True,
                      title_text = '')

bici_dia.update_yaxes(title_text = '')

bici_dia.update_layout(hoverlabel = dict(font_size = 16),
                       hoverlabel_align = 'right',
                       hovermode = 'x unified',
                       margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                       )

#Gr??fica de Conteo Promedio por Hora de Bicicletas
bici_hora = px.line(dias_promedio, x = 'hora', y = 'bicycle',
                    labels = {'fecha': 'Fecha',
                              'bicycle': 'Bicicletas'},
                    template = 'plotly_white')

bici_hora.update_traces(mode = 'markers+lines', fill = 'tozeroy',
                        hovertemplate = '<b>%{y}</b><br>')

bici_hora.update_xaxes(showgrid = False,
                       showline = True,
                       title_text = '')

bici_hora.update_yaxes(title_text = '')

bici_hora.update_layout(hoverlabel = dict(font_size = 16),
                        hoverlabel_align = 'right',
                        hovermode = 'x unified',
                        margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                        )

## GR??FICAS PEATONES

#Gr??fica de Conteo por Semana de Peatones
peatones_semana = px.line(semana_alfonso, x = 'semana_fecha', y = 'peatones',
                            labels = {'fecha': 'Fecha', 
                                      'peatones': 'Peatones'},
                            template = 'plotly_white')

peatones_semana.update_traces(mode = 'markers+lines', fill='tozeroy',
                                hovertemplate = '<b>%{y}</b><br>')

peatones_semana.update_xaxes(showgrid = False, 
                               showline = True,
                               title_text = '')

peatones_semana.update_yaxes(title_text = '')

peatones_semana.update_layout(hoverlabel = dict(font_size = 16),
                                hoverlabel_align = 'right', 
                                hovermode = 'x unified',
                                margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                                )

# Gr??fica de Conteo por D??a de la Semana de Peatones
peatones_diasemana = px.line(diasemana_alfonso, x = 'dia_semana', y = 'peatones',
                             labels = {'dia_semana': 'D??a de la Semana', 
                                       'peatones': 'Peatones'},
                             template = 'plotly_white')

peatones_diasemana.update_traces(mode = 'markers+lines', fill='tozeroy',
                                 hovertemplate = '<b>%{y}</b><br>')

peatones_diasemana.update_xaxes(showgrid = False, 
                                showline = True,
                                title_text = '')

peatones_diasemana.update_yaxes(title_text = '')

peatones_diasemana.update_layout(hoverlabel = dict(font_size = 16),
                                 hoverlabel_align = 'right', 
                                 hovermode = 'x unified',
                                 margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                                 )

# Gr??fica de Conteo por D??a de Peatones
peatones_dia = px.line(dias_alfonso, x = 'fecha', y = 'peatones',
                        labels = {'fecha': 'Fecha', 
                                    'peatones': 'Peatones'},
                        template = 'plotly_white',
                        hover_data = ['dia_semana'])

peatones_dia.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>' +  dias_alfonso['dia_semana'])

peatones_dia.update_xaxes(showgrid = False, 
                            showline = True,
                            title_text = '')

peatones_dia.update_yaxes(title_text = '')

peatones_dia.update_layout(hoverlabel = dict(font_size = 16),
                            hoverlabel_align = 'right', 
                            hovermode = 'x unified',
                            margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                            )

# Gr??fica de Conteo por Hora de Peatones
peatones_hora = px.line(dias_promedio, x = 'hora', y = 'peatones',
                        labels = {'fecha': 'Fecha', 
                                    'bicycle': 'Peatones'},
                        template = 'plotly_white')

peatones_hora.update_traces(mode = 'markers+lines', fill='tozeroy',
                            hovertemplate = '<b>%{y}</b><br>')

peatones_hora.update_xaxes(showgrid = False, 
                            showline = True,
                            title_text = '')

peatones_hora.update_yaxes(title_text = '')

peatones_hora.update_layout(hoverlabel = dict(font_size = 16),
                            hoverlabel_align = 'right', 
                            hovermode = 'x unified',
                            margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                            )

## GR??FICAS VEH??CULOS MOTORIZADOS

# Gr??fica de Conteo por Semana de Motorizados
motorizados_semana = px.line(semana_alfonso, x = 'semana_fecha', y = 'motorizados',
                            labels = {'fecha': 'Fecha', 
                                    'motorizados': 'Veh??culos Motorizados'},
                            template = 'plotly_white')

motorizados_semana.update_traces(mode = 'markers+lines', fill='tozeroy',
                                hovertemplate = '<b>%{y}</b><br>')

motorizados_semana.update_xaxes(showgrid = False, 
                                showline = True,
                                title_text = '')

motorizados_semana.update_yaxes(title_text = '')

motorizados_semana.update_layout(hoverlabel = dict(font_size = 16),
                                hoverlabel_align = 'right', 
                                hovermode = 'x unified',
                                margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                                )

# Gr??fica de Conteo por D??a de la Semana de Motorizados
motorizados_diasemana = px.line(diasemana_alfonso, 
                                x = 'dia_semana', y = 'motorizados',
                                labels = {'dia_semana': 'D??a de la Semana', 
                                        'motorizados': 'Veh??culos Motorizados'},
                                template = 'plotly_white')

motorizados_diasemana.update_traces(mode = 'markers+lines', fill='tozeroy',
                                    hovertemplate = '<b>%{y}</b><br>')

motorizados_diasemana.update_xaxes(showgrid = False, 
                                    showline = True,
                                    title_text = '')

motorizados_diasemana.update_yaxes(title_text = '')

motorizados_diasemana.update_layout(hoverlabel = dict(font_size = 16),
                                    hoverlabel_align = 'right', 
                                    hovermode = 'x unified',
                                    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                                    )

# Gr??fica de Conteo por D??a de Motorizados
motorizados_dia = px.line(dias_alfonso, x = 'fecha', y = 'motorizados',
                            labels = {'fecha': 'Fecha', 
                                        'motorizados': 'Veh??culos Motorizados'},
                            template = 'plotly_white',
                            hover_data = ['dia_semana'])

motorizados_dia.update_traces(mode = 'markers+lines', fill='tozeroy',
                            hovertemplate = '<b>%{y}</b><br>' +  dias_alfonso['dia_semana'])

motorizados_dia.update_xaxes(showgrid = False, 
                             showline = True,
                             title_text = '')

motorizados_dia.update_yaxes(title_text = '')

motorizados_dia.update_layout(hoverlabel = dict(font_size = 16),
                                hoverlabel_align = 'right', 
                                hovermode = 'x unified',
                                margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                                )

#Gr??fica de conteo promedio por hora del d??a de motorizados
motorizados_hora = px.line(dias_promedio, x = 'hora', y = 'motorizados',
                            labels = {'fecha': 'Fecha', 
                                        'motorizados': 'Veh??culos Motorizados'},
                            template = 'plotly_white')

motorizados_hora.update_traces(mode = 'markers+lines', fill='tozeroy',
                                hovertemplate = '<b>%{y}</b><br>')

motorizados_hora.update_xaxes(showgrid = False, 
                                showline = True,
                                title_text = '')

motorizados_hora.update_yaxes(title_text = '')

motorizados_hora.update_layout(hoverlabel = dict(font_size = 16),
                                hoverlabel_align = 'right', 
                                hovermode = 'x unified',
                                margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                                )

# Datos de Conteo por mes de Peatones
mes_peatones = ficha_alfonso.drop(['semana', 'fecha', 'dia_semana', 'hora', 'child', 
                      'car', 'pickup', 'van', 'truck', 'bus'], axis = 1)
mes_peatones = mes_peatones.loc[:, ~mes_peatones.columns.str.contains("avg")]
mes_peatones = mes_peatones.groupby('mes', as_index = False, sort = False).sum()

# G??nero de Peatones
genero = [sum(mes_peatones['hombre']), sum(mes_peatones['mujer'])]

genero_peatones = pd.DataFrame()
genero_peatones['genero'] = ['hombre', 'mujer']
genero_peatones['cuenta'] = genero

# Gr??fica de G??nero de Peatones
pie_peatones = px.pie(genero_peatones, values = 'cuenta', names = 'genero')

pie_peatones.update_layout(
    margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
)

#------------------------------------------------------------------------------

## Layout Ficha T??cnica - Velocidad

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
                            figure = vel_autos,
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
                        'Informaci??n Adicional'
                    ),

                    dbc.CardBody([
                        'La informaci??n proviene de los datos reportados entre el 26 de julio y el 19 de septiembre en el cruce de Alfonso Reyes y Las Sendas.'
                    ])
                ])
            ])
        ])
    ])


#------------------------------------------------------------------------------

## Figuras Ficha T??cnica - Velocidad

# Indicador de Velocidad Promedio
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

# Datos de Velocidad Promedio de Autos Particulares
vel_alfonso = ficha_alfonso.drop(['fecha', 'mes', 'semana', 'dia_semana',
                                   'child', 'hombre', 'mujer', 'peatones',
                                   'bicycle', 'motorcycle', 'autos', 'pickup',
                                    'van', 'truck', 'autos', 'bus'], axis = 1)

vel_alfonso = vel_alfonso.groupby('hora', as_index = False).mean()

vel_dia = ficha_alfonso.drop(['hora', 'mes', 'semana', 'dia_semana',
                                   'child', 'hombre', 'mujer', 'peatones',
                                   'bicycle', 'motorcycle', 'autos', 'pickup',
                                    'van', 'truck', 'autos', 'bus'], axis = 1)

vel_dia = vel_dia.groupby('fecha', as_index = False).mean()

# Gr??fica de Velocidad Promedio por Hora de Autos Particulares
vel_autos = px.line(vel_alfonso, x = 'hora', y = 'avg_vel_car',
       labels = {'avg_vel_car': 'Velocidad Promedio (km/h)', 'hora': 'Hora'},
       template = 'plotly_white')

vel_autos.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')

vel_autos.update_xaxes(showgrid = False, showline = True,
            title_text = '')

vel_autos.update_yaxes(title_text = '')

vel_autos.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified',
                 margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                 )

#------------------------------------------------------------------------------

# Layout Ficha T??cnica - Reparto Modal

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
            ])
        ]),

        html.Br(),

        dbc.Row([

            dbc.Col([

                dbc.Card([

                   dbc.CardHeader(
                        'Informaci??n Adicional'
                    ),

                    dbc.CardBody([
                        'La informaci??n proviene de los datos reportados entre el 26 de julio y el 19 de septiembre en el cruce de Alfonso Reyes y Las Sendas.'
                    ]) 
                ])
            ])
        ])
    ])

#------------------------------------------------------------------------------

# Datos de Conteo por Mes
mes_alfonso = ficha_alfonso.drop(['semana', 'fecha', 'dia_semana', 
                                  'hora', 'child', 'mujer', 'hombre', 
                                  'car', 'pickup', 'van', 'truck'
                                  ], 
                                  axis = 1
                                )
mes_alfonso = mes_alfonso.loc[:, ~mes_alfonso.columns.str.contains("avg")]
mes_alfonso = mes_alfonso.groupby('mes', as_index = False, sort = False).sum()


peatones = sum(mes_alfonso['peatones'])
bici = sum(mes_alfonso['bicycle'])
moto = sum(mes_alfonso['motorcycle'])
autos = sum(mes_alfonso['autos'])
camiones = sum(mes_alfonso['bus'])
total = peatones + bici + moto + autos + camiones

peatones = [peatones / total]
bici = [bici / total]
moto = [moto / total]
autos = [autos / total]
camiones = [camiones / total]

reparto_modal = pd.DataFrame()
reparto_modal['peatones'] = peatones
reparto_modal['bicicletas'] = bici
reparto_modal['motocicletas'] = moto
reparto_modal['autos'] = autos
reparto_modal['camiones'] = camiones

reparto_modal['peatones'] = reparto_modal['peatones'] * 100
reparto_modal['bicicletas'] = reparto_modal['bicicletas'] * 100
reparto_modal['motocicletas'] = reparto_modal['motocicletas'] * 100
reparto_modal['autos'] = reparto_modal['autos'] * 100
reparto_modal['camiones'] = reparto_modal['camiones'] * 100

reparto_modal['peatones'] = reparto_modal['peatones'].round(2)
reparto_modal['bicicletas'] = reparto_modal['bicicletas'].round(2)
reparto_modal['motocicletas'] = reparto_modal['motocicletas'].round(2)
reparto_modal['autos'] = reparto_modal['autos'].round(2)
reparto_modal['camiones'] = reparto_modal['camiones'].round(2)

reparto_modal['motorizados'] = reparto_modal['autos'] + reparto_modal['motocicletas'] + reparto_modal['camiones']
reparto_modal = reparto_modal.drop(['autos', 'motocicletas', 'camiones'], axis = 1)

# Gr??fica de Reparto Modal
bar_reparto = px.bar(reparto_modal.T, template = 'plotly_white')

bar_reparto.update_layout(xaxis={'categoryorder':'total descending'},
                          showlegend = False,
                          uniformtext_minsize = 8,
                          uniformtext_mode = 'hide',
                          margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                          )

bar_reparto.update_xaxes(showgrid = False,
                         showline = True, 
                         title_text = '')

bar_reparto.update_yaxes(title_text = '')

bar_reparto.update_traces(texttemplate='<b>%{y}</b>%',
                          textposition='outside',
                          hovertemplate = None,
                          hoverinfo = 'skip')

#------------------------------------------------------------------------------

## Layout Ficha T??cnica - Hechos Viales

def fichatecnica_hv():
    return html.Div([

        # Indicadores
        dbc.Row([

            dbc.CardDeck([

                dbc.Card([

                    dbc.CardBody([

                        html.H2('257', className = 'card-title'),
                        html.P(
                            'Hechos viales por a??o (2015-2020)'
                        )
                    ])
                ]),

                dbc.Card([

                    dbc.CardBody([

                        html.H2('6', className = 'card-title'),
                        html.P(
                            'Lesionados por a??o (2015-2020)'
                        )
                    ])
                ]),

                dbc.Card([

                    dbc.CardBody([

                        html.H2('0', className = 'card-title'),
                        html.P(
                            'Fallecidos por a??o (2015-2020)'
                        )
                    ])
                ]),

                dbc.Card([

                    dbc.CardBody([

                        html.H2('5', className = 'card-title'),
                        html.P(
                            'Atropellos a peatones por a??o (2015-2020)'
                        )
                    ])
                ])
            ])
        ], justify = 'center'),

        html.Br(),

        # Gr??fica de Hechos Viales por A??o
        dbc.Row([

            dbc.Col([

               dbc.Card([

                    dbc.CardHeader(
                        'Hechos Viales Totales en V??a Libre por A??o'
                    ),

                    dbc.CardBody(

                        dcc.Graph(

                            id = 'hv_totales',
                            figure = hv_totales,
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
                        'Top 10 Intersecciones con m??s Hechos Viales (2015 - 2020)'
                    ),

                    dbc.CardBody(

                        dcc.Graph(

                            id = 'hv_top10_2',
                            figure = hv_top10_2,
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
            ])
        ]),

        html.Br(),

        # Tipos y Causas de Hechos Viales
        dbc.Row([

            # Tipos de Hechos Viales
            dbc.Col([

               dbc.Card([

                    dbc.CardHeader(
                        'El alcance es el principal tipo de hecho vial en V??a Libre (2015 - 2020)'
                    ),

                    dbc.CardBody([

                        dbc.Table.from_dataframe(hv_tipos, 
                                                 striped = True, 
                                                 bordered = True, 
                                                 hover = True)
                    ])
                ]) 
            ]),

            # Causas de Hechos Viales
            dbc.Col([

               dbc.Card([

                    dbc.CardHeader(
                        'No guardar distancia es la principal causa de hecho vial en V??a Libre (2015 - 2020)'
                    ),

                    dbc.CardBody([

                        dbc.Table.from_dataframe(hv_causas, 
                                                 striped = True, 
                                                 bordered = True, 
                                                 hover = True)
                    ])
                ]) 
            ])
        ]),

        html.Br(),

        # Hechos Viales e Intersecciones
        dbc.Row([

            # Top 10 Intersecciones con m??s hechos viales
            dbc.Col([

               dbc.Card([

                    dbc.CardHeader(
                        'Top 10 Intersecciones con m??s Hechos Viales (2015 - 2020)'
                    ),

                    dbc.CardBody(

                        dcc.Graph(

                            id = 'hv_top10',
                            figure = hv_top10,
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

            # Top 10 Intersecciones con lesionados
            dbc.Col([

               dbc.Card([

                    dbc.CardHeader(
                        'Top 10 Intersecciones con m??s Hechos Viales con al menos un lesionado (2015 - 2020)'
                    ),

                    dbc.CardBody([

                        dbc.Table.from_dataframe(hv_top10_lesionados, 
                                                 striped = True, 
                                                 bordered = True, 
                                                 hover = True)
                    ])
                ]) 
            ])
        ])
    ])

#------------------------------------------------------------------------------

## Figuras Ficha T??cnica - Hechos Viales

# Indicador de Hechos Viales por A??o
prom_hv = go.Figure(go.Indicator(
    mode = "number",
    value = 257,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {"text": "Promedio Anual<br><span style='font-size:0.8em;color:gray'>"}
))

prom_hv.update_layout(
     margin = dict(t=0, l=0, r=0, b=0))

prom_hv.update_traces(selector=dict(type='indicator'))

# Indicador de Lesionados por A??o
prom_lesionados = go.Figure(go.Indicator(
    mode = "number",
    value = 6,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {"text": "Promedio Anual<br><span style='font-size:0.8em;color:gray'>"}
))

prom_lesionados.update_layout(
     margin = dict(t=0, l=0, r=0, b=0))

prom_lesionados.update_traces(selector=dict(type='indicator'))

# Indicador de Fallecidos por A??o
prom_fallecidos = go.Figure(go.Indicator(
    mode = "number",
    value = 0,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {"text": "Promedio Anual<br><span style='font-size:0.8em;color:gray'>"}
))

prom_fallecidos.update_layout(
     margin = dict(t=0, l=0, r=0, b=0))

prom_fallecidos.update_traces(selector=dict(type='indicator'))

# Indicador de Atropellos a Peatones por A??o
prom_atropellos = go.Figure(go.Indicator(
    mode = "number",
    value = 5,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {"text": "Promedio Anual<br><span style='font-size:0.8em;color:gray'>"}
))

prom_atropellos.update_layout(
     margin = dict(t=0, l=0, r=0, b=0))

prom_atropellos.update_traces(selector=dict(type='indicator'))

# Gr??fica de Hechos Viales por A??o en V??a Libre
hv_anual = {'year': [2015, 2016, 2017, 2018, 2019, 2020],
            'hechos_viales': [329, 307, 326, 280, 215, 87]}

hv_anual = pd.DataFrame.from_dict(hv_anual)

hv_totales = px.line(hv_anual, x = 'year', y = 'hechos_viales', 
                      labels = {'year': 'A??o',
                                'hechos_viales': 'Hechos Viales'},
                      template = 'plotly_white')

hv_totales.update_traces(mode = 'markers+lines', fill = 'tozeroy',
                          hovertemplate = '<b>%{y}</b><br>')

hv_totales.update_xaxes(showgrid = False, showline = True,
                         title_text = '')

hv_totales.update_yaxes(title_text = '')

hv_totales.update_layout(hoverlabel = dict(font_size = 16),
                          hoverlabel_align = 'right',
                          hovermode = 'x unified',
                          margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                        )

# Tabla de Tipos de Hechos Viales en V??a Libre
hv_tipos = pd.DataFrame(
    {
        'Tipo de Hecho Vial': ['Alcance', 'Choque de crucero', 'Estrellamiento',
                                'Choque lateral', 'Choque diverso', 'Atropello',
                                'Otros (incendio, choque de frente y de reversa, ca??da de persona)'],
        'Proporci??n': ['52%', '18%', '13%', '13%', '2%', '0.3%', '1.3%']
    }
)

# Tabla de Causas de Hechos Viales en V??a Libre
hv_causas = pd.DataFrame(
    {
        'Causa de Hecho Vial': ['No guardar distancia', 'Invadir carril', 'No respet?? sem??foro',
                                'Otros','Distracci??n', 'Vir?? indebidamente', 'No respet?? alto',
                                'NA', 'Otros (exceso de velocidad, mal estacionado, estado alcoh??lico)'],
        'Proporci??n': ['51%', '13%', '12%', '9%', '7%', '5%', '3%', '1%', '1%']
    }
)

# Gr??fica de Top 10 Intersecciones con m??s Hechos Viales
hv_intersecciones = {'interseccion': ['ALFONSO REYES CON NEIL ARMSTRONG',
                                    'ALFONSO REYES CON LAS OLIMPIADAS',
                                    'ALFONSO REYES CON PADRE MIER',
                                    'ALFONSO REYES CON MATAMOROS',
                                    'ALFONSO REYES CON JIMENEZ',
                                    'ALFONSO REYES CON GENARO GARZA GARCIA',
                                    'ALFONSO REYES CON CORREGIDORA',
                                    'ALFONSO REYES CON LAS SENDAS',
                                    'ALFONSO REYES CON BENITO JUAREZ',
                                    'ALFONSO REYES CON MONTE FALCO'],
                    'hechos_viales': [170, 128, 109, 103, 93, 93, 82,
                                    70, 70, 63]}

hv_intersecciones = pd.DataFrame.from_dict(hv_intersecciones)

hv_top10 = px.bar(hv_intersecciones, x = "hechos_viales", y = "interseccion",
                  orientation = 'h',
                  template = 'plotly_white')

hv_top10.update_layout(yaxis={'categoryorder':'total ascending'},
                          showlegend = False,
                          uniformtext_minsize = 8,
                          uniformtext_mode = 'hide')

hv_top10.update_xaxes(showgrid = True,
                         showline = True, 
                         title_text = '')

hv_top10.update_yaxes(title_text = '')

hv_top10.update_traces(texttemplate = '<b>%{x}</b>',
                          textposition = 'inside',
                          hovertemplate = None,
                          hoverinfo = 'skip')

hv_intersecciones2 = {'interseccion': ['NEIL ARMSTRONG', 'LAS OLIMPIADAS',
                                    'PADRE MIER', 'MATAMOROS', 'JIMENEZ',
                                    'GENARO GARZA GARCIA', 'CORREGIDORA',
                                    'LAS SENDAS', 'BENITO JUAREZ', 'MONTE FALCO'],
                    'hechos_viales': [170, 128, 109, 103, 93, 93, 82,
                                    70, 70, 63]}

hv_intersecciones2 = pd.DataFrame.from_dict(hv_intersecciones2)

hv_top10_2 = px.bar(hv_intersecciones2, x = "hechos_viales", y = "interseccion",
                  orientation = 'h',
                  template = 'plotly_white')

hv_top10_2.update_layout(yaxis={'categoryorder':'total ascending'},
                          showlegend = False,
                          uniformtext_minsize = 8,
                          uniformtext_mode = 'hide',
                          margin = dict(t = 0, l = 0, r = 0, b = 0, pad = 0)
                        )

hv_top10_2.update_xaxes(showgrid = True,
                         showline = True, 
                         title_text = '')

hv_top10_2.update_yaxes(title_text = '')

hv_top10_2.update_traces(texttemplate = '<b>%{x}</b>',
                          textposition = 'inside',
                          hovertemplate = None,
                          hoverinfo = 'skip')

# Tabla de Intersecciones con m??s Hechos Viales con al menos un Lesionado
hv_top10_lesionados = pd.DataFrame(
    {
        'Intersecci??n': ['Padre Mier', 'Matamoros', 'Corregidora', 'Las Sendas',
                         'Genaro Garza Garc??a', 'Neil Armstrong', 'Jim??nez', 
                         'Guillermo Prieto', 'Santa B??rbara', 'Las Olimpiadas'],
        'Total Lesionados': [11, 4, 4, 3, 3, 2, 2, 2, 1, 1]
    }
)

#----------------------------------------------------------

## Layout - BiciRuta

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

                # Gr??ficas
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label='Hora', tab_id='hora',
                                disabled = False),
                            dbc.Tab(label = 'D??a', tab_id = 'dia',
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

# Conexi??n entre dropdown de variables y dropdown de modo de transporte
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

# Visualizar gr??ficas de l??nea para conteo y velocidad
def render_conteo(periodo, my_dropdown, my_dropdown_0, start_date, end_date):

    # Diferencia en d??as entre fecha de inicio y fecha final
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

    # Conteo por d??a
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

    # Velocidad por d??a
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
