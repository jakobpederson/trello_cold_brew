from trello import TrelloClient


class TrelloHelper():

    def __init__(self, api_key, token):
        self.client = TrelloClient(api_key=api_key, token=token)

    def create_organization(self, organization_name):
        post_args = {'displayName': organization_name}
        obj = self.client.fetch_json(
            '/organizations',
            http_method='POST',
            post_args=post_args
        )
        return self.client.get_organization(obj['id'])

    def delete_organization(self, organization_id):
        self.client.fetch_json(
            '/organizations/{}'.format(organization_id),
            http_method='DELETE',
        )

    def list_organizations(self):
        return self.client.list_organizations()
