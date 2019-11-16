import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_daq as daq

from clean_honey_data import *
import pandas as pd

external_stylesheets_ = ['https://codepen.io/amyoshino/pen/jzXypZ.css']



honey_data = pd.read_csv('all_honey_data.csv')
colony_data = pd.read_csv('all_colony_data.csv')
period_vals = list(colony_data.period.unique())
slider_markers = {i+1: period_vals[i] for i in range(len(period_vals))}
stressors = ["varroa_mites", "other_pests", "other", "pesticides", "unknown", "diseases", "lost_perc"]
state_dropdown = get_state_dropdown()
state_names = get_state_names()

app = dash.Dash(__name__, external_stylesheets = external_stylesheets_)
server = app.server 
app.title = "Honey Report"
app.layout = html.Div(children=[
    html.Div([
        html.H1(children=['The Story of US Honey and Bee Colonies']),
        html.H2(children = '  yet to be finished by Edwin Ramirez'),

        #paragraph
        html.Div([
        	html.P('In 2006 the US Environmental Protection Agency (EPA)' + \
        		' reported the high emergence of colony collapse disorder (CCD)' + \
        		' among bee populations throughout the United States. The large' + \
        		' number of colonies dying had no single direct cause linked at the' + \
        		' time even after several studies attempted to link possible' +\
        		' colony stressors to the epidemic, such as pesticides, diseases,'+ \
        		' parasites, weather, etc. With such a vital' + \
        		' role in the ecosystem as pollinators and as producers of honey,' + \
        		' the significance of bee preservation is not something to be ingored' + \
        		' as factors, such as climate change and increasing pesticide usage' + \
        		' continue to harm the populations. Over ten years after the CCD epidemic began' + \
        		' researchers discovered that neonicotinoid pesticides were killing off colony' + \
        		' populations, and the EPA responded by banning all use of harmful pesticides' + \
        		' to honey bee populations.'),
        	

        	html.P('The United States Department of Agriculture (USDA) has been recording' +\
        		' data on honey production per state since the 1970s, and recently began' + \
        		' collecting data on colony populations and potential colony stressors starting in 2015.' + \
        		' The objective of this report is to understand how colony stressors recorded from 2015 to 2018' + \
        		' may have affected the populations per state, and to also analyze the potential' + \
        		' stressors that affect each state more than others. Additionally, this report' + \
        		' will also analyze the honey industry in the United States prior to the outbreak and after' + \
        		' (2000-2018). With the utilization of the USDA data that is recorded annually, a series of dynamic' + \
        		' visualizations will be used to study where in the United States certain stressors have' + \
        		' affected each region more than others. Additionally, these visualizations will also' + \
        		' explore which states throughout the US have been flagged with USDA violations for specific' + \
        		' pesticide usage using pesticide data specifically focused on honey from 2000-2017.')], 
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