import dash
import dash_core_components as dcc
from dash_core_components.Graph import Graph
import dash_html_components as html
import dash_bootstrap_components as dbc
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
                            dbc.Tab(label='Conteo y Velocidad', tab_id='alfonsoreyes_1',
                                disabled = False),
                            
                            dbc.Tab(label = 'Ficha Técnica', tab_id = 'fichatecnica',
                                disabled = False)
                        ],
                        id='tabs',
                        active_tab="alfonsoreyes_1",
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
                                disabled = False),
                            dbc.Tab(label = 'Semana', tab_id = 'semana',
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

    # Conteo por semana - una semana o menos
    elif my_dropdown_0 == 'conteo' and periodo == 'semana' and dif_tiempo < 7:

        # Leer csv
        conteo_semana = pd.read_csv('assets/camaras_viales_dia.csv')
        conteo_semana = conteo_semana.iloc[3:]

        # Cambiar variable a datetime
        conteo_semana['dia'] = pd.to_datetime(conteo_semana['dia'],
            dayfirst = True)

        # Duplicar columna de fecha y set index
        conteo_semana['dia1'] = conteo_semana['dia']
        conteo_semana = conteo_semana.set_index('dia')

        # Filtro por calendario
        conteo_semana = conteo_semana.loc[start_date:end_date]

        # Crear df nuevo con suma de selección
        suma = conteo_semana[my_dropdown].sum()
        suma = pd.Series(suma)
        fecha = pd.Series(start_date)
        conteo_semana = pd.DataFrame(dict(fecha = fecha, suma = suma))

        # Graph
        conteo2 = px.scatter(conteo_semana, x = 'fecha', y = 'suma',
            template = 'plotly_white')

        conteo2.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>' + '%{x}')
        conteo2.update_xaxes(showgrid = False, showline = True, title_text = '')
        conteo2.update_yaxes(title_text = '')
        conteo2.update_layout(hoverlabel = dict(font_size =16),
            hoverlabel_align = 'right')

        return conteo2

    # Conteo por semana - más de una semana
    elif my_dropdown_0 == 'conteo' and periodo == 'semana':

        # Leer csv
        conteo_semana = pd.read_csv('assets/camaras_viales_dia.csv')
        conteo_semana = conteo_semana.iloc[3:]

        # Cambiar variable a datetime
        conteo_semana['dia'] = pd.to_datetime(conteo_semana['dia'],
            dayfirst = True)

        # Duplicar columna de fecha y set index
        conteo_semana['dia1'] = conteo_semana['dia']
        conteo_semana = conteo_semana.set_index('dia')

        # Filtro por calendario
        conteo_semana = conteo_semana.loc[start_date:end_date]

        # Variables de fecha para el while loop
        dt_start_date = pd.to_datetime(start_date)
        dt_end_date = pd.to_datetime(end_date)

        # DF que se actualiza con el loop y termina graficado
        conteo_semana_graph = pd.DataFrame(columns = ['fecha', 'suma'])

        while dif_tiempo_loop >= 7:

            # Filtra por la primera semana completa
            conteo_semana_nuevo = conteo_semana.loc[
                dt_start_date: dt_start_date + pd.DateOffset(days = 6)]

            # Suma de variable y actualiza df a graficar
            suma = conteo_semana_nuevo[my_dropdown].sum()
            conteo_semana_graph = conteo_semana_graph.append(
                {'fecha' : dt_start_date, 'suma' : suma}, ignore_index = True)

            # Actualizar variables para el loop
            dt_start_date = dt_start_date + pd.DateOffset(days = 7)
            dif_tiempo_loop = dif_tiempo_loop - 7 

        else:

            # Filtra por los días restantes
            conteo_semana_ultimo = conteo_semana.loc[dt_start_date: dt_end_date]
    
            # Suma de variable y actualiza df a graficar
            suma = conteo_semana_ultimo[my_dropdown].sum()
            conteo_semana_graph = conteo_semana_graph.append(
                {'fecha' : dt_start_date, 'suma' : suma}, ignore_index = True)

        # Graph
        conteo2 = px.scatter(conteo_semana_graph, x = 'fecha', y = 'suma',
            template = 'plotly_white')

        conteo2.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>' + '%{x}')
        conteo2.update_xaxes(showgrid = False, showline = True, title_text = '')
        conteo2.update_yaxes(title_text = '')
        conteo2.update_layout(hoverlabel = dict(font_size =16),
            hoverlabel_align = 'right')

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

    # Velocidad por semana - una semana o menos
    elif my_dropdown_0 == 'velocidad_promedio' and periodo == 'semana' and dif_tiempo < 7:

        # Leer csv
        vel_semana = pd.read_csv('assets/camaras_viales_dia.csv')
        vel_semana = vel_semana.iloc[3:]

        # Cambiar variable a datetime
        vel_semana['dia'] = pd.to_datetime(vel_semana['dia'],
            dayfirst = True)

        # Duplicar columna de fecha y set index
        vel_semana['dia1'] = vel_semana['dia']
        vel_semana = vel_semana.set_index('dia')

        # Filtro por calendario
        vel_semana = vel_semana.loc[start_date:end_date]

        # Crear df nuevo con suma de selección
        mean = vel_semana[my_dropdown].mean()
        mean = pd.Series(mean)
        fecha = pd.Series(start_date)
        vel_semana = pd.DataFrame(dict(fecha = fecha, mean = mean))

        # Graph
        conteo2 = px.scatter(vel_semana, x = 'fecha', y = 'mean', 
            template = 'plotly_white')

        conteo2.update_traces(mode = 'markers+lines',
            fill='tozeroy', hovertemplate = '<b>%{y}</b><br>' + '%{x}')
        conteo2.update_xaxes(showgrid = False, showline = True, title_text = '')
        conteo2.update_yaxes(title_text = '')
        conteo2.update_layout(hoverlabel = dict(font_size = 16),
            hoverlabel_align = 'right')

        return conteo2

    # Velocidad por semana - más de una semana
    elif my_dropdown_0 == 'velocidad_promedio' and periodo == 'semana':

        # Leer csv
        vel_semana = pd.read_csv('assets/camaras_viales_dia.csv')
        vel_semana = vel_semana.iloc[3:]

        # Cambiar variable a datetime
        vel_semana['dia'] = pd.to_datetime(vel_semana['dia'],
            dayfirst = True)

        # Duplicar columna de fecha y set index
        vel_semana['dia1'] = vel_semana['dia']
        vel_semana = vel_semana.set_index('dia')

        # Filtro por calendario
        vel_semana = vel_semana.loc[start_date:end_date]

        # Variables de fecha para el while loop
        dt_start_date = pd.to_datetime(start_date)
        dt_end_date = pd.to_datetime(end_date)

        # DF que se actualiza con el loop y termina graficado
        vel_semana_graph = pd.DataFrame(columns = ['fecha', 'suma'])

        while dif_tiempo_loop >= 7:

            # Filtra por la primera semana completa
            vel_semana_nuevo = vel_semana.loc[
                dt_start_date: dt_start_date + pd.DateOffset(days = 6)]

            # Suma de variable y actualiza df a graficar
            mean = vel_semana_nuevo[my_dropdown].mean()
            vel_semana_graph = vel_semana_graph.append(
                {'fecha' : dt_start_date, 'mean' : mean}, ignore_index = True)

            # Actualizar variables para el loop
            dt_start_date = dt_start_date + pd.DateOffset(days = 7)
            dif_tiempo_loop = dif_tiempo_loop - 7 

        else:

            # Filtra por los días restantes
            vel_semana_ultimo = vel_semana.loc[dt_start_date: dt_end_date]
    
            # Suma de variable y actualiza df a graficar
            mean = vel_semana_ultimo[my_dropdown].mean()
            vel_semana_graph = vel_semana_graph.append(
                {'fecha' : dt_start_date, 'mean' : mean}, ignore_index = True)

        # Graph
        conteo2 = px.scatter(vel_semana_graph, x = 'fecha', y = 'mean',
            template = 'plotly_white')

        conteo2.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>' + '%{x}')
        conteo2.update_xaxes(showgrid = False, showline = True, title_text = '')
        conteo2.update_yaxes(title_text = '')
        conteo2.update_layout(hoverlabel_align = 'right',
            hoverlabel = dict(font_size =16))

        return conteo2


#-------------------------------

# Layout Ficha Técnica
def fichatecnica():

    return html.Div(children = [
        html.Div([
            html.H1(children = 'Vía Libre'),

            html.Div(children = '''
                La información a continuación proviene de los datos reportados entre el 26 de julio y el 19 de septiembre en el cruce de Alfonso Reyes con Las Sendas.
            '''),

            dcc.Graph(
                id = 'bici_semana',
                figure = fig1
            ),

            dcc.Graph(
                id = 'bici_dia',
                figure = fig2
            ),

            dcc.Graph(
                id = 'bici_hora',
                figure = fig3
            ),

            dcc.Graph(
                id = 'peatones_semana',
                figure = fig4
            ),

            dcc.Graph(
                id = 'peatones_dia',
                figure = fig5
            ),

            dcc.Graph(
                id = 'peatones_hora',
                figure = fig6
            )
        ])
    ])

ficha_alfonso = pd.read_csv('assets/base_conteo_vel.csv')

#Datos de conteo semanales
semana_alfonso = ficha_alfonso.drop(['mes', 'hora', 'dia_semana', 'fecha'], axis = 1)
semana_alfonso = semana_alfonso.loc[:, ~semana_alfonso.columns.str.contains("avg")]
semana_alfonso = semana_alfonso.groupby('semana', as_index = False).sum()

#Datos de conteo por día de la semana

#Datos de conteo diarios
dias_alfonso = ficha_alfonso.drop(['mes', 'semana', 'dia_semana', 'hora'], axis = 1)
dias_alfonso = dias_alfonso.loc[:, ~dias_alfonso.columns.str.contains("avg")]
dias_alfonso['fecha'] = pd.to_datetime(dias_alfonso['fecha'], dayfirst = True)
dias_alfonso = dias_alfonso.groupby('fecha', as_index = False).sum()
dias_alfonso['dia_semana'] = dias_alfonso['fecha'].dt.day_name()

#Datos de conteo promedio por hora del día
dias_promedio = ficha_alfonso.drop(['mes', 'semana', 'dia_semana', 'fecha'], axis = 1)
dias_promedio = dias_promedio.loc[:, ~dias_promedio.columns.str.contains("avg")]
dias_promedio = dias_promedio.groupby('hora', as_index = False).mean()

#Gráfica de Conteo por Semana de Bicicletas es fig1
fig1 = px.line(semana_alfonso, x = 'semana', y = 'bicycle',
       labels = {'fecha': 'Fecha', 'bicycle': 'Bicicletas'},
       title = 'Conteo por Semana de Bicicletas',
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
       title = 'Conteo de Bicicletas por Día',
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
       title = 'Conteo Promedio por Hora de Bicicletas',
       template = 'plotly_white')

fig3.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig3.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig3.update_yaxes(title_text = '')
fig3.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#Gráfica de Conteo por Semana de Bicicletas es fig1
fig4 = px.line(semana_alfonso, x = 'semana', y = 'peatones',
       labels = {'fecha': 'Fecha', 'peatones': 'Peatones'},
       title = 'Conteo por Semana de Peatones',
       template = 'plotly_white')

fig4.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig4.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig4.update_yaxes(title_text = '')
fig4.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#Gráfica de conteo por día de bicicletas es fig2
fig5 = px.line(dias_alfonso, x = 'fecha', y = 'peatones',
       labels = {'fecha': 'Fecha', 'peatones': 'Peatones'},
       title = 'Conteo de Peatones por Día',
       template = 'plotly_white',
       hover_data = ['dia_semana'])

fig5.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>' +  dias_alfonso['dia_semana'])
fig5.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig5.update_yaxes(title_text = '')
fig5.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#Gráfica de conteo promedio por hora del día de bicicletas es fig3
fig6 = px.line(dias_promedio, x = 'hora', y = 'peatones',
       labels = {'fecha': 'Fecha', 'bicycle': 'Peatones'},
       title = 'Conteo Promedio por Hora de Peatones',
       template = 'plotly_white')

fig6.update_traces(mode = 'markers+lines', fill='tozeroy',
            hovertemplate = '<b>%{y}</b><br>')
fig6.update_xaxes(showgrid = False, showline = True,
            title_text = '')
fig6.update_yaxes(title_text = '')
fig6.update_layout(hoverlabel = dict(font_size = 16),
                 hoverlabel_align = 'right', hovermode = 'x unified')

#----------

# Display tabs
def render_alfonsoreyes(tab):
    if tab == 'alfonsoreyes_1':
        return alfonsoreyes_1()
    elif tab == 'fichatecnica':
        return fichatecnica()










