import streamlit as st

def render_property_card(prop):
    """
    Renders a single property card with an image, details, and a CTA link.
    """
    # Use a container with a border for better visual separation
    with st.container(border=True):
        # UPDATED: Changed column ratio from [1, 2] to [1, 3] to make the image smaller.
        col1, col2 = st.columns([1, 3])

        with col1:
            # st.image(prop['first_image'],  width='stretch')
            st.image(prop['first_image'], width='stretch')


        with col2:
            # Use a slightly smaller header for the title to save space
            st.subheader(prop['title'], divider='rainbow')
            
            # Sub-columns for better layout of details
            detail_col1, detail_col2 = st.columns(2)
            with detail_col1:
                st.markdown(f"**📍 {prop['city']}, {prop['locality']}**")
                st.markdown(f"**Project:** {prop['project_name']}")
            with detail_col2:
                st.markdown(f"**Type:** {prop['bhk'].upper()}")
                st.markdown(f"**Status:** {prop['possession_status'].replace('_', ' ').title()}")
            
            # Make the price more prominent
            st.markdown(f"#### Price: {prop['price_formatted']}")
            
            # Display top 3 amenities if available
            amenities_str = prop.get('amenities', '') # Use .get() for safety
            if isinstance(amenities_str, str) and 'no amenities' not in amenities_str.lower() and 'not specified' not in amenities_str.lower():
                amenities_list = [a.strip() for a in amenities_str.split(',')[:3]]
                st.write("✨ **Amenities:** " + " | ".join(amenities_list))

            # Add a button for the call to action
            st.link_button("View Details", "https://nobrokerage.com" + prop['cta_url'])

