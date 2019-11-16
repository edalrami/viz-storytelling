import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import re
from os import listdir
from os.path import isfile, join
import plotly.graph_objects as go


us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

def get_state_dropdown():
    dict_list= []
    for i in us_state_abbrev.keys():
        dict_list.append({'label': i, 'value': i})
    return dict_list


def get_state_names():
    return list(us_state_abbrev.keys())

def remove_chars(input_):
    '''
    removes unwanted characters from a line read from a file
    input parameters:
        input_: A list containing a line read from a file
    output:
        output_list: A list containing the line with unwanted characters removed
    '''
    output_ = input_.strip('\n').split(',')
    output_list = [re.sub(r'^"|"$', '', i) for i in output_]
    return output_list

def clean_colony_data(file_):
    '''
    Reads in the USDA honey colony data files and outputs 2 cleaned dataframes
    One pertaining to the colony count data per state, and the second dataframe containing
    the colony diseases per state.
    
    input parameters: 
        file_: string containing file path 
        
    returns:
        colony_df: Dataframe containing data of colony counts per state
        disease_df: Dataframe containing the colony disease counts per state
    '''
    #Remove unwanted characters in file lines
    f = [remove_chars(i) for i in open(file_)]
    
    #looking at the excel table we know that colony data has 10 columns
    #disease data has nine columns, and that these rowtypes are classified
    #as data rows with character 'd'. Thus we subset these specific
    #data rows by their lengths.
    
    colony_data = [i for i in f if len(i) == 10 for j in i if j == 'd']
    disease_data = [i for i in f if len(i) == 9 for j in i if j == 'd']
    
    #The data for each quarter starts with Alabama and ends with the United States total
    #By getting these indexes, we can separate all quarters in the file
    colony_start_indexes = [colony_data.index(colony_data[i]) for i in range(len(colony_data)) for j in colony_data[i] if j == 'Alabama']
    disease_start_indexes = [disease_data.index(disease_data[i]) for i in range(len(disease_data)) for j in disease_data[i] if j == 'Alabama']
    
    colony_end_indexes = [colony_data.index(colony_data[i]) for i in range(len(colony_data)) for j in colony_data[i] if j == 'Wyoming']
    disease_end_indexes = [disease_data.index(disease_data[i]) for i in range(len(disease_data)) for j in disease_data[i] if j == 'Wyoming']
    
    #subset the data by with the index values collected
    colony_subsets = [colony_data[colony_start_indexes[i]: colony_end_indexes[i]] for i in range(len(colony_start_indexes))]    
    quarters = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8']
    
    #append the quarter labels
    for i in range(len(colony_subsets)):
        for j in colony_subsets[i]:
            j.append(quarters[i])
    
    cleaned_colony_data = [j for i in colony_subsets for j in i]
    
    #Subset the disease data and append the quarter labels
    disease_subsets = [disease_data[disease_start_indexes[i]: disease_end_indexes[i]] for i in range(len(disease_start_indexes))]    
    for i in range(len(disease_subsets)):
        for j in disease_subsets[i]:
            j.append(quarters[i])
    
    cleaned_disease_data = [j for i in disease_subsets for j in i]
    
    #Convert the cleaned data into dataframes
    colony_df = pd.DataFrame(cleaned_colony_data)
    colony_df.columns = ["table_no", "row_type", "state", "initial_count", "max", "lost", "lost_perc", "added", "renovated", "renovated_perc", "quarter"]
    
    disease_df = pd.DataFrame(cleaned_disease_data)
    disease_df.columns = ["table_no", "row_type", "state", "varroa_mites", "other_pests", "diseases", "pesticides", "other", "unknown", "quarter"]
    
    #drop unwanted columns and replace non numeric chars
    colony_df.drop(columns=['table_no', 'row_type'], inplace = True)
    disease_df.drop(columns=['table_no', 'row_type'], inplace = True)

    colony_df.replace(['(X)', '-'], "", inplace = True)
    colony_df.replace(['(Z)'], "0", inplace = True)

    disease_df.replace(['(X)', '-'], '', inplace = True)
    disease_df.replace(['(Z)'], '0', inplace = True)

    #Set column data types
    categoricals = ['state', 'quarter']
    for (columnName, columnData) in colony_df.iteritems():
        if(columnName not in categoricals):
            colony_df[columnName] = pd.to_numeric(colony_df[columnName], errors = 'coerce', downcast = 'float')
        else:
            colony_df[columnName] = colony_df[columnName].astype(str)


    for (columnName, columnData) in disease_df.iteritems():
        if(columnName not in categoricals):
            disease_df[columnName] = pd.to_numeric(disease_df[columnName], errors = 'coerce', downcast = 'float')
        else:
            disease_df[columnName] = disease_df[columnName].astype(str)
    
    colony_df = colony_df[colony_df.state != ""]
    disease_df = disease_df[disease_df.state != ""]
    
    colony_df.state = [abbrev_us_state[i] if i in list(abbrev_us_state.keys()) else i for i in colony_df.state]
    colony_df['state_code'] = [us_state_abbrev[i] if i in list(us_state_abbrev.keys()) else i for i in colony_df.state]
    
    disease_df.state = [abbrev_us_state[i] if i in list(abbrev_us_state.keys()) else i for i in disease_df.state]
    disease_df['state_code'] = [us_state_abbrev[i] if i in list(us_state_abbrev.keys()) else i for i in disease_df.state]
    
    return (colony_df, disease_df)  






def clean_production_data(file_):
    '''
    Reads in the USDA honey colony data files and outputs 2 cleaned dataframes
    One pertaining to the colony count data per state, and the second dataframe containing
    the colony diseases per state.
    
    input parameters: 
        file_: string containing file path 
        
    returns:
        colony_df: Dataframe containing data of colony counts per state
        disease_df: Dataframe containing the colony disease counts per state
    '''
    #Remove unwanted characters in file lines
    f = [remove_chars(i) for i in open(file_)]
    
    #looking at the excel table we know that colony data has 10 columns
    #disease data has nine columns, and that these rowtypes are classified
    #as data rows with character 'd'. Thus we subset these specific
    #data rows by their lengths.
    
    prod_data = [i for i in f if len(i) == 9 for j in i if j == 'd']
    
    #The data for each quarter starts with Alabama and ends with the United States total
    #By getting these indexes, we can separate all quarters in the file
    prod_start_indexes = [prod_data.index(prod_data[i]) for i in range(len(prod_data)) for j in prod_data[i] if j == 'Alabama' or j == 'AL'] 
    prod_end_indexes = [prod_data.index(prod_data[i]) for i in range(len(prod_data)) for j in prod_data[i] if j == 'Wyoming' or j == 'WY']
   
    #subset the data by with the index values collected
    prod_subsets = [prod_data[prod_start_indexes[i]: prod_end_indexes[i]] for i in range(len(prod_start_indexes))]    
    quarters = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8']
    
    #append the quarter labels
    for i in range(len(prod_subsets)):
        for j in prod_subsets[i]:
            j.append(quarters[i])
    
    cleaned_prod_data = [j for i in prod_subsets for j in i]
    
    
    #Convert the cleaned data into dataframes
    prod_df = pd.DataFrame(cleaned_prod_data)
    prod_df.columns = ["table_no", "row_type", "state", "honey_colonies", "yield_per_col", "production", 'stocks', 'avg_price_per_lb', 'prod_value', 'quarter']
    
    #drop unwanted columns and replace non numeric chars
    prod_df.drop(columns=['table_no', 'row_type'], inplace = True)

    prod_df.replace(['(X)', '-'], "", inplace = True)
    prod_df.replace(['(Z)'], "0", inplace = True)

    #Set column data types
    categoricals = ['state', 'quarter']
    for (columnName, columnData) in prod_df.iteritems():
        if(columnName not in categoricals):
            prod_df[columnName] = pd.to_numeric(prod_df[columnName], errors = 'coerce', downcast = 'float')
        else:
            prod_df[columnName] = prod_df[columnName].astype(str)
            
    prod_df = prod_df[prod_df.state != ""]
    
    prod_df.state = [abbrev_us_state[i] if i in list(abbrev_us_state.keys()) else i for i in prod_df.state]
    
    prod_df['state_code'] = [us_state_abbrev[i] if i in list(us_state_abbrev.keys()) else i for i in prod_df.state]
    
    return prod_df  

def get_data():
    
    #Data paths
    colony_path = '.\\colony_data'
    production_path = '.\\production_data'
    colony_files = [f for f in listdir(colony_path) if isfile(join(colony_path, f))]
    production_files = [f for f in listdir(production_path) if isfile(join(production_path, f))]
    
    colony_files = [colony_path + '\\' + i for i in colony_files]
    production_files = [production_path + '\\' + i for i in production_files]
    
    #---------------Production Data-----------------------
    all_prod_data = [clean_production_data(i) for i in production_files]
    #Get 2018 data from last index Q2
    prod_2018 = all_prod_data[17]
    prod_2018 = prod_2018[prod_2018.quarter == 'Q2'].copy()
    prod_2018['year'] = 2018

    #Get 2000-2017 year data from Q1
    all_prod_data = [i[i.quarter == 'Q1'].copy() for i in all_prod_data]
    years = list(range(2000, 2018))

    for i in range(len(years)):
        all_prod_data[i].loc[:,'year'] = years[i]

    all_prod_data.append(prod_2018)
    honey_prod = pd.concat(all_prod_data)
    honey_prod.drop(columns=['quarter'], inplace = True)
    
    
    #----------------Colony Data--------------------------
    
    #clean all separated data
    all_col_data = [clean_colony_data(i) for i in colony_files]
    all_disease_data = [i[1] for i in all_col_data]
    all_col_data = [i[0] for i in all_col_data]
    
    #remove overlapped data
    all_disease_data = [i[i.quarter != 'Q5'] for i in all_disease_data]
    all_disease_data = [i[i.quarter != 'Q6'] for i in all_disease_data]
    
    all_col_data = [i[i.quarter != 'Q5'] for i in all_col_data]
    all_col_data = [i[i.quarter != 'Q6'] for i in all_col_data]
    
    #Include year data
    col_years = list(range(2015,2019))
    for i in range(len(all_disease_data)):
        all_disease_data[i].loc[:,'year'] = col_years[i] 
        all_col_data[i].loc[:,'year'] = col_years[i]
    
    #Combine dataframe lists 
    diseases_df = pd.concat(all_disease_data, ignore_index = True)
    col_df = pd.concat(all_col_data, ignore_index = True)
    
    colony_data = pd.concat([diseases_df, col_df], axis = 1)
    
    colony_data = colony_data.loc[:,~colony_data.columns.duplicated()]
    colony_data['period'] = colony_data["year"].map(str) + colony_data["quarter"]
    
    return (honey_prod, colony_data)

def generate_map_object(input_, period_, category_):
    '''
    Returns a plotly chloropleth graph object

    input: 
        input_: A dataframe of honey_data containing
        relevant production data
        
        period_: A string value containing the year and quarter of 
                 the data to be displayed. Ex: '2015Q1'
        
        category_: The variable to be used for density on the map.
                   Can be any of the following: 
                   - varroa_mites 
                   - diseases 
                   - other 
                   - unknown 
                   - pesticides
                   - other_pests

    returns:
        fig: A chloropleth graph object

    ''' 
    
    df = input_[input_['period'] == period_]
    
    
    
    fig = go.Figure(data=go.Choropleth(
       
        locations=df.state_code,
        z=df[category_],
        zmin = 0,
        zmax = 70,
        locationmode='USA-states',
        colorscale='Reds',
        autocolorscale=False,
        #text=test_df['text'], # hover text
        marker_line_color='white', # line markers between states
        colorbar_title="population %",
        #coloraxis = dict(cmin = 0, cmax = 100),
     
    ))

    fig.update_layout(
        #color_axis=dict(color_axis = dict(colorbar=dict(len=)))
        height=700,
        width=1100,
        title_text=str(period_) + ' '+ category_ + ' Stressor<br>(Hover for breakdown)',
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True, # lakes
            lakecolor='rgb(255, 255, 255)'),
    )
    
    return fig


def generate_line_plot(input_, col_names, state_):
    '''
    Returns a multiline graph object of stressors for a specfic US state.
    
    input parameters:
        input_: DataFrame containing data
        col_names: Names of lines to be traced
        state_: Name of US State the
    
    output
    '''
    fig = go.Figure()
    annotations = []
    colors = ['crimson', 'LightSkyBlue', "MediumPurple", "green", "orange", "yellowgreen"]
    color_ix = 0
    for i in col_names:
        
        x_=list(input_[input_.state == state_].period)
        y_=list(input_[input_.state == state_][i])

        line_size = 4
        mode_size = 12
        color_ = colors[color_ix]

        fig.add_trace(go.Scatter(x=x_, y=y_, mode='lines',
            name=i,
            line=dict(color=color_, width=line_size),
            connectgaps=True,
            showlegend=True
        ))

        # endpoints
        max_val = max(y_)
        max_ix = x_[np.argmax(np.array(y_))]
        fig.add_trace(go.Scatter(
            x=[max_ix],
            y=[max_val],
            name=i,
            mode='markers+text',
            marker=dict(color=color_, size=mode_size),
            showlegend = False,
            text = '{}%'.format(round(max_val,2)),
            textposition = 'middle right'
        ))
        
        color_ix = color_ix + 1
        
    
    fig.update_layout(
        width = 800,
        height = 800,
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                  xanchor='left', yanchor='bottom',
                                  text='Bee Colony Stressors in the State of ' + state_,
                                  font=dict(family='Arial',
                                            size=30,
                                            color='rgb(37,37,37)'),
                                  showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                  xanchor='center', yanchor='top',
                                  text='Source: United States Department of Agriculture (USDA)',
                                  font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False))
    
    tick_text = ["2015", "", "", "", "2016", "", "", "", "2017", "", "", "", "2018", "", "", ""]
    tick_vals = ["2015Q1", "2015Q2", "2015Q3", "2015Q4",
                 "2016Q1", "2016Q2", "2016Q3", "2016Q4", 
                 "2017Q1", "2017Q2", "2017Q3", "2017Q4", 
                 "2018Q1", "2018Q2", "2018Q3", "2018Q4"]
    fig.update_xaxes(ticktext=tick_text, tickvals = tick_vals, tickangle=0, tickfont=dict(family='Rockwell'))
    fig.update_layout(annotations=annotations, showlegend=True, legend_orientation='h', legend=dict(x=0, y=1.03))
    
    return fig
