from flask import session


'''
{'Organization ': {'Organizational Structure Management': { 0: {'question_sentence': "Our company's organizational structure has sufficient capacity to support digital transformation projects.", 'weight': 0.04409100048181188, 'answer': None}, 
                                                            1: {'question_sentence': "Our company's governance approach encourages transforming internal behaviors and programs necessary for digital transformation.", 'weight': 0.18790487327149444, 'answer': None},
                                                            2: {'question_sentence': "Our company's governance approach brings people from different business units together using digital communication channels.", 'weight': 0.04087668048465908, 'answer': None},
                                                            3: {'question_sentence': "Our company...n activities to develop corporate methods.', 'weight': 0.12791235251573305, 'answer': None},
                                                            4: {'question_sentence': 'Our level of agility in change management is high.', 'weight': 0.08630853414475921, 'answer': None}}
'''

def score_calculator(question_dict):
    q = session["questions"]

    scores = {}
    for title in question_dict.keys():
        dim_score = 0.0
        scores[title] = {}
        for subdimension, all_questions in question_dict[title].items():
            subdim_score = 0.0
            scores[title][subdimension] = {}
            for i, res_dict in all_questions.items():
                subdim_score += res_dict["weight"] * res_dict["answer"]
            
            scores[title][subdimension]["score"] = subdim_score
            dim_score += subdim_score

        scores[title]["score"] = dim_score
    
    return scores