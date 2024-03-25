from flask import render_template, request, session, request
import copy
import ahpy

from score_calculator import *
from model.questions_model import QuestionsClass



def pairwise_comp_page():
    if request.method == "GET":
        q = session["questions"]
        return render_template('pairwise_comp_page.html', pairs_with_titles=q.pairs_with_titles, high_crs=None, pair_values={})  # Passing an empty dictionary for pair_values initially

    elif request.method == "POST":
        value_mapping = {1: 1/9, 2: 1/8, 3: 1/7, 4: 1/6, 5: 1/5, 6: 1/4, 7: 1/3, 8: 1/2}
        pair_values = {}
        for key, value in request.form.items():
            if key.startswith('comp_'):
                dims = key.split("_")[1:]  # [dim1, dim2]
                if int(value) in value_mapping.keys():
                    pair_values[(dims[0], dims[1])] = value_mapping[int(value)]
                else:
                    pair_values[(dims[0], dims[1])] = int(value) - 8

        q = session["questions"]
        dim_compares = {}
        high_consistency_ratios = []
        for dim_name, subdims in zip(q.dim_list, q.subdim_list):
            subdim_pair_values = {}
            for pair, value in pair_values.items():
                if pair[0] in subdims:
                    subdim_pair_values[pair] = value

            subdim_comp_result = ahpy.Compare(name=dim_name, comparisons=subdim_pair_values, precision=3, random_index='saaty')
            dim_compares[dim_name] = subdim_comp_result

            if subdim_comp_result.consistency_ratio > 0.1:
                high_consistency_ratios.append(dim_name)

        if len(high_consistency_ratios) > 0:
            return render_template('pairwise_comp_page.html', pairs_with_titles=q.pairs_with_titles, high_crs=high_consistency_ratios, pair_values=request.form)
        else:
            return render_template('digital_report.html', score_dict={"0": pair_values, "1": dim_compares})



def question_page(url_id):
    if not "questions" in session:
        session["questions"] = QuestionsClass()

    q = session["questions"]

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
            return render_template('digital_report.html', score_dict=score_dict)
        else:
            return render_template('index.html')
    
    return render_template('question_page.html', data=q.questions[q.dim_list[q.current_dim_ind]], title=q.dim_list[q.current_dim_ind], url_id=url_id+1)


def main_page():
    session["questions"] = QuestionsClass()
    return render_template('index.html')


    
    

    