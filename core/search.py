import pandas as pd

def find_properties(df, filters):
    """
    Filters the DataFrame using a robust boolean indexing method to ensure all
    filters are strictly and correctly applied.
    """
    if df.empty or filters.get("impossible_query"):
        return pd.DataFrame()

    # Start with a clean copy of the DataFrame to filter
    results = df.copy()

    # Apply filters sequentially. Each step narrows down the 'results' DataFrame.

    # --- String Filters ---
    if filters.get("city"):
        results = results[results['city'].str.lower() == filters["city"].lower()]
    
    if filters.get("locality"):
        results = results[results['locality'].str.lower() == filters["locality"].lower()]

    if filters.get("project_name"):
        results = results[results['project_name'].str.lower() == filters["project_name"].lower()]
        
    if filters.get("property_type"):
        results = results[results['property_type'].str.lower() == filters["property_type"].lower()]
    
    if filters.get("status"):
        results = results[results['possession_status'].str.lower() == filters["status"].lower()]

    # --- Budget Filters ---
    if filters.get("budget"):
        if "min" in filters["budget"]:
            min_price = filters["budget"]["min"]
            # Ensure the price column and the filter value are the same type (numeric)
            results = results[pd.to_numeric(results['price']) >= min_price]
        if "max" in filters["budget"]:
            max_price = filters["budget"]["max"]
            results = results[pd.to_numeric(results['price']) <= max_price]

    # --- Amenity Filters ---
    if filters.get("amenities"):
        for amenity in filters["amenities"]:
            # Ensure we only filter if the 'amenities' column exists and is not empty
            if 'amenities' in results.columns:
                results = results[results['amenities'].str.contains(amenity, case=False, na=False)]
            
    return results.head(5) # Return top 5 matches
