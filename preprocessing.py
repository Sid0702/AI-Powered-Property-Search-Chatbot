import pandas as pd
import numpy as np
import re
import warnings
import os

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Define data directory
DATA_DIR = "data"

def format_price(price):
    """Formats a numeric price into a string like '₹1.2 Cr' or '₹75 L'."""
    if pd.isna(price):
        return "Price on request"
    price = float(price)
    if price >= 10000000:
        return f"₹{price / 10000000:.2f} Cr"
    else:
        return f"₹{price / 100000:.2f} L"

def extract_location_from_slug(slug):
    """Extracts city and locality from the project slug."""
    try:
        slug = str(slug).lower()
        parts = slug.split('-')
        text_parts = [p for p in parts if not p.isdigit()]
        if len(text_parts) >= 2:
            city = text_parts[-1]
            locality = text_parts[-2]
            if city in ['pune', 'mumbai']:
                return pd.Series([city.title(), locality.title()])
    except Exception:
        pass
    return pd.Series(['Unknown', 'Not specified'])

def extract_amenities(summary):
    """Extracts top 3 amenities from the project summary based on keywords."""
    if pd.isna(summary):
        return "No amenities listed"

    summary = str(summary).lower()
    amenities_list = {
        'Swimming Pool': ['pool', 'swimming'],
        'Gymnasium': ['gym', 'gymnasium', 'fitness center'],
        'Clubhouse': ['clubhouse', 'club house'],
        'Car Parking': ['parking', 'car park'],
        'Lift': ['lift', 'elevator'],
        'Kids Play Area': ['play area', 'kids area'],
        'Security': ['security', 'cctv'],
        'Good Connectivity': ['connectivity'],
        'Nearby Schools': ['schools', 'school'],
        'Nearby Hospitals': ['hospitals', 'hospital'],
        'Shopping Access': ['shopping', 'malls'],
        'Modern Living': ['modern living', 'contemporary features'],
        'Good Infrastructure': ['infrastructure']
    }

    found_amenities = [amenity for amenity, keywords in amenities_list.items() if any(keyword in summary for keyword in keywords)]

    if not found_amenities:
        return "Key amenities not specified"

    return ', '.join(found_amenities[:3])

def clean_bathrooms(row):
    """If bathrooms > 5, sets the count to the number of BHKs."""
    try:
        bhk_num = float(re.findall(r'\d+', str(row['bhk']))[0])
        bathrooms = float(row['bathrooms'])
        if bathrooms > 5:
            return bhk_num
        else:
            return bathrooms
    except (IndexError, ValueError):
        return row['bathrooms']


# --- 1. LOAD THE DATA ---
print("Step 1: Loading raw CSV files...")
try:
    project_df = pd.read_csv(os.path.join(DATA_DIR, 'project.csv'))
    address_df = pd.read_csv(os.path.join(DATA_DIR, 'ProjectAddress.csv'))
    config_df = pd.read_csv(os.path.join(DATA_DIR, 'ProjectConfiguration.csv'))
    variant_df = pd.read_csv(os.path.join(DATA_DIR, 'ProjectConfigurationVariant.csv'), sep=',', engine='python', quotechar='"')
    print("✅ All files loaded successfully.")
except FileNotFoundError as e:
    print(f"❌ Error: {e}\nPlease make sure all CSV files are inside the 'data' folder.")
    exit()


# --- 2. MERGE THE FILES ---
print("\nStep 2: Merging the four data files...")
merged_df = pd.merge(variant_df, config_df, left_on='configurationId', right_on='id', how='left', suffixes=('_variant', '_config'))
merged_df = pd.merge(merged_df, project_df, left_on='projectId', right_on='id', how='left', suffixes=('', '_project'))
merged_df = pd.merge(merged_df, address_df, on='projectId', how='left', suffixes=('', '_address'))


# --- 3. SELECT AND RENAME IMPORTANT COLUMNS ---
print("\nStep 3: Selecting and renaming important columns...")
columns_to_keep = {
    'projectName': 'project_name', 'status': 'possession_status', 'slug': 'slug',
    'fullAddress': 'address', 'pincode': 'pincode', 'type': 'bhk', 'price': 'price',
    'carpetArea': 'area_sqft', 'bathrooms': 'bathrooms', 'furnishedType': 'furnishing',
    'projectSummary': 'summary', 'possessionDate': 'possession_date', 'propertyImages': 'images_url'
}
processed_df = merged_df[list(columns_to_keep.keys())].copy()
processed_df.rename(columns=columns_to_keep, inplace=True)


# --- 4. CLEAN AND PREPROCESS DATA ---
print("\nStep 4: Cleaning and preprocessing data...")
processed_df['price'] = pd.to_numeric(processed_df['price'], errors='coerce')
processed_df['area_sqft'] = pd.to_numeric(processed_df['area_sqft'], errors='coerce')
processed_df['bathrooms'] = pd.to_numeric(processed_df['bathrooms'], errors='coerce')
processed_df.dropna(subset=['project_name', 'price', 'bhk'], inplace=True)
processed_df['furnishing'].fillna('Not Specified', inplace=True)
processed_df['bathrooms'] = processed_df.apply(clean_bathrooms, axis=1)
processed_df['bathrooms'].fillna(0, inplace=True)
processed_df['address'] = processed_df['address'].str.lower()


# --- 5. FEATURE ENGINEERING ---
print("\nStep 5: Engineering new features for the chatbot...")
processed_df['price_formatted'] = processed_df['price'].apply(format_price)
processed_df['cta_url'] = '/project/' + processed_df['slug'].astype(str)
processed_df[['city', 'locality']] = processed_df['slug'].apply(extract_location_from_slug)
processed_df['amenities'] = processed_df['summary'].apply(extract_amenities)
processed_df['title'] = processed_df['bhk'] + ' Apartment in ' + processed_df['project_name']


# --- 6. CREATE THE FINAL MASTER FILE ---
print("\nStep 6: Creating the final master file for the application...")
final_columns = [
    'title', 'project_name', 'city', 'locality', 'bhk', 'price_formatted',
    'possession_status', 'amenities', 'cta_url', 'area_sqft', 'bathrooms',
    'furnishing', 'address', 'images_url', 'summary', 'price'
]
master_df = processed_df[final_columns].copy()
output_path = os.path.join(DATA_DIR, 'master_properties.csv')
master_df.to_csv(output_path, index=False)

print(f"\n✅ Data preparation complete! Final file saved at: {output_path}")
