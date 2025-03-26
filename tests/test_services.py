""" Testing services of application"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import filter_voting, filter_votes, create_table_to_plot, create_info_table
import datetime
import unittest
import pandas as pd


VOTES_CSV = ('outputs/clean_votes.csv')
PERSON_CSV = ('outputs/clean_persons.csv')
VOTING_CSV = os.path.join(os.path.dirname(
    __file__), '..', 'outputs', 'pl_voting_clean.csv')


class TestServices(unittest.TestCase):
    def setUp(self):
        self.pl_voting_clean = pd.read_csv(VOTING_CSV)
        self.pl_voting_clean["voting_date"] = pd.to_datetime(
            self.pl_voting_clean["voting_date"])
        self.initial_dates = (datetime.date(2023, 5, 11),
                              datetime.date(2025, 2, 28))
        self.votes_clean = pd.read_csv(VOTES_CSV)
        self.persons_clean = pd.read_csv(PERSON_CSV)

    def test_filter_votings(self):
        """
        Test function filter_voting
        """
        self.assertEqual(filter_voting(voting_table=self.pl_voting_clean,
                                       selected_rubriques=[],
                                       selected_chapitre=[],
                                       selected_dates=self.initial_dates).shape,
                         (82, 18))
        self.assertEqual(filter_voting(voting_table=self.pl_voting_clean,
                                       selected_rubriques=["Police"],
                                       selected_chapitre=[],
                                       selected_dates=self.initial_dates).shape,
                         (1, 18))
        self.assertEqual(filter_voting(voting_table=self.pl_voting_clean,
                                       selected_rubriques=[
                                           "Structure cantonale et principes fondamentaux"],
                                       selected_chapitre=[],
                                       selected_dates=self.initial_dates).shape,
                         (8, 18))
        self.assertEqual(filter_voting(voting_table=self.pl_voting_clean,
                                       selected_rubriques=[],
                                       selected_chapitre=[],
                                       selected_dates=(datetime.date(
                                           2023, 5, 11), datetime.date(2023, 5, 31))
                                       ).shape,
                         (4, 18))
        self.assertEqual(filter_voting(voting_table=self.pl_voting_clean,
                                       selected_rubriques=[
                                           "Structure cantonale et principes fondamentaux"],
                                       selected_chapitre=[
                                           "Constitution et principes généraux"],
                                       selected_dates=self.initial_dates
                                       ).shape,
                         (6, 18))

    def test_filter_votes(self):
        """
        Test function filter_votes
        """
        self.assertEqual(filter_votes(votes_table=self.votes_clean,
                                      persons_table=self.persons_clean,
                                      selected_parties=[],
                                      selected_genre=[]).shape,
                         (35455, 7))
        self.assertEqual(filter_votes(votes_table=self.votes_clean,
                                      persons_table=self.persons_clean,
                                      selected_parties=["S"],
                                      selected_genre=[]).shape,
                         (6326, 7))
        self.assertEqual(filter_votes(votes_table=self.votes_clean,
                                      persons_table=self.persons_clean,
                                      selected_parties=["S", "Ve"],
                                      selected_genre=[]).shape,
                         (11944, 7))
        self.assertEqual(filter_votes(votes_table=self.votes_clean,
                                      persons_table=self.persons_clean,
                                      selected_parties=[],
                                      selected_genre=["f"]).shape,
                         (11041, 7))

    def test_create_table_to_plot(self):
        """
        Test function create_table_to_plot
        """
        filter_votings_test1 = filter_voting(self.pl_voting_clean,
                                             selected_rubriques=[],
                                             selected_chapitre=[],
                                             selected_dates=self.initial_dates)
        filter_votes_test1 = filter_votes(votes_table=self.votes_clean,
                                          persons_table=self.persons_clean,
                                          selected_parties=[],
                                          selected_genre=[])
        self.assertEqual(create_table_to_plot(voting_table=filter_votings_test1,
                                              votes_table=filter_votes_test1).shape,
                         (124, 83))

        filter_votings_test2 = filter_voting(self.pl_voting_clean,
                                             selected_rubriques=["Police"],
                                             selected_chapitre=[],
                                             selected_dates=self.initial_dates)
        filter_votes_test2 = filter_votes(votes_table=self.votes_clean,
                                          persons_table=self.persons_clean,
                                          selected_parties=[],
                                          selected_genre=[])
        self.assertEqual(create_table_to_plot(voting_table=filter_votings_test2,
                                              votes_table=filter_votes_test2).shape,
                         (85, 2))

        filter_votings_test3 = filter_voting(self.pl_voting_clean,
                                             selected_rubriques=[],
                                             selected_chapitre=[],
                                             selected_dates=self.initial_dates)
        filter_votes_test3 = filter_votes(votes_table=self.votes_clean,
                                          persons_table=self.persons_clean,
                                          selected_parties=[],
                                          selected_genre=["f"])
        self.assertEqual(create_table_to_plot(voting_table=filter_votings_test3,
                                              votes_table=filter_votes_test3).shape,
                         (37, 83))

        filter_votings_test4 = filter_voting(self.pl_voting_clean,
                                             selected_rubriques=[
                                                 "Structure cantonale et principes fondamentaux"],
                                             selected_chapitre=[],
                                             selected_dates=self.initial_dates)
        filter_votes_test4 = filter_votes(votes_table=self.votes_clean,
                                          persons_table=self.persons_clean,
                                          selected_parties=["S"],
                                          selected_genre=[])
        self.assertEqual(create_table_to_plot(voting_table=filter_votings_test4,
                                              votes_table=filter_votes_test4).shape,
                         (20, 9))
        
    def test_create_info_table(self):
        """
        Test function create_info_table
        """
        filter_votings_test1 = filter_voting(self.pl_voting_clean,
                                             selected_rubriques=[],
                                             selected_chapitre=[],
                                             selected_dates=self.initial_dates)
        filter_votes_test1 = filter_votes(votes_table=self.votes_clean,
                                          persons_table=self.persons_clean,
                                          selected_parties=[],
                                          selected_genre=[])
        data_to_plot_test1 = create_table_to_plot(voting_table=filter_votings_test1,
                                              votes_table=filter_votes_test1)
        self.assertEqual(create_info_table(voting_table = self.pl_voting_clean, 
                                           data_to_plot = data_to_plot_test1).shape,
                         (82, 13))

        filter_votings_test2 = filter_voting(self.pl_voting_clean,
                                             selected_rubriques=["Santé"],
                                             selected_chapitre=[],
                                             selected_dates=self.initial_dates)
        filter_votes_test2 = filter_votes(votes_table=self.votes_clean,
                                          persons_table=self.persons_clean,
                                          selected_parties=[],
                                          selected_genre=[])
        data_to_plot_test2 = create_table_to_plot(voting_table=filter_votings_test2,
                                              votes_table=filter_votes_test2)
        self.assertEqual(create_info_table(voting_table = self.pl_voting_clean, 
                                           data_to_plot = data_to_plot_test2).shape,
                         (3, 13))

        filter_votings_test2 = filter_voting(self.pl_voting_clean,
                                             selected_rubriques=["Organisation du canton"],
                                             selected_chapitre=["Pouvoirs législatif et exécutif"],
                                             selected_dates=self.initial_dates)
        filter_votes_test2 = filter_votes(votes_table=self.votes_clean,
                                          persons_table=self.persons_clean,
                                          selected_parties=[],
                                          selected_genre=[])
        data_to_plot_test2 = create_table_to_plot(voting_table=filter_votings_test2,
                                              votes_table=filter_votes_test2)
        self.assertEqual(create_info_table(voting_table = self.pl_voting_clean, 
                                           data_to_plot = data_to_plot_test2).shape,
                         (6, 13))

        filter_votings_test2 = filter_voting(self.pl_voting_clean,
                                             selected_rubriques=[],
                                             selected_chapitre=[],
                                             selected_dates=(datetime.date(2023, 5, 11), datetime.date(2023, 5, 31)))
        filter_votes_test2 = filter_votes(votes_table=self.votes_clean,
                                          persons_table=self.persons_clean,
                                          selected_parties=[],
                                          selected_genre=[])
        data_to_plot_test2 = create_table_to_plot(voting_table=filter_votings_test2,
                                              votes_table=filter_votes_test2)
        self.assertEqual(create_info_table(voting_table = self.pl_voting_clean, 
                                           data_to_plot = data_to_plot_test2).shape,
                         (4, 13))

if __name__ == '__main__':
    unittest.main()
