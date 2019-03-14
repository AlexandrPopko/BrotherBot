import json
import requests

from config import Config
from jira.Collections import IssueCollection


class JiraProject:
    def __init__(self, data=None) -> None:
        super().__init__()
        self.data = data

    def get_name(self):
        return self.data['name']


class JiraStatus:
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data

    def get_id(self):
        return self.data['id']

    def get_name(self):
        return self.data['name']


class JiraUser:
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data

    def get_id(self):
        return self.data['key']

    def get_email(self):
        return self.data['emailAddress']

    def get_display_name(self):
        return self.data['displayName']


class JiraIssue:
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.host = None
        self.data = data
        self.assignee = None
        self.project = None
        self.status = None

    def set_host(self, host: str):
        self.host = host

    def get_id(self):
        return self.data['id']

    def get_key(self):
        return self.data['key']

    def get_status(self) -> JiraStatus:
        return self.status

    def set_status(self, status: JiraStatus):
        self.status = status

    def get_assignee(self) -> JiraUser:
        return self.assignee

    def set_assignee(self, user: JiraUser):
        self.assignee = user

    def get_project(self) -> JiraProject:
        return self.project

    def set_project(self, project: JiraProject):
        self.project = project

    def get_url(self):
        return '%s/browse/%s' % (Config.JIRA_HOST, self.get_key())

    def get_type(self):
        return self.data['fields']['issuetype']['name']

    def get_summary(self):
        return self.data['fields']['summary']

    def get_due_date(self):
        return self.data['fields']['duedate']


class Api:
    def __init__(self) -> None:
        super().__init__()
        self.username = Config.JIRA_USERNAME
        self.password = Config.JIRA_PASSWORD
        self.host = Config.JIRA_HOST

    def search(self, jql: str) -> list:
        response = requests.get(
            '%s/rest/api/2/search' % self.host,
            params={'jql': jql, 'maxResults': 1000},
            auth=(self.username, self.password)
        )
        if not response.ok:
            return []

        result = []
        try:
            result = json.loads(response.text)['issues'].values()
        except Exception:
            pass

        return result