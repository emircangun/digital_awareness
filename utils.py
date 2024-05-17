from flask import session
import matplotlib.pyplot as plt
from math import pi

from suggestions import limits, suggestions
 
 
def make_spider(df, row, title, color):

    # number of variable
    categories=list(df)[1:]
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    my_dpi=96
    plt.figure(figsize=(1000/my_dpi, 1000/my_dpi), dpi=my_dpi)
    ax = plt.subplot(1,1,row+1, polar=True, )

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=15)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100"], color="grey", size=10)
    plt.ylim(0, 100)

    # Ind1
    values=df.loc[row].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
    ax.fill(angles, values, color=color, alpha=0.4)

    # Add a title
    plt.title(title, size=11, color=color, y=1.1)
    return plt



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

'''
{
    "Organization": {
        "Organizational Structure Management": {
            "score": 0.8300000000000001
        },
        "Organizational Change Management": {
            "score": 0.664
        },
        "Sustainable Learning Management": {
            "score": 0.498
        },
        "score": 1.9920000000000002
    },
    ...
}
'''

def get_group_by_score(score):
    for _, limit_dict in limits.items():
        if score >= limit_dict["Bottom"] and score <= limit_dict["Top"]:
            return limit_dict["Maturity Level"], limit_dict["Group"]

def get_texts_by_scores(score_dict):
    groups = {}
    texts = {}
    for dim, subdims in score_dict.items():
        groups[dim] = {}
        texts[dim] = {}
        
        dim_score = score_dict[dim]['score']
        
        for subdim, _ in subdims.items():
            if subdim != "score":
                level, group = get_group_by_score(dim_score)
                groups[dim][subdim] = f"{level} {group}"
            
                title_of_suggestion = None
                if level == "Level-1":
                    title_of_suggestion = "initiating to emerging"
                elif level == "Level-2":
                    title_of_suggestion = "emerging to performing"
                elif level == "Level-3":
                    title_of_suggestion = "performing to advancing"
                elif level == "Level-4":
                    title_of_suggestion = "advancing to leading"
                elif level == "Level-5":
                    title_of_suggestion = "leading"

                if level != "Level-5":
                    text_dict = suggestions[dim.lower().strip()][subdim.lower()][title_of_suggestion]
                else:
                    text_dict = {
                        "recommendation": suggestions[dim.lower().strip()][subdim.lower()][title_of_suggestion],
                        "actionable steps": suggestions[dim.lower().strip()][subdim.lower()][title_of_suggestion]
                    }
                    
                texts[dim][subdim] = text_dict
                
    return groups, texts
