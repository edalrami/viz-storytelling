import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_daq as daq

from clean_honey_data import *
import pandas as pd

external_stylesheets_ = ['https://codepen.io/amyoshino/pen/jzXypZ.css']


all_data = get_data()
honey_data = all_data[0]
colony_data = all_data[1]
period_vals = list(colony_data.period.unique())
slider_markers = {i+1: period_vals[i] for i in range(len(period_vals))}
stressors = ["varroa_mites", "other_pests", "other", "pesticides", "unknown", "diseases", "lost_perc"]
state_dropdown = get_state_dropdown()
state_names = get_state_names()

app = dash.Dash(__name__, external_stylesheets = external_stylesheets_)
app.title = "Honey Report"
app.layout = html.Div(children=[
    html.Div([
        html.H1(children='The Story of US Honey and Bee Colonies'),

        #paragraph
        html.Div([
        	html.P('EXAMPLE 1 good bladbla afblasfblasfb blasfblasflb basflasfblaf basflbasfbl aAPPLES yadadssd asdnasd infasf asfapf a aspfaspfa p asfp aspf aspfap asfpasf p '),
        	html.P('Paragraph 2')], 
        className='six columns', 
        style={'margin-top':"10%",
        		'margin-bottom': '10%'}),

        html.Div([], className = "six columns"),
        
        #Dropdown
        html.Div(
            children=[
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
            className='two columns',
            style={'margin-right': '10%',
            	   'display':'inline-block'}
        ),

        html.Div([], className = 'ten columns'),
       
        #map
        html.Div(
        	[
        		dcc.Graph(
		            id='us-map',
	        )], 
	        className = "six columns",
	        style = {'margin-top': '1%'}),

        html.Div([], className = "six columns"),

        #slider
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
                className='nine columns',
                style={'margin-top': '3%',
                		'margin-bottom:':'3%'}),

        html.Div([], className = "three columns"),
        
        #paragraph
        html.Div([
        	html.P('EXAMPLE 3 good bladbla afblasfblasfb blasfblasflb basflasfblaf basflbasfbl aAPPLES yadadssd asdnasd infasf asfapf a aspfaspfa p asfp aspf aspfap asfpasf p '),
        	html.P('Paragraph 4')], 
        className='six columns', 
        style={'margin-top':"10%",
        		#'margin-left': '10%',
        		#'margin-right': '10%',
        		}),




        html.Div([], className='six columns'),

        
        #Dropdown 2
        html.Div(
            [
                dcc.Dropdown(
                        id = 'dropdown2',
                        options=state_dropdown,
                        value='California'
                ),
            ],
            className='two columns',
            #style = {'margin-left' : '10%',
            		 #'margin-right': '10%'}
            		 ),

        html.Div([], className = "ten columns"),

        #Line plot
        html.Div(
        	[
	        	dcc.Graph(
	        		id='state-line-plot'
	        )], 
	        className = "three columns",
	        style = {'margin-right':'80%'}),
	        		 #'margin-left' : '12%',
	        		 #'margin-right': '10%',
	        #		 'margin-bottom': '10%'}),

        html.Div([], className = "nine columns"),



        
        #paragraph
        html.Div([
        	html.P('EXAMPLE 5 good bladbla afblasfblasfb blasfblasflb basflasfblaf basflbasfbl aAPPLES yadadssd asdnasd infasf asfapf a aspfaspfa p asfp aspf aspfap asfpasf p '),
        	html.P('Paragraph 4')], 
        className='six columns', 
        style={'margin-top':"10%",
        		#'margin-left': '10%',
        		#'margin-right': '10%',
        		}),




        html.Div([], className='six columns'),

      	#slider
    	html.Div(
                [
                    daq.Slider(
                        id = 'slider2',
                  		min=2000,
                  		max=2018,
                        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(2000, 2019)},
                        #marks = slider_markers,
                        value=2000,
                        size = 800,
                        handleLabel={"showCurrentValue":True, "label": "VALUE"}
                    ),
                ],
                className='six columns',
                style = {'margin-top' : '5%', 'margin-left': '5%'}),
            		 	 
    	html.Div([], className="six columns"),

    	
    	#bubbble
    	html.Div(
        	[
	        	dcc.Graph(
	        		id='bubble-plot'
	        )], 
	        className = "six columns",
	        style = {'margin-top':'1%',
	        		 #'margin-left' : '10%',
	        		 #'margin-right': '10%',
	        		 'margin-bottom': '10%'}),


    ], 
    className = "twelve columns",
    style={'margin-top': '10%', 'margin-left':'10%'}),
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



stressors2 = ["varroa_mites", "other_pests", "pesticides", "diseases", "lost_perc"]

@app.callback(
    dash.dependencies.Output('state-line-plot', 'figure'),
    [dash.dependencies.Input('dropdown2', 'value')])
def update_line_plot(dropdown_):
	for i in state_names:
		if i in dropdown_:
		    fig = generate_line_plot(colony_data, stressors2, dropdown_)
		    figure = fig
	
	return figure

@app.callback(
    dash.dependencies.Output('bubble-plot', 'figure'),
    [dash.dependencies.Input('slider2', 'value')])
def update_bubble_plot(slider_):
	figure = generate_bubble_chart(honey_data, slider_, 15)
	return figure


if __name__ == '__main__':
    app.run_server(debug=True)