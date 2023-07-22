# Entry model
# has following fields:
# Name of the person, company
# job location (city name) or remote
# Job Title (Flutter Developer, Android Developer, etc)
# Platform (LinkedIn, Indeed, etc)
# Salary (in LPA)
# Experience (in years)
# Type (Company, Person, Post, Job Posting or Other)
# URL (URL of the job posting)
# Status (New, Applied, Interview, Rejected, Offered, Joined, Other)
#  Ceate a model for Entry below


class Entry:
    def __init__(self, id, name, location, job_title, platform, salary, experience, type, url, status):
        self.id = id
        self.name = name
        self.location = location
        self.job_title = job_title
        self.platform = platform
        self.salary = salary
        self.experience = experience
        self.type = type
        self.url = url
        self.status = status

    def copy(self, other_entry):
        self.id = other_entry.id
        self.name = other_entry.name
        self.location = other_entry.location
        self.job_title = other_entry.job_title
        self.platform = other_entry.platform
        self.salary = other_entry.salary
        self.experience = other_entry.experience
        self.type = other_entry.type
        self.url = other_entry.url
        self.status = other_entry.status
