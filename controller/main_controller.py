from flask import render_template, request

from score_calculator import *
from model.questions_model import q



def pairwise_comp_page():
    if request.method == "GET":
        return render_template('pairwise_comp_page.html', pairs=q.pairs)

    elif request.method == "POST":
        pair_values = {}
        for key, value in request.form.items():
            if key.startswith('pair_'):
                pair_values[key] = value

        return render_template('digital_report.html', score_dict=pair_values)


def question_page(url_id):
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
            score_dict = score_calculator(q.questions)
            return render_template('digital_report.html', score_dict=score_dict)
        else:
            return render_template('index.html')
    
    return render_template('question_page.html', data=q.questions[q.dim_list[q.current_dim_ind]], title=q.dim_list[q.current_dim_ind], url_id=url_id+1)


def main_page():
    if request.method == "GET":
        return render_template('index.html')
        

    
    

    