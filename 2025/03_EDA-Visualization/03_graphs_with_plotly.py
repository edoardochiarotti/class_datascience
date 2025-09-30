
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
pio.renderers.default='browser'
import statsmodels

#####################
##### LOAD DATA #####
#####################

df = pd.read_csv("../02_Data-Cleaning/data_generated/data_intro_co2.csv")

#####################################################
##### MAKE TIME SERIES OF AVERAGE CO2 EMISSIONS #####
#####################################################

# prepare dataframe
df_graph = pd.melt(df, id_vars = ["Country","Year"])
df_graph = df_graph.loc[df_graph["variable"] == 'CO2_emissions[MtCO2]',:]
df_graph = df_graph.groupby(["Year","variable"], as_index=False)['value'].agg("mean")

# make graph
fig = px.line(df_graph,x="Year", y="value", color="variable", 
              labels={"Year": "Year",
                      "value": "CO2 emissions (MtCO2)",
                      "variable": ""
                      },
              title="Average CO2 emissions across countries"
              )
fig.show()


########################################################
##### MAKE TIME SERIES OF CO2 EMISSIONS BY COUNTRY #####
########################################################

# prepare dataframe
df_graph = pd.melt(df, id_vars = ["Country","Year"])
df_graph = df_graph.loc[df_graph["variable"] == 'CO2_emissions[MtCO2]',:]

# make graph
fig = px.line(df_graph,x="Year", y="value", color="Country", 
              labels={"Year": "Year",
                      "value": "CO2 emissions (MtCO2)",
                      "variable": ""
                      },
              title="CO2 emissions by country"
              )
fig.show()

########################################################
##### MAKE A FUNCTION TO DO THIS FOR EACH VARIABLE #####
########################################################

def plot_variable(df, variable):
    
    # prepare dataframe
    df_graph = pd.melt(df, id_vars = ["Country","Year"])
    df_graph = df_graph.loc[df_graph["variable"] == variable,:]

    # make graph
    fig = px.line(df_graph,x="Year", y="value", color="Country", 
                  labels={"Year": "Year",
                          "value": "CO2 emissions (MtCO2)",
                          "variable": ""
                          },
                  title= f"{variable} by country"
                  )
    fig.show()
    
plot_variable(df, "CO2_emissions[MtCO2]")
plot_variable(df, 'population[milpeople]')
plot_variable(df, 'CO2_emissions_per_capita[tCO2/person]')


########################################################################
##### MAKE TIME SERIES OF CO2 EMISSIONS AND POPULATION WITH FACETS #####
########################################################################

# prepare dataframe
df_graph = pd.melt(df, id_vars = ["Country","Year"])
df_graph = df_graph.groupby(["Year","variable"], as_index=False)['value'].agg("mean")

# make graph
fig = px.line(df_graph,x="Year", y="value", color="variable", 
              facet_col="variable", # put variables in different panels (facets)
              facet_col_wrap=2, # say that you want 2 columns (so if you have 3 graphs it will be also 2 rows)
              labels={"Year": "Year",
                      "value": "",
                      "variable": "Variable"
                      },
              title="Average variables across countries"
              )
fig.update_yaxes(matches=None, showticklabels=True) # let y axis scale automatically
fig.show()

####################################################
##### MAKE SCATTER OF EMISSIONS AND POPULATION #####
####################################################

# normal scatter
df_graph = df.copy()
fig = px.scatter(df_graph, x="population[milpeople]", y="CO2_emissions[MtCO2]",
                 color="Country",           # optional: see each country separately
                 trendline="ols",           # adds regression line
                 trendline_scope="overall", # regression over all points (default)
                 labels={
                     "population[milpeople]": "Population (million people)",
                     "CO2_emissions[MtCO2]": "CO2 emissions (MtCO2)"
                 },
                 title="CO2 emissions vs. population"
)
fig.show()

# scatter on mean values across years

# prepare dataframe
df_graph = pd.melt(df, id_vars = ["Country","Year"])
df_graph = df_graph.groupby(["Country","variable"], as_index=False)['value'].agg("mean")
df_graph = df_graph.pivot(index="Country", columns="variable", values="value").reset_index()

# make scatter
fig = px.scatter(df_graph, x="population[milpeople]", y="CO2_emissions[MtCO2]",
                 color="Country",           # optional: see each country separately
                 trendline="ols",           # adds regression line
                 trendline_scope="overall", # regression over all points (default)
                 labels={
                     "population[milpeople]": "Population (million people)",
                     "CO2_emissions[MtCO2]": "CO2 emissions (MtCO2)"
                 },
                 title="CO2 emissions vs. population"
)
fig.show()

# alternate way (avoid melting and pivot)
df_graph = df.groupby("Country", as_index=False).mean()
df_graph.drop(columns=["Year"],inplace=True)
fig = px.scatter(df_graph, x="population[milpeople]", y="CO2_emissions[MtCO2]",
                 color="Country",           # optional: see each country separately
                 trendline="ols",           # adds regression line
                 trendline_scope="overall", # regression over all points (default)
                 labels={
                     "population[milpeople]": "Population (million people)",
                     "CO2_emissions[MtCO2]": "CO2 emissions (MtCO2)"
                 },
                 title="CO2 emissions vs. population"
)
fig.show()

#####################################
##### MAKE BOXPLOT OF VARIABLES #####
#####################################

# all data
fig = px.box(df, y="CO2_emissions_per_capita[tCO2/person]",
             labels={
                 "O2_emissions_per_capita[tCO2/person]": "CO2 emissions per capita (tCO2 per person)"
                 },
             title="Distribution of CO2 emissions per capita"
             )
fig.show()

# by country
fig = px.box(df, x="Country", y="CO2_emissions_per_capita[tCO2/person]", color = "Country",
             labels={
                 "O2_emissions_per_capita[tCO2/person]": "CO2 emissions per capita (tCO2 per person)"
                 },
             title="Distribution of CO2 emissions per capita per country"
             )
fig.show()


