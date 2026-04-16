# Grocers

**Grocers** is an intelligent, agentic data system designed to help you navigate the chaos of grocery pricing. Instead of manual price checking, Grocers will help you you compare products from different stores.  

---

## The Project Goal
I am building a full-stack data and AI pipeline to solve the problem of turning messy, raw information into useful. Most people focus on the app interface, but this project is about the infrastructure that makes the intelligence work.

The system is built in three main parts:

Data Engineering
Most AI models fail because they use outdated information. I automated the data flow so there is a constant, clean stream of updates moving through the system without me having to touch it.

Storage and Persistence
By using SQL to store everything over time, lets the system look back at historical trends rather than just reacting to what is happening right now.

AI Orchestration
This is where the logic happens. Instead of just showing a list of data points, I am using LLM agents to look at the information, figure out what it means, and take action based on the current situation.

## Tech Stack
* **Language:** Python 3.13
* **Database:** SQLite (SQL)
* **Libraries:** `requests` for APIs, `sqlite3` for data storage.
* **API Sources:** Kroger Developer Portal (King Soopers).

---

## Project Structure
```text
GroceryApp/
├── scraping.py       # ETL Script (The Hose)
├── pantry.db         # SQL Database (The Bucket)
└── README.md         