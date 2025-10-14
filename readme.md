# 🏠 AI-Powered Property Search Chatbot

An intelligent, conversational **property search chatbot** built with **Streamlit** and powered by the **Groq API (Llama 3)**.  
This chatbot allows users to search for properties using **natural language queries** instead of traditional filters.  

---

## 🚀 Core Features

- **Natural Language Understanding:** Parses complex user queries like  
  > “Show me 2BHKs in Pune under 1 Cr.”
- **Dynamic Filtering:** Extracts filters for city, locality, budget, property type, project name, and amenities.
- **Intelligent Summaries:** Provides human-like summaries of search results or suggestions if no matches are found.
- **Interactive UI:** A clean, GPT-style chat interface built with Streamlit.
- **Fast & Powerful NLU:** Uses the high-speed **Groq API with Llama 3 (llama-3.3-70b-versatile)** for state-of-the-art query understanding.

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend & Backend** | Streamlit |
| **Data Handling** | Pandas |
| **AI / NLU** | Groq API with Llama 3 (llama-3.3-70b-versatile) |
| **Language** | Python |

---

## 🏛️ How It Works

The application follows a simple yet powerful three-step pipeline:

1. **NLU (Natural Language Understanding):**  
   The user’s query is sent to the Groq API with a detailed prompt.  
   The **Llama 3 model** extracts key entities like *location*, *budget*, *property type*, and *amenities* and returns a structured JSON.

2. **Search & Filtering:**  
   The structured JSON is used to filter a **Pandas DataFrame** loaded from the project’s local CSV (`4_master_properties.csv`).

3. **UI & Summarization:**  
   The chatbot displays **property cards** and generates a **dynamic summary** of the results in the chat interface.

---

## ▶️ Live Demo

🔗 **Live Application:** [Click Here to Try the Demo](https://ai-powered-property-search-chatbot.streamlit.app/)

---

## 🛠️ Setup and Installation

Follow these steps to run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/Sid0702/AI-Powered-Property-Search-Chatbot.git
cd AI-Powered-Property-Search-Chatbot
```

### 2. Create a Virtual Environment

It’s recommended to use a virtual environment to manage dependencies.

**For Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**For macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root and add your **Groq API key**:

```bash
GROQ_API_KEY="gsk_YourSecretApiKeyHere"
```

---

## ▶️ Run the Application

Once setup is complete, run the Streamlit app with:

```bash
streamlit run app.py
```

Your web browser will automatically open the chatbot interface.

---

## 💬 Example Queries

Try these example queries:

* “Show me properties in Pune”
* “2BHK in Chembur under 2 crore”
* “Find a villa in Pune that is over 4 Cr”
* “Ready-to-move properties in Shivajinagar”
* “Show me properties in the Pristine02 project”
* “2BHKs in Pune under 1 Cr”

---

## 📂 Project Structure

```
/nobrokerage-chatbot/
├── .streamlit/         # Streamlit configuration (optional)
├── components/         # UI helper functions
│   ├── __init__.py     # Makes 'components' a Python package
│   └── ui.py           # Renders the property card
├── core/               # Core backend logic
│   ├── __init__.py     # Makes 'core' a Python package
│   ├── data_loader.py  # Loads and preprocesses CSV data
│   ├── nlu.py          # Handles NLU with Groq API
│   └── search.py       # Filters DataFrame based on NLU output
├── data/               # Contains the property CSV file
│   ├── master_properties.csv
│   ├── project.csv
│   ├── ProjectAddress.csv
│   ├── ProjectConfiguration.csv
│   └── ProjectConfigurationVariant.csv
├── .env                # Stores secret API keys (not committed)
├── .gitignore          # Specifies files for Git to ignore
├── app.py              # Main Streamlit application
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```

---
