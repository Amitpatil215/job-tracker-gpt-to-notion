instruction = '''
Strictly return json object in the following format
{
"name" :
"location" :
"job_title" :
"platform" : 
"salary" :
"experience" :
"status" :
}

Please consider following rules
"name" is the name of person or company
"location" is the (city name) or remote or Other
"job_title" (Flutter Developer, Android Developer, etc)
"platform" is (Strictly one of these values -> LinkedIn, Twitter, Wellfound, or Other, can refer to domain of the URL)
"salary" (in LPA), if not avaialble put "NA"
"experience" (in years) if not available put 0

'''

def get_promt(raw_job_description, postUrl):
    return instruction +"Raw job description : " + raw_job_description + "\n" + "URL OF THE JOB DESCRIPTION: " + postUrl;