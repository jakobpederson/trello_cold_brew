import logging
import logging.config
from unittest import TestCase

from cold_brew.cold_brew import TrelloColdBrew
from cold_brew.trello_helper import TrelloHelper
from cold_brew.tests.tokens import API_KEY, TOKEN
from cold_brew.tests.members import TEST_MEMBER_IDS


class ColdBrewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        logging.config.dictConfig({"version": 1, "loggers": {"requests": {"level": "INFO"}}})

    def setUp(self):
        self.helper = TrelloHelper(API_KEY, TOKEN)
        self.sut = TrelloColdBrew(API_KEY, TOKEN)
        self.test_org = self.helper.create_organization('ORGTEST')

    def tearDown(self):
        for organization in self.helper.list_organizations():
            if organization.name.lower().startswith('orgtest'):
                self.helper.delete_organization(organization.id)

    def test_create_organization(self):
        self.assertTrue(self.test_org.name.lower().startswith('orgtest'))

    def test_add_workers_organizations_adds_workers(self):
        members = self.test_org.get_members()
        self.assertEqual(len(members), 1)
        self.assertEqual(len(TEST_MEMBER_IDS), 1)
        self.sut.add_workers_to_organization(self.test_org, member_ids=TEST_MEMBER_IDS)
        members = self.test_org.get_members()
        self.assertEqual(len(members), 2)

    def test_remove_workers_from_organization_removes_workers(self):
        self.sut.add_workers_to_organization(self.test_org)
        members = self.test_org.get_members()
        self.assertEqual(len(members), 2)
        self.sut.remove_workers_from_organization(self.test_org)
        members = self.test_org.get_members()
        self.assertEqual(len(members), 1)
