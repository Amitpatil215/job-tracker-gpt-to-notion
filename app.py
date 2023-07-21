# Initialisation

import requests
import json
import promts as promts
import openai

from entry import Entry

openai.api_key = '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'
token = 'secret_K0TlVmzAnjnC6JxdjX91DkJ1vGPodOv6b7XMKgWu2Ap'
databaseID = "d045fb49e8de4e2486a2888da49d08b8"
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}


# create a chat completion
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a job seeker and want to extract info from raw job description,"}, {"role": "user", "content": promts.instruction + promts.rawJobDescription},])

# print the chat completion
# print(chat_completion.choices[0].message.content)
gptJsonResponse = chat_completion.choices[0].message.content

decodedGptJsonResponse = json.loads(gptJsonResponse)

# Accessing the parsed data
name = decodedGptJsonResponse["name"]
location = decodedGptJsonResponse["location"]
job_title = decodedGptJsonResponse["job_title"]
platform = decodedGptJsonResponse["platform"]
salary = decodedGptJsonResponse["salary"]
experience = decodedGptJsonResponse["experience"]
job_type = decodedGptJsonResponse["type"]
url = decodedGptJsonResponse["url"]
status = decodedGptJsonResponse["status"]

# Printing the parsed data
print("Name:", name)
print("Location:", location)
print("Job Title:", job_title)
print("Platform:", platform)
print("Salary:", salary)
print("Experience:", experience)
print("Job Type:", job_type)
print("URL:", url)
print("Status:", status)


entry = Entry(
    name=decodedGptJsonResponse["name"],
    location=decodedGptJsonResponse["location"],
    job_title=decodedGptJsonResponse["job_title"],
    platform=decodedGptJsonResponse["platform"],
    salary=decodedGptJsonResponse["salary"],
    experience=decodedGptJsonResponse["experience"],
    type=decodedGptJsonResponse["type"],
    url=decodedGptJsonResponse["url"],
    status="New"
)

# Response a Database


def responseDatabase(databaseID, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseID}"
    res = requests.request("GET", readUrl, headers=headers)
    print(res.status_code)
    print(res.text)

# Create a Page

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
                "number": entry.salary
            },
            "Experience": {
                "number": 2
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
    print(res.status_code)
    print(res.text)


createPage(databaseID, entry=entry, headers=headers)
# responseDatabase(databaseID, headers)
