# WildFly Log Analyzer with LLM Integration

This project allows you to upload WildFly .log files, automatically extract and analyze errors, and get concise, actionable insights powered by a large language model (LLM). It’s designed for backend engineers, DevOps, and SRE teams who want to speed up troubleshooting and root cause identification.

# 🚀 Project Overview

<img width="750" height="550" alt="image" src="https://github.com/user-attachments/assets/ca99fbf9-61aa-472d-9bbe-4324f406821b" />

<img width="696" height="373" alt="Screenshot 2026-02-16 at 21 31 01" src="https://github.com/user-attachments/assets/0c96c387-4e71-47d7-8c99-a1b0b50ba92c" />


# 🛠 Features

1. Log Parsing & Preprocessing

    - Extracts log entries at ERROR level.
    - Deduplicates repeated messages.
   
    - Counts occurrences for all errors.
   
    - Handles large log files efficiently with streaming reads.

3. Top N Error Analysis

    - Sorts errors by occurrence.
    
    - Selects the Top N most frequent errors (configurable via API).
    
    - Passes Top N errors to an LLM for root cause analysis and exact solutions.

3. LLM Integration

    - Uses OpenAI GPT-4.1 to analyze errors.
    
    - Generates concise technical explanations and actionable fixes.
    

4. FastAPI Web Interface

    - Upload logs via REST API.
    
    - Returns a structured JSON with:
    
        - Top N errors + LLM analysis.
     
        - Full sorted count of all errors.
    
    - Flexible top_n parameter to control number of errors analyzed.

5. Additional Utilities

    - Text summarization, keyword extraction, and title generation for general documents.
    
    - Modular architecture for easy extension of analysis tools.

    - Supports multiple languages (English and Chinese).
      
