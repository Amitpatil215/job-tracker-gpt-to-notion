# Initialisation

import requests
import json
import promts as promts
import openai
import traceback
import os
import logging

from model.entry import Entry
from model.page import Page
from model.rawData import RawData
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('openAiAPIKEY')

token = os.getenv('notionToken')
jobDBdatabaseID = os.getenv('jobDBdatabaseID')
rawDatabaseID = os.getenv('rawDatabaseID')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}


def getFormatedJSONFromChatGPT(rawJobDescription, jobPostingUrl):
    # create a chat completion
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a job seeker and want to extract info from raw job description,"}, {"role": "user", "content": promts.get_promt(rawJobDescription, jobPostingUrl)},])

    gptJsonResponse = chat_completion.choices[0].message.content

    decodedGptJsonResponse = json.loads(gptJsonResponse)

    # Accessing the parsed data
    name = decodedGptJsonResponse["name"]
    location = decodedGptJsonResponse["location"]
    job_title = decodedGptJsonResponse["job_title"]
    platform = decodedGptJsonResponse["platform"]
    salary = decodedGptJsonResponse["salary"]
    experience = decodedGptJsonResponse["experience"]

    entry = Entry(
        id="",
        name=decodedGptJsonResponse["name"],
        location=decodedGptJsonResponse["location"],
        job_title=decodedGptJsonResponse["job_title"],
        platform=decodedGptJsonResponse["platform"],
        salary=decodedGptJsonResponse["salary"],
        experience=decodedGptJsonResponse["experience"],
        type="",
        url="",
        status="New"
    )

    return entry

# Response a Database


def responseDatabase(databaseID, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseID}"
    res = requests.request("GET", readUrl, headers=headers)
    print(res.status_code)
    print(res.text)


def getCompleteDatabse(databaseID, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseID}/query"
    filterBody = {
        # "filter": {
        #     # "or": [
        #     #     {
        #     #         "property": "In stock",
        #     #         "checkbox": {
        #     #             "equals": True
        #     #         }
        #     #     },
        #     #     {
        #     #         "property": "Cost of next trip",
        #     #         "number": {
        #     #             "greater_than_or_equal_to": 2
        #     #         }
        #     #     }
        #     # ]
        # },
        # "sorts": [
        #     # {
        #     #     "property": "Last ordered",
        #     #     "direction": "ascending"
        #     # }
        # ]
    }
    data = json.dumps(filterBody)
    res = requests.request("POST", readUrl, headers=headers, data=data)
    jsonDecodedPageResponse = json.loads(res.text)
    page = Page.from_json(jsonDecodedPageResponse)
    # List of Entries
    listOfRowsInRawDB = []
    for p in page:
        pageId = p.id
        postUrl = p.properties["URL"]["url"]
        type = p.properties["Type"]["select"]["name"]
        rawDataString = ""
        rawDataList = p.properties["Raw Data"]["rich_text"]
        for rawData in rawDataList:
            rawDataString += rawData["text"]["content"]

        rawData = RawData(
            id=pageId,
            url=postUrl,
            raw_data=rawDataString,
            type=type
        )
        listOfRowsInRawDB.append(rawData)
    return listOfRowsInRawDB
# Create a Page


# returns status code
def createPage(databaseID, headers, entry):
    createUrl = 'https://api.notion.com/v1/pages'
    newPageData = {
        "parent": {"database_id": databaseID},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": entry.name
                        }
                    }
                ]
            },
            "Location": {
                "rich_text": [
                        {
                            "text": {
                                "content": entry.location
                            },
                        }
                ]
            },
            "Job Title": {
                "rich_text": [
                    {
                        "text": {
                            "content": entry.job_title
                        },
                    }
                ]
            },
            "Platform": {
                "select": {
                    "name": entry.platform
                }
            },
            # "Checkbox": {
            #         "checkbox": True
            #     },
            "Salary": {
                "rich_text": [
                    {
                        "text": {
                            "content": f"{entry.salary}"
                        },
                    }
                ]
            },
            "Experience": {
                "rich_text": [
                    {
                        "text": {
                            "content": f"{entry.experience}"
                        },
                    }
                ]
            },
            "Type": {
                "select": {
                    "name": entry.type
                }
            },
            "Status": {
                "select": {
                    "name": entry.status
                }
            },
            # "Multi-select": {
            #         "multi_select": [
            #             {
            #                 "name": "Apple",
            #             },
            #             {
            #                 "name": "Banana",
            #             }
            #         ]
            #     },
            # "Date": {
            #         "date": {
            #             "start": "2022-08-05",
            #             "end": "2022-08-10",
            #         }
            #     },
            "URL": {
                "url": entry.url
            },
            # "Email": {
            #         "email": "dolor@ipsum.com"
            #     },
            # "Phone": {
            #         "phone_number": "19191919"
            #     },
        }
    }
    data = json.dumps(newPageData)
    res = requests.request("POST", createUrl, headers=headers, data=data)
    if (res.status_code == 200):
        logger.debug('Created page having company name: ' + entry.name)
    else:
        logger.debug('Error in creating page, response from api: '+res.text)
    return res.status_code


def deletePage(headers, entry):
    createUrl = f'https://api.notion.com/v1/pages/{entry.id}'
    archivedPage = {
        "archived": True
    }
    data = json.dumps(archivedPage)
    res = requests.request("PATCH", createUrl, headers=headers, data=data)
    if (res.status_code == 200):
        logger.debug('Deleted page having company name: '+entry.name)


def execute():
    listOfRowsInRawDB = getCompleteDatabse(rawDatabaseID, headers)
    for row in listOfRowsInRawDB:
        try:
            # getting formated json from chat gpt
            entry = getFormatedJSONFromChatGPT(
                rawJobDescription=row.raw_data, jobPostingUrl=row.url
            )
            formatedEntry = Entry(
                id=row.id,
                name=entry.name,
                location=entry.location,
                job_title=entry.job_title,
                platform=entry.platform,
                salary=entry.salary,
                experience=entry.experience,
                type=row.type,
                url=row.url,
                status="New"
            )
            # Adding a new entry to the database
            createPageStatusCode = createPage(
                jobDBdatabaseID, entry=formatedEntry, headers=headers)
            # Deleting the entry from raw database
            if(createPageStatusCode==200):
                deletePage(headers=headers, entry=formatedEntry)
        except:
            logger.debug('Error in executing the script for url ->' +
                         row.url + " Continueing with next url if available")
            traceback.print_exc()
            continue


execute()
