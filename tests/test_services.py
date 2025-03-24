""" Testing services of application"""
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import datetime

from src.services import filter_voting


class TestFilterVotings(unittest.TestCase):
  def test_filter_votings(self):

    VOTING_CSV = os.path.join(os.path.dirname( __file__ ), '..','outputs', 'pl_voting_clean.csv')
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
if __name__ == '__main__':
  unittest.main()