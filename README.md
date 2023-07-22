# Application Tracker ( NOTION -> GPT -> NOTION )
This project is a Python script that extracts information from raw job descriptions using the OpenAI GPT-3.5-turbo model and interacts with the Notion API to store and modify the extracted data.

## Features

- Extracts information from raw job descriptions using OpenAI GPT-3.5-turbo model.
- Retrieves and manipulates data from a Notion database.
- Creates new pages in a Notion database with the extracted information.
- Deletes pages from a Notion database.

## Architecture

The project consists of the following components:

- `promts.py`: Contains prompt generation functions.
- `model/entry.py`: Defines the `Entry` class to represent the extracted job information.
- `model/page.py`: Defines the `Page` class to represent a Notion page.
- `model/rawData.py`: Defines the `RawData` class to represent the raw job description data.
- `.env`: Environment variables file containing API keys and database IDs.
- `README.md`: This README file.
- `main.py`: The main Python script that performs the extraction and interaction with the Notion API.

The script uses the `requests` library to make HTTP requests to the Notion API and the `openai` library to interact with the OpenAI GPT-3.5-turbo model. It also uses the `dotenv` library to load environment variables from the `.env` file.

## How to Use

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Set up the required environment variables in the `.env` file. You will need the Notion API token, job database ID, and raw database ID.
4. Run the script using `python main.py`. The script will extract information from the raw job descriptions, create new pages in the job database, and delete the corresponding pages from the raw database.

Make sure you have the necessary permissions and access to the Notion workspace and databases before running the script.