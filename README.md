WildFly Log Analyzer with LLM Integration

A Python & FastAPI project to parse WildFly logs, extract ERROR-level entries, perform Top N analysis, and leverage LLMs for automated root cause analysis.

🚀 Project Overview

This project allows you to upload WildFly .log files, automatically extract and analyze errors, and get concise, actionable insights powered by a large language model (LLM). It’s designed for backend engineers, DevOps, and SRE teams who want to speed up troubleshooting and root cause identification.

🛠 Features

Log Parsing & Preprocessing

Extracts log entries at ERROR level.

Deduplicates repeated messages.

Counts occurrences for all errors.

Handles large log files efficiently with streaming reads.

Top N Error Analysis

Sorts errors by occurrence.

Selects the Top N most frequent errors (configurable via API).

Passes Top N errors to an LLM for root cause analysis and exact solutions.

LLM Integration

Uses OpenAI GPT-4.1 to analyze errors.

Generates concise technical explanations and actionable fixes.

Supports multiple languages (English and Chinese).

FastAPI Web Interface

Upload logs via REST API.

Returns a structured JSON with:

Top N errors + LLM analysis.

Full sorted count of all errors.

Flexible top_n parameter to control number of errors analyzed.

Additional Utilities

Text summarization, keyword extraction, and title generation for general documents.

Modular architecture for easy extension of analysis tools.