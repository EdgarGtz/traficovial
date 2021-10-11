import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output, State
import dash_auth

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

app = dash.Dash(__name__, title='Centro de Gestión de Movilidad',
				external_stylesheets = [dbc.themes.BOOTSTRAP, FONT_AWESOME],
				meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'},],)



app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-2FB009N3XV"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-2FB009N3XV');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

server = app.server

# Connect to app pages
from apps import home
from apps.alfonsoreyes import (alfonsoreyes, render_alfonsoreyes, render_conteo,
	render_opciones, toggle_modal_bici, toggle_modal_peatones, toggle_modal_vel, 
    toggle_modal_bicisemana, toggle_modal_bicidia, toggle_modal_bicihora)


# App Layout

app.layout = html.Div([

	dbc.NavbarSimple(
		[

			dbc.Button('Vía Libre', href = '/apps/alfonsoreyes', color = 'light',
				disabled = False)

		],
		brand='CGM',
		brand_href='/apps/home'
	),

	html.Div(id='page-content', children=[]),
	dcc.Location(id='url', refresh=False)

])


# Display main pages

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])

def display_page(pathname):
	if pathname == '/apps/alfonsoreyes':
		return alfonsoreyes()
	else:
		return home.layout

#----------

# Opciones
@app.callback(
	Output('my_dropdown', 'options'),
 	Input('my_dropdown_0', 'value'))

def get_opciones(tab):
    return render_opciones(tab)


# Conteo y Velocidades

@app.callback(
	Output('conteo2', 'figure'),
	[Input('periodo', 'active_tab'),
	Input('my_dropdown', 'value'),
	Input('my_dropdown_0', 'value'),
	Input('calendario', 'start_date'),
	Input('calendario', 'end_date')])

def get_conteo1(tab, tab1, tab2, tab3, tab4):
    return render_conteo(tab, tab1, tab2, tab3, tab4)


# Alfonso Reyes - General

@app.callback(Output('alfonsoreyes_content', 'children'), 
	[Input('tabs', 'active_tab')])

def get_ayuda(tab):
    return render_alfonsoreyes(tab)

#----------------------------------------------------------

# MODAL BICICLETAS INICIO
@app.callback(
    Output("modal_bici", "is_open"),
    [Input("open1_bici", "n_clicks"), 
    Input("close1_bici", "n_clicks")],
    [State("modal_bici", "is_open")],)

def toggle_modal_bici(open1_bici, close1_bici, modal_bici):
    if open1_bici or open1_bici:
        return not modal_bici
    return modal_bici

# MODAL PEATONES INICIO
@app.callback(
    Output("modal_peatones", "is_open"),
    [Input("open1_peatones", "n_clicks"), 
    Input("close1_peatones", "n_clicks")],
    [State("modal_peatones", "is_open")],)

def toggle_modal_peatones(open1_peatones, close1_peatones, modal_peatones):
    if open1_peatones or close1_peatones:
        return not modal_peatones
    return modal_peatones

# MODAL VELOCIDAD INICIO
@app.callback(
    Output("modal_vel", "is_open"),
    [Input("open1_vel", "n_clicks"), 
    Input("close1_vel", "n_clicks")],
    [State("modal_vel", "is_open")],)

def toggle_modal_vel(open1_vel, close1_vel, modal_vel):
    if open1_vel or close1_vel:
        return not modal_vel
    return modal_vel

# MODAL BICIS POR SEMANA

@app.callback(
    Output("modal_bicisemana", "is_open"),
    [Input("open1_bicisemana", "n_clicks"), 
    Input("close1_bicisemana", "n_clicks")],
    [State("modal_bicisemana", "is_open")],)

def toggle_modal_bicisemana(open1_bicisemana, close1_bicisemana, modal_bicisemana):
    if open1_bicisemana or close1_bicisemana:
        return not modal_bicisemana
    return modal_bicisemana

# MODAL BICIS POR DIA

@app.callback(
    Output("modal_bicidia", "is_open"),
    [Input("open1_bicidia", "n_clicks"), 
    Input("close1_bicidia", "n_clicks")],
    [State("modal_bicidia", "is_open")],)

def toggle_modal_bicidia(open1_bicidia, close1_bicidia, modal_bicidia):
    if open1_bicidia or close1_bicidia:
        return not modal_bicidia
    return modal_bicidia

# MODAL BICIS POR HORA

@app.callback(
    Output("modal_bicihora", "is_open"),
    [Input("open1_bicihora", "n_clicks"), 
    Input("close1_bicihora", "n_clicks")],
    [State("modal_bicihora", "is_open")],)

def toggle_modal_bicihora(open1_bicihora, close1_bicihora, modal_bicihora):
    if open1_bicihora or close1_bicihora:
        return not modal_bicihora
    return modal_bicihora


#----------------------------------------------------------

if __name__ == '__main__':
	app.run_server(debug=True)

