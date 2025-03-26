""" Testing services of application"""
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import datetime

from src.services import filter_voting, filter_votes, create_table_to_plot

VOTES_CSV = ('outputs/clean_votes.csv')
PERSON_CSV = ('outputs/clean_persons.csv')
VOTING_CSV = os.path.join(os.path.dirname( __file__ ), '..','outputs', 'pl_voting_clean.csv')


class TestFilterVotings(unittest.TestCase):
  def test_filter_votings(self):
    pl_voting_clean = pd.read_csv(VOTING_CSV)
    pl_voting_clean["voting_date"] = pd.to_datetime(pl_voting_clean["voting_date"])
    initial_dates= (datetime.date(2023, 5, 11), datetime.date(2025, 2, 28))
    self.assertEqual(filter_voting(voting_table =  pl_voting_clean,
                                   selected_rubriques = [], 
                                   selected_chapitre = [],
                                   selected_dates = initial_dates).shape,
                                   (82,18))
    self.assertEqual(filter_voting(voting_table =  pl_voting_clean,
                                   selected_rubriques = ["Police"],
                                   selected_chapitre = [],
                                   selected_dates = initial_dates).shape,
                                   (1,18))
    self.assertEqual(filter_voting(voting_table =  pl_voting_clean,
                                   selected_rubriques = ["Structure cantonale et principes fondamentaux"],
                                   selected_chapitre = [],
                                   selected_dates = initial_dates).shape,
                                   (8,18))
    self.assertEqual(filter_voting(voting_table =  pl_voting_clean,
                                   selected_rubriques = [], 
                                   selected_chapitre = [],
                                   selected_dates = (datetime.date(2023, 5, 11), datetime.date(2023, 5, 31))
                                   ).shape,
                                   (4,18))
    self.assertEqual(filter_voting(voting_table =  pl_voting_clean,
                                   selected_rubriques = ["Structure cantonale et principes fondamentaux"], 
                                   selected_chapitre = ["Constitution et principes généraux"],
                                   selected_dates = initial_dates
                                   ).shape,
                                   (6,18))    

 
class TestFilterVotes(unittest.TestCase):
  def test_filter_votes(self):
    votes_clean = pd.read_csv(VOTES_CSV)
    persons_clean = pd.read_csv(PERSON_CSV)  
    self.assertEqual(filter_votes(votes_table= votes_clean,
                                  persons_table=persons_clean,
                                  selected_parties=[],
                                  selected_genre=[]).shape,
                                  (35455, 7))
    self.assertEqual(filter_votes(votes_table= votes_clean,
                                  persons_table=persons_clean,
                                  selected_parties=["S"],
                                  selected_genre=[]).shape,
                                  (6326, 7))
    self.assertEqual(filter_votes(votes_table= votes_clean,
                                  persons_table=persons_clean,
                                  selected_parties=["S", "Ve"],
                                  selected_genre=[]).shape,
                                  (11944, 7))
    self.assertEqual(filter_votes(votes_table= votes_clean,
                                  persons_table=persons_clean,
                                  selected_parties=[],
                                  selected_genre=["f"]).shape,
                                  (11041, 7)) 

class TestCreateTableToPlot(unittest.TestCase):
  def test_create_table_to_plot(self):

    pl_voting_clean = pd.read_csv(VOTING_CSV)
    pl_voting_clean["voting_date"] = pd.to_datetime(pl_voting_clean["voting_date"])
    initial_dates= (datetime.date(2023, 5, 11), datetime.date(2025, 2, 28))
    votes_clean = pd.read_csv(VOTES_CSV)
    persons_clean = pd.read_csv(PERSON_CSV)

    filter_votings_test1 = filter_voting(pl_voting_clean,
                                       selected_rubriques=[],
                                       selected_chapitre=[],
                                       selected_dates=initial_dates)
    filter_votes_test1 = filter_votes(votes_table=votes_clean, 
                                      persons_table=persons_clean,
                                      selected_parties=[],
                                      selected_genre=[])
    self.assertEqual(create_table_to_plot(voting_table=filter_votings_test1,
                                          votes_table=filter_votes_test1).shape,
                                  (124, 83))
    
    filter_votings_test2 = filter_voting(pl_voting_clean,
                                       selected_rubriques=["Police"],
                                       selected_chapitre=[],
                                       selected_dates=initial_dates)
    filter_votes_test2 = filter_votes(votes_table=votes_clean, 
                                      persons_table=persons_clean,
                                      selected_parties=[],
                                      selected_genre=[])
    self.assertEqual(create_table_to_plot(voting_table=filter_votings_test2,
                                          votes_table=filter_votes_test2).shape,
                                  (85, 2))

    filter_votings_test3 = filter_voting(pl_voting_clean,
                                       selected_rubriques=[],
                                       selected_chapitre=[],
                                       selected_dates=initial_dates)
    filter_votes_test3 = filter_votes(votes_table=votes_clean, 
                                      persons_table=persons_clean,
                                      selected_parties=[],
                                      selected_genre=["f"])
    self.assertEqual(create_table_to_plot(voting_table=filter_votings_test3,
                                          votes_table=filter_votes_test3).shape,
                                  (37, 83))

    filter_votings_test4 = filter_voting(pl_voting_clean,
                                       selected_rubriques=["Structure cantonale et principes fondamentaux"],
                                       selected_chapitre=[],
                                       selected_dates=initial_dates)
    filter_votes_test4 = filter_votes(votes_table=votes_clean, 
                                      persons_table=persons_clean,
                                      selected_parties=["S"],
                                      selected_genre=[])
    self.assertEqual(create_table_to_plot(voting_table=filter_votings_test4,
                                          votes_table=filter_votes_test4).shape,
                                  (20, 9))

if __name__ == '__main__':
  unittest.main()