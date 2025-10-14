import streamlit as st
import pandas as pd
import ast

@st.cache_data
def load_data(csv_path='data/master_properties.csv'):
    """
    Loads, cleans, and preprocesses the property data from the CSV file.
    Caches the result to improve performance.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(f"Error: The file was not found at {csv_path}. Please make sure the file exists.")
        return pd.DataFrame()

    # --- Data Cleaning and Preprocessing ---
    df.columns = df.columns.str.strip().str.lower()

    # Clean text columns by stripping whitespace
    for col in ['city', 'locality', 'project_name', 'bhk', 'possession_status']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df.dropna(subset=['price'], inplace=True)

    if 'images_url' in df.columns:
        def get_first_image(urls_str):
            try:
                urls_list = ast.literal_eval(urls_str)
                if isinstance(urls_list, list) and urls_list and isinstance(urls_list[0], str):
                    return urls_list[0].strip('"')
            except (ValueError, SyntaxError, TypeError):
                pass
            return "https://www.home-invest.be/wp-content/uploads/2022/10/placeholder-home-invest.jpeg"
        df['first_image'] = df['images_url'].apply(get_first_image)

    if 'bhk' in df.columns:
        # Create a standardized property_type column for better matching
        df['property_type'] = df['bhk'].str.lower()

    return df

@st.cache_data
def get_known_values(_df):
    """
    Extracts unique values from the DataFrame for the NLU model to use.
    """
    if _df.empty:
        return {}
        
    known_values = {
        "cities": set(_df['city'].dropna().str.lower()),
        "localities": set(_df['locality'].dropna().str.lower()),
        "project_names": set(_df['project_name'].dropna().str.lower()),
        "property_types": set(_df['property_type'].dropna())
    }
    return known_values
