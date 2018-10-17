from trello import TrelloClient, exceptions

from cold_brew.members import MEMBER_IDS


class TrelloColdBrew():

    def __init__(self, api_key, token):
        self.client = TrelloClient(api_key=api_key, token=token)

    def add_workers_to_organization(self, organization, member_ids=None):
        member_ids = MEMBER_IDS if not member_ids else member_ids
        for member_id in member_ids:
            yield self.try_add_member(member_id, organization)

    def remove_workers_from_organization(self, organization, member_ids=None):
        member_ids = member_ids if member_ids else MEMBER_IDS
        for member_id in member_ids:
            yield self.try_remove_member(member_id, organization)

    def try_add_member(self, member_id, organization):
        try:
            return self._add_member(member_id, organization.id)
        except exceptions.ResourceUnavailable as e:
            if str(e).startswith('member not found at'):
                print('Trello member {} not found'.format(member_id))
            else:
                raise e

    def try_remove_member(self, member_id, organization):
        try:
            return self._remove_member(member_id, organization.id)
        except exceptions.Unauthorized:
            print('cannot remove member {}'.format(member_id))
            pass

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
