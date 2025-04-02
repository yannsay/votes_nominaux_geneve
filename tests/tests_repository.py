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
        
        self.assertEqual(self.app_database.clean_persons_persons,
                         ['Adrien Genecand', 'Alberto Velasco', 'Alexandre de Senarclens', 'Alexis Barbey',
                          'Alia Chaker Mangeat', 'Amar Madani', 'Ana Roch', 'André Pfeffer',
                          'Angèle-Marie Habiyakare', 'Arber Jahija', 'Caroline Marti', 'Caroline Renold',
                          'Celine van Till', 'Charles Poncet', 'Charles Selleger', 'Christian Flury', 
                          'Christian Steiner', 'Christina Meissner', 'Christo Ivanov', 'Cyril Aellen', 
                          'Cyril Mizrahi', 'Cédric Jeanneret', 'Céline Bartolomucci', 'Céline Zuber-Roy',
                          'Daniel Noël', 'Daniel Sormanni', 'Danièle Magnin', 'Darius Azarpey',
                          'David Martin', 'Diane Barbier-Mueller', 'Diego Esteban', 'Dilara Bayrak',
                          'Djawed Sangdel', 'Emilie Fernandez', 'Fabienne Monbaron', 'Florian Dugerdil',
                          'Francine de Planta', 'Francisco Taboada', 'François Baertschi', 'François Erard',
                          'François Wolfisberg', 'Frédéric Saenger', 'Gabriela Sonderegger',
                          'Gabrielle Le Goff', 'Geoffray Sirolli', 'Grégoire Carasso', 'Guy Mettan',
                          'Jacklean Kalibala', 'Jacques Blondin', 'Jacques Béné', 'Jacques Jeannerat',
                          'Jean-Charles Rielle', 'Jean-Louis Fazio', 'Jean-Marc Guinchard',
                          'Jean-Marie Voumard', 'Jean-Pierre Pasquier', 'Jean-Pierre Tombola',
                          'Jennifer Conti', 'Joëlle Fiss', 'Julien Nicolet-dit-Félix', 'Julien Ramu',
                          'Lara Atassi', 'Laura Mach', 'Laurent Seydoux', 'Leonard Ferati',
                          'Lionel Dugerdil', 'Louise Trottet', 'Léna Strasser', 'Léo Peterschmitt',
                          'Marc Falquet', 'Marc Saudan', 'Marjorie de Chastonay', 'Masha Alimi',
                          'Matthieu Jotterand', 'Mauro Poggia', 'Michael Andersen', 'Monika Ducret',
                          'Murat-Julian Alder', 'Natacha Buffet-Desfayes', 'Nicole Valiquer Grecuccio',
                          'Oriana Brücker', 'Pascal Uehlinger', 'Patricia Bidaux', 'Patrick Dimier',
                          'Patrick Lussi', 'Philippe Meyer', 'Philippe Morel', 'Philippe de Rougemont',
                          'Pierre Conne', 'Pierre Eckert', 'Pierre Maudet', 'Pierre Nicollier',
                          'Raphaël Dunand', 'Roger Golay', 'Romain de Sainte Marie', 'Rémy Burri',
                          'Sami Gashi', 'Sandro Pistis', 'Sebastian Aeschbach', 'Skender Salihi',
                          'Sophie Bobillier', 'Sophie Demaurex', 'Souheil Sayegh', 'Stefan Balaban',
                          'Stéphane Florey', 'Stéphane Fontaine', 'Sylvain Thévoz', 'Sébastien Desfayes',
                          'Thierry Arn', 'Thierry Cerutti', 'Thierry Oppikofer', 'Thomas Bruchez',
                          'Thomas Wenger', 'Uzma Khamis Vannini', 'Vincent Canonica', 'Vincent Subilia',
                          'Virna Conti', 'Véronique Kämpfen', 'Xavier Magnin', 'Xhevrie Osmani',
                          'Yvan Zweifel', 'Yves Magnin', 'Yves Nidegger', 'Yves de Matteis']
                        )

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
