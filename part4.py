{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNo3Y5rze7kmzzpS1Guiy/x",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/aaminabenazir/capstone-project-part-4/blob/main/part4.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import os\n",
        "import json\n",
        "import requests\n",
        "import pandas as pd\n",
        "import re\n",
        "import time\n",
        "# This grabs the key you already saved in the Render dashboard\n",
        "os.environ['LLM_API_KEY'] = os.environ.get('OPENROUTER_API_KEY')\n",
        "\n",
        "'''# 1. Securely load API Key\n",
        "try:\n",
        "    with open('use.env', 'r') as f:\n",
        "        content = f.read().strip()\n",
        "        key = content.split(\"=\")[1] if \"=\" in content else content\n",
        "        os.environ['LLM_API_KEY'] = key\n",
        "        print(\"API Key loaded successfully.\")\n",
        "except Exception as e:\n",
        "    print(f\"Error loading use.env: {e}\")'''\n",
        "\n",
        "# 2. Load Data from Part 3\n",
        "try:\n",
        "    df = pd.read_csv('cleaned_data.csv')\n",
        "    data_sample = df.iloc[0].to_string()\n",
        "    print(\"Data loaded from Part 3.\")\n",
        "except Exception as e:\n",
        "    print(f\"Error loading CSV: {e}\")\n",
        "    data_sample = \"longitude: -114.31, latitude:34.05, category:location\"\n",
        "\n",
        "# 3. Call LLM with Stable Model ID\n",
        "def call_llm(user_input):\n",
        "    # Added delay to respect rate limits\n",
        "    time.sleep(2)\n",
        "\n",
        "    url = \"https://openrouter.ai/api/v1/chat/completions\"\n",
        "    headers = {\n",
        "        \"Authorization\": f\"Bearer {os.environ.get('LLM_API_KEY')}\",\n",
        "        \"Content-Type\": \"application/json\"\n",
        "    }\n",
        "\n",
        "    system_prompt = \"You are a data extractor. Output ONLY raw valid JSON. Do not include markdown, code blocks, or text.\"\n",
        "\n",
        "    # Using verified stable model slug\n",
        "    payload = {\n",
        "        \"model\": \"meta-llama/llama-3.1-8b-instruct\", # Updated model slug as per error message\n",
        "        \"messages\": [{\"role\": \"system\", \"content\": system_prompt}, {\"role\": \"user\", \"content\": user_input}],\n",
        "        \"temperature\": 0.0\n",
        "    }\n",
        "\n",
        "    try:\n",
        "        response = requests.post(url, headers=headers, json=payload, timeout=30)\n",
        "        print(f\"DEBUG: Status Code: {response.status_code}\")\n",
        "\n",
        "        if response.status_code == 200:\n",
        "            return response.json()['choices'][0]['message']['content']\n",
        "        else:\n",
        "            print(f\"DEBUG: Response Text: {response.text}\")\n",
        "            return None\n",
        "    except Exception as e:\n",
        "        print(f\"DEBUG: Connection error: {e}\")\n",
        "        return None\n",
        "\n",
        "# 4. Pipeline Execution\n",
        "def run_pipeline(input_text):\n",
        "    raw_response = call_llm(f\"Extract details from: {input_text}\")\n",
        "\n",
        "    if not raw_response:\n",
        "        return \"Error: No response from LLM\"\n",
        "\n",
        "    try:\n",
        "        # CLEANING: Remove markdown formatting\n",
        "        clean_json = re.sub(r'```json|```', '', raw_response).strip()\n",
        "        data = json.loads(clean_json)\n",
        "        return data\n",
        "    except Exception as e:\n",
        "        print(f\"DEBUG: Parsing error: {e}\")\n",
        "        print(f\"DEBUG: Raw response was: {raw_response}\")\n",
        "        return \"Error: Could not parse JSON\"\n",
        "\n",
        "# Execution\n",
        "result = run_pipeline(data_sample)\n",
        "print(\"Pipeline Result:\", result)"
      ],
      "metadata": {
        "id": "Wl35in2GVlkB"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}