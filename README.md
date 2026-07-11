# capstone-project-part-4
 Project Overview
"For this project, I built an automated data extraction pipeline using an LLM. The goal was to take messy, raw text and turn it into clean, organized JSON data that my code can actually use. I chose Track A because I wanted to focus on getting reliable, structured results from the AI."
How I Built It
"To make the project reliable and secure, I followed these steps:
 Prompting: I created a system prompt that tells the AI to act specifically as a 'data extractor.' By setting the temperature to 0, I ensured the AI provides the exact same, predictable answer every time, rather than guessing or getting creative.
 Security: I kept my API key completely out of the code. I used a separate environment file (⁠use.env⁠) to store the key, ensuring it would never be accidentally shared or uploaded to GitHub.
 Safety Guardrails: I added a simple check to scan for private information (like emails). If the code detects sensitive data, it blocks the process to keep the information safe."
Performance Demonstration
"I tested the pipeline with different types of data. Here is what happened:"
   input                        output         status    
   raw text                     cleanjson      pass
   clean data                   cleanjs        pass
   text containing an email     blocked        pass(safety check||)
Why I chose Temperature 0
"I set the temperature to 0 because, in data extraction, you don't want the AI to be 'imaginative.' You want it to be a robot that follows instructions perfectly. Higher temperatures (like 0.7) allow the AI to be random, which is fun for chatting, but it causes errors when you need to fill out a strict JSON form."
