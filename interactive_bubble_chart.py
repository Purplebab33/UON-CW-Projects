import pandas as pd
import os
import numpy as np
import plotly.express as px

# Setting the current working path
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("current working path:", os.getcwd())

# Read files
df = pd.read_csv('./Data_Output/Results_with_outliers_flag.csv')

# Generate new indicators and fields
df['diet_sex_group'] = df['diet_group'] + '_' + df['sex']
df['stability_score'] = np.sqrt(df['sd_watuse']**2 + df['sd_watscar']**2)

# Generate new color_group
def assign_color_group(row):
    if row['outliers'] == 1:
        return 'vegan_female_outlier'
    elif row['outliers'] == 2:
        return 'vegan_male_outlier'
    elif row['outliers'] == 3:
        return 'veggie_female_outlier'
    elif row['outliers'] == 4:
        return 'veggie_male_outlier'
    else:
        return row['diet_sex_group']

df['color_group'] = df.apply(assign_color_group, axis=1)

# Define the color mapping
color_map = {
    'vegan_female': '#AEC6CF', 
    'vegan_male': '#D1C4E9', 
    'veggie_female': '#A8E6CF', 
    'veggie_male': '#FFD3B6', 
    'vegan_female_outlier': 'red', 
    'vegan_male_outlier': 'red',
    'veggie_female_outlier': 'red',
    'veggie_male_outlier': 'red'
}

# Customize the order of color_group
order = [
    'vegan_female',
    'vegan_male',
    'veggie_female',
    'veggie_male',
    'vegan_female_outlier',
    'vegan_male_outlier',
    'veggie_female_outlier',
    'veggie_male_outlier'
]

# Set color_group to be an ordered categorical variable.
df['color_group'] = pd.Categorical(df['color_group'], categories=order, ordered=True)

# Drawing Interactive Bubble Charts
fig = px.scatter(
    df,
    x='mean_watuse',       
    y='mean_watscar',       
    color='color_group',
    color_discrete_map=color_map,
    size='stability_score',
    animation_frame='age_group',
    size_max=60,
    hover_name='grouping',
    hover_data={
        'mean_watuse': ':.2f',
        'mean_watscar': ':.2f',
        'outliers': True
    },
    category_orders={'color_group': order} 
)

# Customized bubble styles (transparency + white border)
fig.update_traces(
    marker=dict(
        opacity=0.7,
        line=dict(color='white', width=1)
    )
)

# Fine-tune the overall layout
fig.update_layout(
    title={
        'text': (
            "Interactive Bubble Chart: Water Use vs Water Scarcity by Diet Group and Age<br>"
            "<span style='font-size:16px; color:gray;'>Analyzing Water Use Outliers and Scarcity Risks Among Vegan and Vegetarian Dietary Groups</span>"
        ),
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },

    title_font=dict(
        size=28,
        family='Arial',
        color='black'
    ),

    sliders=[{
        'active': 0,
        'currentvalue': {
            'prefix': 'Age Group: ',
            'font': {'size': 14, 'color': 'grey'}, 
            'offset': 10  
        },
        'pad': {'t': 10},  
        'len': 0.8,        
        'x': 0.1,         
        'y': -0.15,        
        'font': {'size': 14},
        'steps': [], 
    }],

    transition={'duration': 300}, 
    sliderdefaults=dict(
        bgcolor='lightgrey',  
        activebgcolor='deepskyblue', 
        bordercolor='lightgrey',
        borderwidth=1
    ),

    legend_title_text='Diet + Sex Group',
    legend=dict(
        title_font=dict(size=20, family='Arial'),
        font=dict(size=16, family='Arial'),
        bgcolor='rgba(255,255,255,0.6)',  
        bordercolor='lightgrey',
        borderwidth=1,
        orientation='v',
        yanchor='top',
        y=0.8,
        xanchor='left',
        x=1.02  
    ),

    xaxis_title='Mean Water Use (liters/day)',
    xaxis=dict(
        range=[df['mean_watuse'].min()*0.8, df['mean_watuse'].max()*1.2],
        showline=True,
        linecolor='black',
        linewidth=2
    ),

    yaxis_title='Mean Water Scarcity (index)',
    yaxis=dict(
        range=[df['mean_watscar'].min()*0.8, df['mean_watscar'].max()*1.2],
        showline=True,
        linecolor='black',
        linewidth=2
    ),

    plot_bgcolor='white',
    autosize=True,
    margin=dict(l=50, r=50, t=100, b=50) 
)

# Export as an HTML file
# File stored in Data_Output
fig.write_html('./Data_Output/interactive_bubble_chart_final.html', full_html=True, include_plotlyjs='cdn', config={'responsive': True})


