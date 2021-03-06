from app.notify import NotifyMessage
from jira.Api import Api


class SingleStatusNotify(NotifyMessage):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.jql = kwargs['jql'] if 'jql' in kwargs else None

    @property
    def jql(self):
        return self._jql

    @jql.setter
    def jql(self, value):
        self._jql = value

    def _get_data(self):
        collection = Api().search(self.jql)

        unique_index = {}
        for item in collection.get_list():
            if item.assignee.ident is None:
                continue
            index = '_'.join([item.assignee.ident, item.status.ident])
            if unique_index.get(index) is None:
                unique_index[index] = [item]
            else:
                unique_index[index].append(item)
        return [val for val in unique_index.values() if len(val) > 1]

    def _get_template(self, data):
        template = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Нарушен принцип workflow: *в работе только одна задача на разработчика*"
                }
            }
        ]

        for issue_list in data:
            template.append({"type": "divider"})
            text = "*%s*\n\n" % issue_list[0].assignee.display_name
            for issue in issue_list:
                text += "• *<%s|%s>* %s in _%s_\n" % (
                    issue.url, issue.key,
                    issue.type, issue.status.name
                )
            template.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            })
        return template
