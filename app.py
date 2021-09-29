import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output, State
import dash_auth


app = dash.Dash(__name__, title='Centro de Gestión de Movilidad',
				external_stylesheets = [dbc.themes.BOOTSTRAP],
				meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'},])



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
	render_opciones)


# App Layout

app.layout = html.Div([

	dbc.NavbarSimple(
		[

			dbc.Button('Alfonso Reyes', href = '/apps/alfonsoreyes', color = 'light',
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


if __name__ == '__main__':
	app.run_server(debug=True)