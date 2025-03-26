import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
import unittest
from src.repository import AppDatabase


class TestRepository(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app_database = AppDatabase()

    def test_attribute_clean_persons_x(self):
        self.assertEqual(self.app_database.clean_persons_genres,
                         ["f", "m"])
        self.assertEqual(self.app_database.clean_persons_parties,
                         ['Ind', 'LC', 'LJS', 'MCG', 'PLR', 'S', 'UDC', 'Ve'])

    def test_attribute_rubriques_rsge(self):
        self.assertEqual(self.app_database.rubriques_rsge,
                         ['Structure cantonale et principes fondamentaux', 
                          'Organisation du canton', 
                          'Instruction publique, culture', 
                          'Finances et contributions', 
                          'Droit civil et droit pénal, organisation judiciaire et procédure', 
                          'Police', 
                          'Militaire, protection civile et défense générale', 
                          'Transports et communications', 
                          'Commerce, industrie, arts et métiers, logement', 
                          'Législation\xa0sociale', 
                          'Santé', 
                          'Domaine public et travaux', 
                          'Agriculture, forêts, chasse et pêche'])

    def test_attribute_clean_voting(self):
        self.assertTrue(isinstance(self.app_database.clean_voting["voting_date"][0], datetime.date))

    def test_attributes_min_max_dates(self):
        self.assertEqual(self.app_database.min_date,datetime.datetime(2023, 5, 11, 21,58,00))
        self.assertEqual(self.app_database.max_date,datetime.datetime(2025, 2, 15, 20,2,00))

if __name__ == '__main__':
    unittest.main()
