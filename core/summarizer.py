import pandas as pd

def format_price_for_summary(filters: dict) -> str:
    """Formats the budget from the filters for use in the summary string."""
    budget = filters.get("budget", {})
    if "max" in budget:
        price_in_cr = budget['max'] / 10000000
        return f"Within your budget of ₹{price_in_cr:.1f} Cr"
    if "min" in budget:
        price_in_cr = budget['min'] / 10000000
        return f"Over your budget of ₹{price_in_cr:.1f} Cr"
    return "For your search"

# --- NEW HELPER FUNCTION ---
# This helps format the raw price numbers into "Cr" or "L" strings.
# It's based on the logic from your preprocessing.py file.
def format_price_value(price: float) -> str:
    """Formats a numeric price into a string like '₹1.2 Cr' or '₹75 L'."""
    if pd.isna(price):
        return ""
    if price >= 10000000:
        return f"₹{price / 10000000:.2f} Cr"
    else:
        return f"₹{price / 100000:.2f} L"

def generate_summary_from_results(results_df: pd.DataFrame, filters: dict) -> str:
    """
    Analyzes the search results DataFrame and generates a dynamic, insightful summary.
    """
    total_found = len(results_df)
    if total_found == 0:
        return "I couldn't find any properties matching your exact criteria."

    # --- 1. Get Price Range from Actual Results (THE NEW LOGIC) ---
    price_range_summary = ""
    if total_found > 1:
        min_price = results_df['price'].min()
        max_price = results_df['price'].max()
        # Format the min and max prices using our new helper function
        min_price_formatted = format_price_value(min_price)
        max_price_formatted = format_price_value(max_price)
        price_range_summary = f" They range in price from **{min_price_formatted}** to **{max_price_formatted}**."

    # --- 2. Analyze Top Locations ---
    location_summary = ""
    if 'locality' in results_df.columns and not results_df['locality'].empty:
        top_locations = results_df['locality'].value_counts().nlargest(2).index.tolist()
        if len(top_locations) > 1:
            location_summary = f" Most are located in **{top_locations[0].title()}** and **{top_locations[1].title()}**."
        elif len(top_locations) == 1:
            location_summary = f" Most are located in **{top_locations[0].title()}**."

    # --- 3. Construct the Final Summary Sentence ---
    price_part = format_price_for_summary(filters)
    
    # Build the response piece by piece for better readability
    final_summary = f"I found **{total_found}** matching properties. {price_part}, the listings look promising."
    
    # Add the new price range summary
    final_summary += price_range_summary
    
    # Add the location summary
    final_summary += location_summary

    return final_summary.strip()

def generate_not_found_summary(filters: dict) -> str:
    """
    Creates a specific "not found" message based on the user's filters.
    e.g., "No ready 3BHK options found under ₹1.2 Cr in Baner."
    """
    # --- NEW: Handle invalid locations first ---
    if "invalid_location" in filters:
        invalid_loc = filters["invalid_location"].title()
        # The dataset only contains properties in Pune and Mumbai [cite: 12]
        return f"I'm sorry, I don't have property listings for {invalid_loc} at the moment. My current database is focused on Pune and Mumbai."

    parts = ["No"]

    # Add status if present
    if "status" in filters:
        status_formatted = filters['status'].replace('_', ' ').replace(' to move', '')
        parts.append(status_formatted)

    # Add property type (BHK) if present
    if "property_type" in filters:
        parts.append(filters['property_type'].upper())

    parts.append("options found")

    # Add budget details if present
    if "budget" in filters:
        budget = filters.get("budget", {})
        if "max" in budget:
            price_formatted = format_price_value(budget['max'])
            parts.append(f"under {price_formatted}")
        if "min" in budget:
            price_formatted = format_price_value(budget['min'])
            parts.append(f"over {price_formatted}")

    # Add location details if present
    if "locality" in filters:
        parts.append(f"in {filters['locality'].title()}")
    elif "city" in filters:
        parts.append(f"in {filters['city'].title()}")
        
    if len(parts) <= 2: # Only contains "No options found"
        return "I couldn't find any properties matching your exact criteria. You could try being less specific."

    return " ".join(parts) + "."