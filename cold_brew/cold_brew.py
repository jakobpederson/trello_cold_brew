from trello import TrelloClient

from cold_brew.members import MEMBER_IDS


class TrelloColdBrew():

    def __init__(self, api_key, token):
        self.client = TrelloClient(api_key=api_key, token=token)

    def add_workers_to_organization(self, organization, member_ids=None):
        result = []
        member_ids = MEMBER_IDS if not member_ids else member_ids
        for member_id in MEMBER_IDS:
            result.append(self._add_member(member_id, organization.id))
        return result

    def remove_workers_from_organization(self, organization):
        result = []
        for member_id in MEMBER_IDS:
            result.append(self._remove_member(member_id, organization.id))
        return result

    def _remove_member(self, member_id, organization_id):
        json_obj = self.client.fetch_json(
            '/organizations/{0}/members/{1}'.format(organization_id, member_id),
            http_method='DELETE',
            post_args={'idMember': member_id},
        )
        return json_obj

    def _add_member(self, member_id, organization_id):
        json_obj = self.client.fetch_json(
            '/organizations/{0}/members/{1}'.format(organization_id, member_id),
            http_method='PUT',
            post_args={'idMember': member_id, "type": "normal"},
        )
        return json_obj
