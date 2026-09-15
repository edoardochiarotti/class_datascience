
import pandas as pd
import numpy as np

###################################
##### GENERATE EMISSIONS DATA #####
###################################

np.random.seed(42)  # for reproducibility
years = list(range(2017, 2025))

# Starting and ending values for each country
trends = {
    "France": (330, 280),
    "Switzerland": (50, 35),
    "Germany": (780, 650)
}

emissions_dict = {}

for country, (start, end) in trends.items():
    # Create a linear decreasing trend
    base = np.linspace(start, end, len(years))
    # Add small random noise
    noise = np.random.normal(0, 5, len(years))
    emissions = np.round(base + noise).astype(int)
    
    # Store results in dictionary
    emissions_dict[country] = emissions.tolist()

print("Generated emissions data:")
print(emissions_dict)

###############################
##### BUILD THE DATAFRAME #####
###############################

rows = []
for country, values in emissions_dict.items():
    for year, value in zip(years, values):
        rows.append({"Country": country, "Year": year, "CO2_Emissions[tCO2]": value})

df = pd.DataFrame(rows)

print("\nFinal DataFrame:")
print(df)

######################################
##### DO THE SAME FOR POPULATION #####
######################################

def generate_df(years, trends, variable_name, add_noise = True):
    
    np.random.seed(42)  # for reproducibility
    
    # generate values and put them in dictionary
    dict_temp = {}
    for country, (start, end) in trends.items():
        
        # Create a linear trend
        base = np.linspace(start, end, len(years))
        
        # Add small random noise
        if add_noise == True:
            noise = np.random.normal(0, 5, len(years))
            values = np.round(base + noise, 2)
        else:
            values = np.round(base, 2)
        
        # Store results in dictionary
        dict_temp[country] = values.tolist()
        
    # make the df
    rows = []
    for country, values in dict_temp.items():
        for year, value in zip(years, values):
            rows.append({"Country": country, "Year": year, variable_name: value})
    df = pd.DataFrame(rows)
    
    # return
    return df


years = list(range(2017, 2025))

# remake emissions
trends_emission = {"France": (330, 280), "Switzerland": (50, 35), "Germany": (780, 650)}
df_emissions = generate_df(years = years, trends = trends_emission, variable_name = "CO2_emissions[MtCO2]")

# make poulation
trends_population = {"France": (67.0, 68.0), "Switzerland": (8.4, 8.9), "Germany": (82.8, 83.5)}
df_population = generate_df(years = years, trends = trends_population, variable_name = "population[milpeople]", add_noise = False)

################################
##### MERGE TWO DATAFRAMES #####
################################

# merge two dfs together
df = pd.merge(df_emissions, df_population, "left", ["Country","Year"])

############################################
##### CREATE VARIABLES / DO OPERATIONS #####
############################################

# add emissions per capita
df["CO2_emissions_per_capita[tCO2/person]"] = (df["CO2_emissions[MtCO2]"] * 1e6) / (df["population[milpeople]"] * 1e6)

# subset
df_sub = df.loc[df["Country"] == "France",:]
df_sub = df.loc[(df["Country"] == "France") & (df["Year"].isin([2017,2018])),:]
df_sub = df.loc[df["Country"] == "France","population[milpeople]"]

###############################
##### WIDE VS LONG FORMAT #####
###############################

# melt
df_melted = pd.melt(df, id_vars = ["Country","Year"])

# pivot
df_back = df_melted.pivot(index=["Country","Year"], columns='variable', values='value').reset_index()

###################
##### GROUPBY #####
###################

# make ts
df_agg = df_melted.groupby(["Year","variable"], as_index=False)['value'].agg("sum")

# sort
df_agg.sort_values(["variable","Year"], inplace=True)

# pivot back in case
df_agg_pivoted = df_agg.pivot(index=["Year"], columns='variable', values='value').reset_index()

################
##### SAVE #####
################

df.to_csv("data_generated/data_intro_co2.csv", index=False)
