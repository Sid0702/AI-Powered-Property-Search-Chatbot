import streamlit as st
from core.data_loader import load_data, get_known_values
from core.nlu import extract_filters_with_groq # Use the new Groq NLU function
from core.search import find_properties
from components.ui import render_property_card
from core.summarizer import generate_summary_from_results, generate_not_found_summary

# --- Page Configuration ---
st.set_page_config(
    page_title="NoBrokerage AI Property Finder",
    page_icon="🤖",
    layout="wide"
)

# --- Load Data and Initial Values (Cached) ---
# This runs only once at the start of the session.
with st.spinner("Loading property data..."):
    df = load_data()
    known_values = get_known_values(df)

# --- Main App UI ---
st.title("🤖 NoBrokerage AI Property Finder")
st.caption("Ask me to find properties, like 'Show me 2BHKs in Pune under 1 Cr '")

# --- Session State Initialization for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you find your dream property today?"}]

# --- Display Chat History ---
# This loop runs on every interaction to show the conversation so far.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        # If the message from the assistant has search results, display them as cards
        if "results" in msg and not msg["results"].empty:
            for _, row in msg["results"].iterrows():
                render_property_card(row)

# --- Handle User Input and Generate Response ---
if prompt := st.chat_input("e.g., 3bhk apartment in Ravet over 1 crore..."):
    # 1. Add user's message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Generate and display the assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your query and searching properties..."):
            
            # --- Core Logic ---
            # a. Use the Groq LLM to understand the query and extract filters
            filters = extract_filters_with_groq(prompt, known_values)
            
            # b. Search the database with the extracted filters
            results_df = find_properties(df, filters)
            
            # --- Construct and Display Response ---
            if "error" in filters:
                response_summary = f"Sorry, I encountered an error: {filters['error']}"
                st.write(response_summary)
                st.session_state.messages.append({"role": "assistant", "content": response_summary})

            elif not results_df.empty:
                # --- NEW: Generate the intelligent summary FIRST ---
                response_summary = generate_summary_from_results(results_df, filters)
                st.write(response_summary)

                # --- NEW: Limit the results for display AFTER analysis ---
                # We use head(5) here now, instead of in the search.py file.
                results_to_display = results_df.head(5)

                # Display property cards for the limited results
                st.write("Here are the top matching properties for you:")
                for _, row in results_to_display.iterrows():
                    render_property_card(row)

                # Add the full response (summary + display data) to session state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_summary, 
                    "results": results_to_display
                })
            
            else:
                # This handles both "impossible_query" and regular no-match scenarios
                # --- NEW: Generate a specific "not found" message using the filters ---
                fallback_response = generate_not_found_summary(filters)
                st.write(fallback_response)
                st.session_state.messages.append({"role": "assistant", "content": fallback_response})
