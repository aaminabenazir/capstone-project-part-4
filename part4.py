import os
import json
import requests
import pandas as pd
import re
import time
# This grabs the key you already saved in the Render dashboard
os.environ['LLM_API_KEY'] = os.environ.get('OPENROUTER_API_KEY')

'''# 1. Securely load API Key
try:
    with open('use.env', 'r') as f:
        content = f.read().strip()
        key = content.split("=")[1] if "=" in content else content
        os.environ['LLM_API_KEY'] = key
        print("API Key loaded successfully.")
except Exception as e:
    print(f"Error loading use.env: {e}")'''

# 2. Load Data from Part 3
try:
    df = pd.read_csv('cleaned_data.csv')
    data_sample = df.iloc[0].to_string()
    print("Data loaded from Part 3.")
except Exception as e:
    print(f"Error loading CSV: {e}")
    data_sample = "longitude: -114.31, latitude:34.05, category:location"

# 3. Call LLM with Stable Model ID
def call_llm(user_input):
    # Added delay to respect rate limits
    time.sleep(2)

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ.get('LLM_API_KEY')}",
        "Content-Type": "application/json"
    }

    system_prompt = "You are a data extractor. Output ONLY raw valid JSON. Do not include markdown, code blocks, or text."

    # Using verified stable model slug
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct", # Updated model slug as per error message
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        "temperature": 0.0
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"DEBUG: Status Code: {response.status_code}")

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print(f"DEBUG: Response Text: {response.text}")
            return None
    except Exception as e:
        print(f"DEBUG: Connection error: {e}")
        return None

# 4. Pipeline Execution
def run_pipeline(input_text):
    raw_response = call_llm(f"Extract details from: {input_text}")

    if not raw_response:
        return "Error: No response from LLM"

    try:
        # CLEANING: Remove markdown formatting
        clean_json = re.sub(r'```json|```', '', raw_response).strip()
        data = json.loads(clean_json)
        return data
    except Exception as e:
        print(f"DEBUG: Parsing error: {e}")
        print(f"DEBUG: Raw response was: {raw_response}")
        return "Error: Could not parse JSON"

# Execution
result = run_pipeline(data_sample)
print("Pipeline Result:", result)
