import pandas as pd
import os
from itertools import combinations

'''
{'Organization ': {'Organizational Structure Management': { 0: {'question_sentence': "Our company's organizational structure has sufficient capacity to support digital transformation projects.", 'weight': 0.04409100048181188, 'answer': None}, 
                                                            1: {'question_sentence': "Our company's governance approach encourages transforming internal behaviors and programs necessary for digital transformation.", 'weight': 0.18790487327149444, 'answer': None},
                                                            2: {'question_sentence': "Our company's governance approach brings people from different business units together using digital communication channels.", 'weight': 0.04087668048465908, 'answer': None},
                                                            3: {'question_sentence': "Our company...n activities to develop corporate methods.', 'weight': 0.12791235251573305, 'answer': None},
                                                            4: {'question_sentence': 'Our level of agility in change management is high.', 'weight': 0.08630853414475921, 'answer': None}}
'''

class QuestionsClass():
    def __init__(self):
        self.questions = self.get_questions()
        self.dim_list = list(self.questions.keys())
        self.current_dim_ind = -1
        self.completed_dimensions = set()
        
        self.subdim_list = []
        for dim in self.dim_list:
            self.subdim_list.append(list(self.questions[dim].keys()))

        self.pairs_with_titles = {}
        for dim_name, dim_pairs in zip(self.dim_list, self.subdim_list):
            self.pairs_with_titles[dim_name] = list(combinations(dim_pairs, 2))
        
        self.scores = {}

    def get_questions(self):
        # take also weights and make them {"answer": , "weight":}
        q_df = pd.read_excel(os.path.join(os.getcwd(), "data", "dims-coefficients.xlsx"))

        question_dict = {}
        for dim_name in q_df['Dimension'].unique():
            subdims = q_df[q_df['Dimension'] == dim_name]["Sub-dimension"].unique()

            _question_dict = {}
            for subdim in subdims:
                subdim_questions = list(q_df[(q_df['Dimension'] == dim_name) & (q_df['Sub-dimension'] == subdim)]["Question"])
                # _question_dict[subdim] = subdim_questions
                _question_dict[subdim] = {}
                for i, question_sentence in enumerate(subdim_questions):
                    weight = q_df[q_df['Question'] == question_sentence]["Coefficient"].iloc[0]
                    _question_dict[subdim][i] = {"question_sentence": question_sentence, "weight": weight, "answer": None}
            
            question_dict[dim_name] = _question_dict

        return question_dict
    
    def clear(self):
        self.questions = self.get_questions()
        self.current_dim_ind = -1
        self.completed_dimensions = set()