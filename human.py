"""
Assignment: HW3 Human vs. AI
File: human.py
Name: Rayd Hussain

DS3500
5/23/2025
"""

import pandas as pd
import panel as pn

# Loads javascript dependencies and configures Panel (required)
pn.extension()


# LOAD DATA

df = pd.read_csv("subrecipient_data.csv")
df.columns = [c.strip() for c in df.columns]

states = ["All"] + sorted(df["Recipient/Sub-Recipient State Abbreviation"].dropna().unique())
years = ["All"] + sorted(df["Reporting Year"].dropna().astype(int).astype(str).unique())


# WIDGET DECLARATIONS

state_select = pn.widgets.Select(name="State", options=states, value=states[0])
year_select  = pn.widgets.Select(name="Year",  options=years,  value=years[0])


# CALLBACK FUNCTIONS

def filter_data(state, year):
    d = df.copy()
    if state != "All":
        d = d[d["Recipient/Sub-Recipient State Abbreviation"] == state]
    if year != "All":
        d = d[d["Reporting Year"] == int(year)]
    return d

def provider_bar(state, year):
    d = filter_data(state, year)
    counts = d["HAB Provider Type Description"].value_counts()
    ax = counts.plot(
        kind="bar",
        xlabel="Provider Type",
        ylabel="Count",
        title="Providers by Type"
    )
    return pn.pane.Matplotlib(ax.get_figure(), tight=True)

def data_table(state, year):
    return pn.pane.DataFrame(filter_data(state, year), height=300)


# CALLBACK BINDINGS (Connecting widgets to callback functions)

plot_panel = pn.bind(provider_bar, state_select.param.value, year_select.param.value)
table_panel = pn.bind(data_table, state_select.param.value, year_select.param.value)


# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 320

search_card = pn.Card(
    pn.Column(
        state_select,
        year_select
    ),
    title="Search", width=card_width, collapsed=False
)

plot_card = pn.Card(
    pn.Column(
        # you could add more plot options here
    ),
    title="Plot", width=card_width, collapsed=True
)


# LAYOUT

layout = pn.template.FastListTemplate(
    title="Subrecipient Dashboard",
    sidebar=[
        search_card,
        plot_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Providers by Type", plot_panel),
            ("Data Table", table_panel),
            active=0
        )
    ],
    header_background='#a93226'
).servable()

layout.show()
