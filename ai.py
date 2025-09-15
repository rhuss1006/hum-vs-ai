"""
Human vs. AI
ai.py - ai-generated dashboard
Name: Rayd Hussain

5/23/2025
"""

import panel as pn
import pandas as pd
import numpy as np
import holoviews as hv
from holoviews import opts
import plotly.express as px
import plotly.graph_objects as go

# Load extensions and configure Panel
pn.extension('plotly', 'tabulator')
hv.extension('plotly')


# Load and prepare data
def load_data():
    # Read the CSV file
    df = pd.read_csv('subrecipient_data.csv')

    # Clean and prepare data
    df = df.dropna(subset=['State Name'])  # Remove rows without state info
    df = df[df[
                'State Name'] != 'Not Determined']  # Filter out undetermined locations

    # Create funding summary columns
    funding_cols = ['Received Part A Funding Indicator',
                    'Received Part B Funding Indicator',
                    'Received Part C Funding Indicator',
                    'Received Part D Funding Indicator']

    for col in funding_cols:
        df[col] = df[col].map({'Y': 1, 'N': 0}).fillna(0)

    df['Total_Funding_Parts'] = df[funding_cols].sum(axis=1)

    # Parse services into a list
    df['Services_List'] = df['RWHAP Funded Services'].str.split(';')
    df['Service_Count'] = df['Services_List'].apply(
        lambda x: len(x) if isinstance(x, list) else 0)

    return df


# Load data
data = load_data()

# WIDGET DECLARATIONS

# Search Widgets
state_select = pn.widgets.MultiChoice(
    name='Select States:',
    value=data['State Name'].unique().tolist(),
    options=data['State Name'].unique().tolist(),
    width=280
)

provider_select = pn.widgets.MultiChoice(
    name='Provider Type:',
    value=data['HAB Provider Type Description'].unique().tolist(),
    options=data['HAB Provider Type Description'].unique().tolist(),
    width=280
)

region_select = pn.widgets.MultiChoice(
    name='HHS Region:',
    value=data['HHS Region Name'].unique().tolist(),
    options=data['HHS Region Name'].unique().tolist(),
    width=280
)

# Plotting widgets
chart_type = pn.widgets.Select(
    name='Chart Type:',
    value='Bar Chart',
    options=['Bar Chart', 'Pie Chart', 'Scatter Plot', 'Geographic Map'],
    width=280
)

metric_select = pn.widgets.Select(
    name='Metric to Display:',
    value='Provider Count',
    options=['Provider Count', 'Total Funding Parts', 'Service Count'],
    width=280
)

groupby_select = pn.widgets.Select(
    name='Group By:',
    value='State Name',
    options=['State Name', 'HHS Region Name', 'HAB Provider Type Description'],
    width=280
)


# CALLBACK FUNCTIONS

def filter_data_with_params(states, providers, regions):
    """Filter data based on passed parameters"""
    filtered_df = data.copy()

    if states:
        filtered_df = filtered_df[filtered_df['State Name'].isin(states)]

    if providers:
        filtered_df = filtered_df[
            filtered_df['HAB Provider Type Description'].isin(providers)]

    if regions:
        filtered_df = filtered_df[filtered_df['HHS Region Name'].isin(regions)]

    return filtered_df


def create_summary_table(states, providers, regions):
    """Create summary statistics table"""
    filtered_df = filter_data_with_params(states, providers, regions)

    if filtered_df.empty:
        return pn.pane.HTML("<p>No data matches the current filters.</p>")

    summary_stats = pd.DataFrame({
        'Metric': [
            'Total Providers',
            'Unique States',
            'Unique Counties',
            'Avg Services per Provider',
            'Part A Recipients',
            'Part B Recipients',
            'Part C Recipients',
            'Part D Recipients'
        ],
        'Value': [
            len(filtered_df),
            filtered_df['State Name'].nunique(),
            filtered_df['Complete County Name'].nunique(),
            round(filtered_df['Service_Count'].mean(), 1),
            filtered_df['Received Part A Funding Indicator'].sum(),
            filtered_df['Received Part B Funding Indicator'].sum(),
            filtered_df['Received Part C Funding Indicator'].sum(),
            filtered_df['Received Part D Funding Indicator'].sum()
        ]
    })

    return pn.widgets.Tabulator(
        summary_stats,
        pagination='remote',
        page_size=10,
        width=600,
        height=400
    )


def create_main_plot(states, providers, regions, chart_type_val, metric_val,
                     groupby_val):
    """Create the main visualization based on widget selections"""
    filtered_df = filter_data_with_params(states, providers, regions)

    if filtered_df.empty:
        return pn.pane.HTML("<p>No data matches the current filters.</p>")

    # Prepare data based on metric selection
    if metric_val == 'Provider Count':
        plot_data = filtered_df.groupby(groupby_val).size().reset_index(
            name='Count')
        y_col = 'Count'
        title = f'Provider Count by {groupby_val}'
    elif metric_val == 'Total Funding Parts':
        plot_data = filtered_df.groupby(groupby_val)[
            'Total_Funding_Parts'].sum().reset_index()
        y_col = 'Total_Funding_Parts'
        title = f'Total Funding Parts by {groupby_val}'
    else:  # Service Count
        plot_data = filtered_df.groupby(groupby_val)[
            'Service_Count'].mean().reset_index()
        y_col = 'Service_Count'
        title = f'Average Service Count by {groupby_val}'

    x_col = groupby_val

    # Create plot based on chart type
    if chart_type_val == 'Bar Chart':
        fig = px.bar(plot_data, x=x_col, y=y_col, title=title)
        fig.update_layout(xaxis_tickangle=-45)

    elif chart_type_val == 'Pie Chart':
        fig = px.pie(plot_data, values=y_col, names=x_col, title=title)

    elif chart_type_val == 'Scatter Plot':
        # For scatter plot, use original data with coordinates
        if 'Geocoding Artifact Address Primary X Coordinate' in filtered_df.columns:
            fig = px.scatter(
                filtered_df,
                x='Geocoding Artifact Address Primary X Coordinate',
                y='Geocoding Artifact Address Primary Y Coordinate',
                color=groupby_val,
                size='Service_Count',
                hover_data=['Recipient/Sub-Recipient Name', 'State Name'],
                title='Geographic Distribution of Providers'
            )
        else:
            fig = px.scatter(plot_data, x=x_col, y=y_col, title=title)

    elif chart_type_val == 'Geographic Map':
        # Create a map visualization
        if 'Geocoding Artifact Address Primary X Coordinate' in filtered_df.columns:
            fig = px.scatter_mapbox(
                filtered_df,
                lat='Geocoding Artifact Address Primary Y Coordinate',
                lon='Geocoding Artifact Address Primary X Coordinate',
                color=groupby_val,
                size='Service_Count',
                hover_data=['Recipient/Sub-Recipient Name', 'State Name'],
                mapbox_style='open-street-map',
                title='Provider Locations Map',
                zoom=3,
                height=600
            )
        else:
            # Fallback to bar chart if no coordinates
            fig = px.bar(plot_data, x=x_col, y=y_col, title=title)

    fig.update_layout(height=500)
    return pn.pane.Plotly(fig, width=800, height=550)


def create_services_analysis(states, providers, regions):
    """Create analysis of services provided"""
    filtered_df = filter_data_with_params(states, providers, regions)

    if filtered_df.empty:
        return pn.pane.HTML("<p>No data matches the current filters.</p>")

    # Extract all services
    all_services = []
    for services_list in filtered_df['Services_List'].dropna():
        if isinstance(services_list, list):
            all_services.extend([s.strip() for s in services_list])

    # Count service frequency
    services_df = pd.DataFrame(all_services, columns=['Service'])
    service_counts = services_df['Service'].value_counts().head(
        15).reset_index()
    service_counts.columns = ['Service', 'Count']

    # Create horizontal bar chart
    fig = px.bar(
        service_counts,
        x='Count',
        y='Service',
        orientation='h',
        title='Most Common RWHAP Services',
        height=600
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})

    return pn.pane.Plotly(fig, width=800, height=650)


def create_funding_analysis(states, providers, regions):
    """Create funding pattern analysis"""
    filtered_df = filter_data_with_params(states, providers, regions)

    if filtered_df.empty:
        return pn.pane.HTML("<p>No data matches the current filters.</p>")

    # Funding patterns analysis
    funding_cols = ['Received Part A Funding Indicator',
                    'Received Part B Funding Indicator',
                    'Received Part C Funding Indicator',
                    'Received Part D Funding Indicator']

    funding_summary = filtered_df[funding_cols].sum().reset_index()
    funding_summary.columns = ['Funding_Part', 'Count']
    funding_summary['Funding_Part'] = funding_summary[
        'Funding_Part'].str.replace('Received Part ', 'Part ').str.replace(
        ' Funding Indicator', '')

    fig = px.bar(
        funding_summary,
        x='Funding_Part',
        y='Count',
        title='Distribution of RWHAP Funding Parts',
        color='Funding_Part'
    )

    return pn.pane.Plotly(fig, width=800, height=500)


# CALLBACK BINDINGS (Connecting widgets to callback functions)
summary_table = pn.bind(create_summary_table,
                        state_select.param.value,
                        provider_select.param.value,
                        region_select.param.value)

main_plot = pn.bind(create_main_plot,
                    state_select.param.value,
                    provider_select.param.value,
                    region_select.param.value,
                    chart_type.param.value,
                    metric_select.param.value,
                    groupby_select.param.value)

services_plot = pn.bind(create_services_analysis,
                        state_select.param.value,
                        provider_select.param.value,
                        region_select.param.value)

funding_plot = pn.bind(create_funding_analysis,
                       state_select.param.value,
                       provider_select.param.value,
                       region_select.param.value)

# DASHBOARD WIDGET CONTAINERS ("CARDS")
card_width = 320

search_card = pn.Card(
    pn.Column(
        state_select,
        provider_select,
        region_select
    ),
    title="🔍 Filter Data", width=card_width, collapsed=False
)

plot_card = pn.Card(
    pn.Column(
        chart_type,
        metric_select,
        groupby_select
    ),
    title="📊 Visualization Options", width=card_width, collapsed=False
)

# LAYOUT
layout = pn.template.FastListTemplate(
    title="RWHAP Funding Recipients Dashboard",
    sidebar=[
        search_card,
        plot_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("📈 Overview", pn.Column(summary_table, main_plot)),
            ("🏥 Services Analysis", services_plot),
            ("💰 Funding Analysis", funding_plot),
            active=0
        )
    ],
    header_background='#2E86AB'
).servable()

# Display the dashboard
layout.show()
