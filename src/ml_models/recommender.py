import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def get_data_path(filename):
    return os.path.join(PROJECT_ROOT, 'data', filename)

def load_customer_data(filepath):
    return pd.read_csv(filepath)

def create_user_item_matrix(df):
    return df.pivot_table(index='CustomerID', columns='Drink', values='Rating').fillna(0)

def recommend_drinks(customer_id, customer_df, top_n=3):
    # Load drink profiles
    drink_profiles = pd.read_csv(get_data_path("drink_profiles.csv"))
    
    # Get drinks this customer already ordered
    customer_orders = customer_df[customer_df["CustomerID"] == customer_id]
    if customer_orders.empty:
        # Fallback: recommend random drinks
        return drink_profiles["Drink"].sample(top_n).tolist()
    
    # Find most frequently ordered drink
    favorite_drink = customer_orders["Drink"].value_counts().idxmax()
    
    # Get flavor of favorite drink
    favorite_flavor = drink_profiles.loc[
        drink_profiles["Drink"] == favorite_drink, "Flavor"
    ].values[0]
    
    # Recommend drinks with the same flavor, excluding already ordered ones
    similar_drinks = drink_profiles[
        (drink_profiles["Flavor"] == favorite_flavor) &
        (~drink_profiles["Drink"].isin(customer_orders["Drink"]))
    ]["Drink"].tolist()
    
    if similar_drinks:
        return similar_drinks[:top_n]
    else:
        # fallback: random drinks
        return drink_profiles["Drink"].sample(top_n).tolist()
    
def get_customer_taste_profile(customer_id, customer_orders_file, drink_profiles_file):
    # loading csv files 
    orders_df = pd.read_csv(get_data_path("customer_orders.csv"))
    drinks_df = pd.read_csv(get_data_path("drink_profiles.csv"))

    # merging files 
    drink_orders = orders_df.merge(drinks_df, on="Drink", how="left")

    # filtering for customer
    customer_df = drink_orders[drink_orders["CustomerID"] == customer_id]

    # creating summary preference
    flavor_counts = customer_df["Flavor"].value_counts().to_dict()

    return {
        "flavor": flavor_counts,
        "orders": customer_df
    }

def recommend_drinks_based_on_taste(taste_profile, drink_profiles_file):
    # Build absolute path to drink_profiles.csv
    drink_profiles_path = os.path.join(PROJECT_ROOT, drink_profiles_file)
    drinks_df = pd.read_csv(drink_profiles_path)

    # Extract preferences from taste_profile
    favorite_flavors = list(taste_profile.get("flavor", {}).keys())
    favorite_caffeine = list(taste_profile.get("caffeine", {}).keys())[0] if taste_profile.get("caffeine") else None

    # For simplicity, assume preferences (you could make these dynamic later)
    preferred_sweetness = "Medium"  
    preferred_milk = "Yes"          

    # Filter drinks by taste profile
    recommended_drinks = drinks_df[
        (drinks_df["Flavor"].isin(favorite_flavors)) &
        ((drinks_df["CaffeineLevel"] == favorite_caffeine) if favorite_caffeine else True) &
        (drinks_df["Sweetness"] == preferred_sweetness) &
        (drinks_df["Milk"] == preferred_milk)
    ]

    # Sort by Season if available
    if "Season" in drinks_df.columns:
        recommended_drinks = recommended_drinks.sort_values(by="Season", ascending=False)

    return recommended_drinks