import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
from clean_honey_data import *

#Get all file names
colony_path = '.\\colony_data'
production_path = '.\\production_data'
colony_files = [f for f in listdir(colony_path) if isfile(join(colony_path, f))]
production_files = [f for f in listdir(production_path) if isfile(join(production_path, f))]

#Format file paths
colony_files = [colony_path + '\\' + i for i in colony_files]
production_files = [production_path + '\\' + i for i in production_files]

#USE CLEANING SCRIPT
all_prod_data = [clean_production_data(i) for i in production_files]
#Get 2018 data from last index Q2
prod_2018 = all_prod_data[17]
prod_2018 = prod_2018[prod_2018.quarter == 'Q2']
prod_2018['year'] = 2018

#Get all other year data from Q1
all_prod_data = [i[i.quarter == 'Q1'] for i in all_prod_data]
years = list(range(2000, 2018))

for i in range(len(years)):
    all_prod_data[i]['year'] = years[i]

all_prod_data.append(prod_2018)
honey_prod = pd.concat(all_prod_data)
honey_prod.drop(columns=['quarter'], inplace = True)


external_stylesheets_ = ['https://codepen.io/amyoshino/pen/jzXypZ.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets_)

app.title = "Honey Production In the USA"
app.layout = html.Div(children=[
    html.Div([
        

        html.Div([
            html.Div(
                [ 
                    html.Div(
                        [
                            dcc.Slider(
                                id = 'slider',
                                min=2000,
                                max=2018,
                                
                                marks={str(h) : {'label' : str(h), 'style':{'color':'black', 'font-size':'large', 'font-weight': 'bold'}} for h in range(2000,2019,1)},
                                value=2000
                            ),
                        ],
                        className='four columns', 
                        #style={
                        #    'background-color': '#FF63B2',
                        #    'font-size': 'large',

                        #}
                    )
                ], 
                className="row",
                #style = {
                #    'background-color': '#0193E8', 
                #    'margin-left': '10%'
                #}
            )
        ], className = 'row'),

        dcc.Graph(
            id='map',
        )

    ], className = "six columns"),


])

@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('slider', 'value')])
def update_map(slider_):
    if 'converted' in dropdown_:
        if 'all' in selector_:
            title_ = "Top "+ str(slider_) + " User Paths from All Patterns"
            fig = gen_sankey(all_patterns_con.head(slider_), cat_cols = list(all_patterns_con)[:-1], value_cols = 'percentage', title=title_)   

        if 'rep' in selector_:
            title_ = "Top "+ str(slider_) + " User Paths from Repeated Patterns"
            fig = gen_sankey(rep_patterns_con.head(slider_), cat_cols = list(rep_patterns_con)[:-1], value_cols = 'percentage', title=title_)

    if 'nonconverted' in dropdown_:
        if 'all' in selector_:
            title_ = "Top "+ str(slider_) + " User Paths from All Patterns"
            fig = gen_sankey(all_patterns_noncon.head(slider_), cat_cols = list(all_patterns_noncon)[:-1], value_cols = 'percentage', title=title_)   

        if 'rep' in selector_:
            title_ = "Top "+ str(slider_) + " User Paths from Repeated Patterns"
            fig = gen_sankey(rep_patterns_noncon.head(slider_), cat_cols = list(rep_patterns_noncon)[:-1], value_cols = 'percentage', title=title_)
    
    figure = fig[0]

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)