import pandas as pd

# League settings
teams = 10
budget_per_team = 200
total_budget = teams * budget_per_team
roster_positions = {'QB': 1, 'RB': 2, 'WR': 3, 'TE': 1, 'FLEX': 1}

# Load the data
file_path = r"C:\Keepers.csv"
df = pd.read_csv(file_path)

# Calculate the total keeper cost
df['Float Value'] = df['Value'].str.replace("$", "", regex=True).astype(float)
total_keeper_cost = df[df['Keeper'] == 'k']['Float Value'].sum()


# Calculate the total value of kept players
total_keeper_value = df[df['Keeper'] == 'k']['Float Value'].sum()


# Calculate the money and player value left in the pool
remaining_pool_money = total_budget - total_keeper_cost
remaining_player_value = total_budget - total_keeper_value

# Calculate inflation rate
inflation_rate = total_budget / remaining_pool_money

# Calculate the demand for each position
total_demand = {position: count * teams for position, count in roster_positions.items()}

# Calculate the supply for each position (excluding kept players)
available_players = df[df['Keeper'] != 'k']
supply = available_players['Position'].value_counts().to_dict()

# Handle FLEX logic: Assuming best value FLEX players are those with the highest auction value
flex_positions = ['RB', 'WR', 'TE']
flex_players = available_players[available_players['Position'].isin(flex_positions)].nlargest(roster_positions['FLEX'] * teams, 'Float Value')
for _, player in flex_players.iterrows():
    supply[player['Position']] -= 1

# Calculate scarcity factor for each position
scarcity_factor = {}
for position, count in total_demand.items():
    scarcity_factor[position] = count / supply.get(position, 1)

# Adjust the values for non-kept players
df.loc[df['Keeper'] != 'k', 'Adjusted Value'] = df['Value'].str.replace("$", "").astype(float) * inflation_rate * df['Position'].map(scarcity_factor)
df['Adjusted Value'] = df['Adjusted Value'].round(2).astype(str).apply(lambda x: "${}".format(x))

# Save the dataframe back to a CSV
output_path = r"C:\Users\jjese\OneDrive\Documents\GitHub\Fantasy_FB\adjusted_values.csv"
df.to_csv(output_path, index=False)

print(df)
