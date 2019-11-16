import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_daq as daq

from clean_honey_data import *
import pandas as pd

external_stylesheets_ = ['https://codepen.io/amyoshino/pen/jzXypZ.css']


all_data = get_data()
colony_data = all_data[1]
period_vals = list(colony_data.period.unique())
slider_markers = {i+1: period_vals[i] for i in range(len(period_vals))}
stressors = ["varroa_mites", "other_pests", "other", "pesticides", "unknown", "diseases"]
state_dropdown = get_state_dropdown()
state_names = get_state_names()

app = dash.Dash(__name__, external_stylesheets = external_stylesheets_)
app.title = "Honey Report"
app.layout = html.Div(children=[
    html.Div([
        html.H1(children='Honey Report'),

        html.Div([
        	html.P('EXAMPLE 1 good bladbla afblasfblasfb blasfblasflb basflasfblaf basflbasfbl aAPPLES yadadssd asdnasd infasf asfapf a aspfaspfa p asfp aspf aspfap asfpasf p '),
        	html.P('Paragraph 2')], 
        className='six columns', 
        style={'margin-top':"10%",
        		'margin-left': '10%',
        		'margin-right': '10%',
        		'margin-bottom': '10%'}),



        html.Div(
            children=[   


                html.Div(
                    [
                        dcc.Dropdown(
                                id = 'dropdown1',
                                options=[
                                    {'label': 'Varroa Mites', 'value': 'varroa_mites'},
                                    {'label': 'Pesticides', 'value': 'pesticides'},
                                    {'label': 'Other Pests (Tracheal Mites, Nosema, Wax Moths, etc)', 'value': 'other_pests'},
                                    {'label': 'Unknown', 'value': 'unknown'},
                                    {'label': 'Diseases', 'value': 'diseases'},
                                    {'label': 'Other Causes (Weather, Starvation, Queen Failure, etc)', 'value': 'other'}
                                ],
                                value='varroa_mites'
                        ),
                    ],
                    className='four columns',
                )
            ], 
            className="row",
            style = {
                'margin-left':'7%',
                'margin-right':'10%'
            }
        ),

        html.Div(children=[
        	html.Div(
                    [
                        daq.Slider(
                            id = 'slider1',
                      		min=1,
                      		max=16,
                            #marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(10, 41,5)},
                            marks = slider_markers,
                            value=1,
                            size = 1000,
                            handleLabel={"showCurrentValue":True, "label": "VALUE"}
                        ),
                    ],
                    className='ten columns',
                )
        ],
        className="row",
        style = {'margin-left':'10%',
                'margin-right':'10%',
                'margin-top': '5%',
                'margin-bottom': '10%'}),


        html.Div(
        	[
        		dcc.Graph(
		            id='us-map',
	        )], 
	        className = "six columns"),

        

        html.Div([
        	html.P('EXAMPLE 3 good bladbla afblasfblasfb blasfblasflb basflasfblaf basflbasfbl aAPPLES yadadssd asdnasd infasf asfapf a aspfaspfa p asfp aspf aspfap asfpasf p '),
        	html.P('Paragraph 4')], 
        className='six columns', 
        style={'margin-top':"10%",
        		'margin-left': '10%',
        		'margin-right': '10%',
        		'margin-bottom': '10%'}),





        html.Div(
            [
                dcc.Dropdown(
                        id = 'dropdown2',
                        options=state_dropdown,
                        value='California'
                ),
            ],
            className='two columns',
            style = {'margin-left' : '10%',
            		 'margin-right': '10%'}),

        html.Div(
        	[
	        	dcc.Graph(
	        		id='state-line-plot'
	        )], 
	        className = "six columns",
	        style = {'margin-top':'3%',
	        		 'margin-left' : '10%',
	        		 'margin-right': '10%',
	        		 'margin-bottom': '10%'}),

    ], 
    className = "ten columns",
    style={'margin-top': '10%'}),
])



@app.callback(
    dash.dependencies.Output('us-map', 'figure'),
    [dash.dependencies.Input('dropdown1', 'value'), dash.dependencies.Input('slider1', 'value')])
def update_map(dropdown_, slider_):
	for i in stressors:
		if i in dropdown_:
		    title_ = "Top "+ str(slider_) + " Honey"
		    fig = generate_map_object(colony_data, slider_markers[slider_], dropdown_)
		    figure = fig
	
	return figure


@app.callback(
    dash.dependencies.Output('state-line-plot', 'figure'),
    [dash.dependencies.Input('dropdown2', 'value')])
def update_line_plot(dropdown_):
	for i in state_names:
		if i in dropdown_:
		    fig = generate_line_plot(colony_data, stressors, dropdown_)
		    figure = fig
	
	return figure


if __name__ == '__main__':
    app.run_server(debug=True)