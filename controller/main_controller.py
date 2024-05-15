from flask import render_template, request, session, request
from io import BytesIO
import matplotlib
import pandas as pd
import base64
import copy
import ahpy

from utils import *
from model.questions_model import QuestionsClass
from utils import make_spider, get_texts_by_scores


def pairwise_comp_page():
    if request.method == "GET":
        q = session["questions"]
        return render_template('pairwise_comp_page.html', subdim_pairs_with_titles=q.pairs_with_titles, dim_pairs=q.dim_pairs, subdim_high_crs=None, dim_high_crs=None, pair_values={})

    elif request.method == "POST":
        q = session["questions"]
        value_mapping = {
            1: 9,
            2: 8,
            3: 7, 
            4: 6,
            5: 5,
            6: 4,
            7: 3,
            8: 2,
            9: 1,
            10: 1/2,
            11: 1/3,
            12: 1/4,
            13: 1/5,
            14: 1/6,
            15: 1/7,
            16: 1/8,
            17: 1/9,
        }
        pair_values = {}
        for key, value in request.form.items():
            if key.startswith('comp_') or key.startswith('priority_'):
                dims = key.split("_")[1:]
                pair_values[(dims[0], dims[1])] = value_mapping[int(value)]

        # subdimension pairwise comparison
        dim_compares = {}
        subdim_high_consistency_ratios = []
        for dim_name, subdims in zip(q.dim_list, q.subdim_list):
            subdim_pair_values = {}
            for pair, value in pair_values.items():
                if pair[0] in subdims:
                    subdim_pair_values[pair] = value

            subdim_comp_result = ahpy.Compare(name=dim_name, comparisons=subdim_pair_values, precision=3, random_index='saaty')
            dim_compares[dim_name] = subdim_comp_result

            if subdim_comp_result.consistency_ratio > 0.1:
                subdim_high_consistency_ratios.append(dim_name)

        # dimension pairwise comparison
        dim_high_consistency_ratios = None
        dim_pair_values = {}
        for pair, value in pair_values.items():
            if pair[0] in q.dim_list:
                dim_pair_values[pair] = value
        
        dim_comp_result = ahpy.Compare(name="dimension", comparisons=dim_pair_values, precision=3, random_index='saaty')
        if dim_comp_result.consistency_ratio > 0.1:
            dim_high_consistency_ratios = 1

        # rendering
        if len(subdim_high_consistency_ratios) > 0 or dim_high_consistency_ratios != None:
            return render_template('pairwise_comp_page.html', subdim_pairs_with_titles=q.pairs_with_titles, dim_pairs=q.dim_pairs, subdim_high_crs=subdim_high_consistency_ratios, dim_high_crs=dim_high_consistency_ratios, pair_values=request.form)
        else:
            if not "questions" in session:
                session["questions"] = QuestionsClass()

            q = session["questions"]
            q.update_weights_from_compares(dim_compares)
            q.update_dim_weights_from_compares(dim_comp_result)
            
            session["questions"] = q

            return render_template('index.html')



def question_page(url_id):
    if not "questions" in session:
        session["questions"] = QuestionsClass()

    q = session["questions"]
    if q.subdim_weights == {}:
        return render_template('question_page.html', data=q.questions[q.dim_list[q.current_dim_ind]], title=q.dim_list[q.current_dim_ind], url_id=url_id+1, is_pairwise_done=False)

    q.current_dim_ind = int(url_id)
    
    if request.method == "POST":
        if q.current_dim_ind > 0 and q.current_dim_ind <= len(q.dim_list):
            title = q.dim_list[q.current_dim_ind-1]
            q.completed_dimensions.add(title)
            for subdimension, all_questions in q.questions[title].items():
                for i, _ in enumerate(all_questions, start=1):
                    q.questions[title][subdimension][i-1]["answer"] = int(request.form.get(f"{subdimension}_{i}"))

    if q.current_dim_ind == len(q.dim_list):
        if len(q.completed_dimensions) == q.current_dim_ind:
            score_dict = score_calculator(copy.deepcopy(q.questions))
            q.scores = score_dict
        
            df_scores = pd.DataFrame({
                'group': ['Digital Awareness'],
            })
            for dim in q.dim_list:
                df_scores[dim] = q.scores[dim]["score"] * 25
        
            img_tag = radar_chart_tag(df_scores)
            groups, texts = get_texts_by_scores(score_dict)
            
            dim_weights = q.dim_weights
            subdim_weights = q.subdim_weights

            overall_score = 0
            for dim, weight in dim_weights.items():
                overall_score += weight * score_dict[dim]['score']
            
            overall_level = get_group_by_score(overall_score)
            
            return render_template('digital_report.html', img_tag=img_tag, score_dict=score_dict, groups=groups, texts=texts, dim_weights=dim_weights, subdim_weights=subdim_weights, overall_score=overall_score, overall_level=overall_level)
        
        else:
            return render_template('index.html')
    
    return render_template('question_page.html', data=q.questions[q.dim_list[q.current_dim_ind]], title=q.dim_list[q.current_dim_ind], url_id=url_id+1, is_pairwise_done=True)



def radar_chart_tag(df):
    my_palette = matplotlib.colormaps["Set2"]

    plt = make_spider(df, row=0, title="", color=my_palette(0))
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    img_base64 = base64.b64encode(img.getvalue()).decode()
    img_tag = f'<img src="data:image/png;base64,{img_base64}">'
    plt.close()

    return img_tag


def main_page():
    session["questions"] = QuestionsClass()
    return render_template('index.html')