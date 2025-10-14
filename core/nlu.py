import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
try:
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in .env file.")
    client = Groq(api_key=groq_api_key)
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    client = None

# The correct model name for Llama 3 70B on Groq
MODEL_NAME = 'llama-3.3-70b-versatile'

def create_llm_prompt(query, known_values):
    """
    Creates a more robust and direct prompt for the LLM to extract filters,
    with improved handling for project names and amenities.
    """
    cities = list(known_values.get("cities", []))
    localities = list(known_values.get("localities", []))
    property_types = list(known_values.get("property_types", []))
    project_names = list(known_values.get("project_names", []))

    prompt = f"""
    You are an expert AI assistant for a property search website. Your task is to extract search filters from a user's query and return them as a valid JSON object.

    IMPORTANT INSTRUCTIONS:
    1.  **Be Precise:** Your ONLY output must be a valid JSON object. Do not add any extra text or explanations.
    2.  **Project Name vs. Location:** A project name is NOT a location. If the user query includes a name from the "Valid Project Names" list, extract it as `project_name`. DO NOT treat it as a location.
    3.  **Location Check:** If the user's query contains a location (city or locality) that is NOT in the "Valid Cities" or "Valid Localities" lists, you MUST return `{{"impossible_query": true}}`.
    4.  **Budget Analysis:** Analyze terms like "under", "over", "less than", "more than" to set "min" or "max" values in a "budget" object. The value must be an integer in Rupees.
    5.  **Amenity Extraction:** If the user mentions amenities like "gym", "pool", "security", etc., you MUST include them in an "amenities" list in the JSON.
    6.  **Status Detection:** Look for terms like "ready to move" or "ready" and set a "status" key to "ready_to_move".

    DATABASE VALUES:
    -   Valid Cities: {cities}
    -   Valid Localities: {localities}
    -   Valid Property Types: {property_types}
    -   Valid Project Names: {project_names}

    EXAMPLES:

    User Query: "Show me 2BHKs in Pune under 1 Cr with a gym"
    JSON Response:
    {{
      "city": "pune",
      "property_type": "2bhk",
      "budget": {{
        "max": 10000000
      }},
      "amenities": ["gym"]
    }}

    User Query: "Show me properties in the Pristine02 project"
    JSON Response:
    {{
      "project_name": "pristine02"
    }}

    User Query: "Dehradun property"
    JSON Response:
    {{
      "impossible_query": true
    }}
    
    ---
    Now, process the following user query.

    User Query: "{query}"
    JSON Response:
    """
    return prompt

def extract_filters_with_groq(query, known_values):
    """
    Uses the Groq API and an LLM to extract filters, then standardizes and prints the output.
    """
    if not client:
        return {"error": "Groq client not initialized. Check API key."}

    prompt = create_llm_prompt(query, known_values)

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME,
            temperature=0,
            response_format={"type": "json_object"},
        )
        
        response_text = chat_completion.choices[0].message.content
        filters = json.loads(response_text)

        # Standardization Step
        key_mappings = {
            "bhk": "property_type",
            "type": "property_type",
            "property type": "property_type"
        }
        standardized_filters = {}
        for key, value in filters.items():
            new_key = key_mappings.get(key.lower(), key)
            standardized_filters[new_key] = value

        # Print the final JSON to the terminal for debugging
        print("="*50)
        print(f"Query: '{query}'")
        print(f"Extracted JSON Filters: {json.dumps(standardized_filters, indent=2)}")
        print("="*50)

        return standardized_filters

    except Exception as e:
        print(f"An error occurred with the Groq API call: {e}")
        return {"error": "Failed to parse query. Please try again."}

