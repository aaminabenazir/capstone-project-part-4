# capstone-project-part-4
 
Data Extraction Pipeline (Part 4)
Overview
This project component implements an automated data extraction pipeline. It ingests raw, cleaned data from a CSV file and utilizes an LLM via the OpenRouter API to transform unstructured data into a structured, validated JSON format.
How the Code Works
The pipeline is structured into four main functional blocks to ensure reliability and maintainability:
1. Configuration & Security: The code securely loads an API key from an environment file (⁠use.env⁠) to ensure sensitive credentials are never hardcoded into the notebook.
2. Data Ingestion: The system reads the ⁠cleaned_data.csv⁠ file using ⁠pandas⁠. It extracts individual rows to be processed as data samples, allowing for scalable data handling.
3. LLM Interaction:
 The ⁠call_llm⁠ function sends the data sample to a stable LLM endpoint.
 Deterministic Output: The ⁠temperature⁠ is set to ⁠0.0⁠. This is critical for data extraction, as it removes "creativity" from the model to ensure consistent, reproducible results.
 System Prompting: A defined system prompt forces the model to output only raw, valid JSON, minimizing the need for heavy post-processing.
4. Parsing & Cleaning:
 The pipeline includes a cleaning step using regular expressions (⁠re.sub⁠) to strip away any markdown formatting or extraneous text that the LLM might return.
 The final response is validated using ⁠json.loads⁠ to confirm the structure is correct before the data is finalized.
Pipeline Performance
The table below demonstrates the pipeline’s ability to convert raw input into structured JSON output.
input sample(row)          extracted output(json)           validation status
inser row                      "key":"value"                   success
