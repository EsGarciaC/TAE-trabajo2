import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_scores():
    scores_test = pd.read_pickle("DataFramesYutiles/puntajesTest.pkl")
    score_train = pd.read_pickle("DataFramesYutiles/puntajesTrain.pkl")

    scores = score_train.append(scores_test)
    scores.columns = ["scores"]

    return scores
scores = load_scores()

def calcular_percentil(puntaje):

    cantidad_puntajes_debajo = len(scores[(scores["scores"] <= puntaje)])

    percentil = (cantidad_puntajes_debajo/len(scores["scores"])) * 100

    return int(percentil)

def load_scorecard():
    scorecard = pd.read_pickle("DataFramesYutiles/scorecard.pkl")
    return scorecard

def input_toCreditScore(grade, home_ownership, verification_status, purpose, term,
                  int_rate, annual_inc, dti, inq_last_6mths, revol_util, out_prncp,
                  total_pymnt, total_rec_int, total_rev_hi_lim, mths_since_earliest_cr_line,
                  mths_since_issue_d, mths_since_last_credit_pull_d):

    df_scorecard = load_scorecard()


    nombre_columnas = ("grade", "home_ownership", "verification_status", "purpose", "term",
                  "int_rate", "annual_inc", "dti", "inq_last_6mths", "revol_util", "out_prncp",
                  "total_pymnt", "total_rec_int", "total_rev_hi_lim", "mths_since_earliest_cr_line",
                  "mths_since_issue_d", "mths_since_last_credit_pull_d")
    valores_columnas = (grade, home_ownership, verification_status, purpose, term,
                  int_rate, annual_inc, dti, inq_last_6mths, revol_util, out_prncp,
                  total_pymnt, total_rec_int, total_rev_hi_lim, mths_since_earliest_cr_line,
                  mths_since_issue_d, mths_since_last_credit_pull_d)
    

    column_value_dict = dict.fromkeys(df_scorecard["Feature name"].values, 0)

    for nombre, bin in zip(nombre_columnas, valores_columnas):
        column_value_dict[nombre + ":" + bin] += 1
    column_value_dict["Intercept"] += 1


    column_value_dict = {k:[v] for k,v in column_value_dict.items()}
    matriz_mult = pd.DataFrame.from_dict(column_value_dict)


    scorecard_scores_array = df_scorecard["Score - Final"].values
    scorecard_scores = scorecard_scores_array.reshape(102, 1)


    credit_score = matriz_mult.dot(scorecard_scores)

    return round(credit_score[0][0])

def create_score_pie_chart(explode):

    y = np.array([len(scores[scores['scores'] < 460]), 
                  len(scores[(scores["scores"] >= 460) & (scores["scores"] < 517)]), 
                  len(scores[(scores["scores"] >= 517) & (scores["scores"] < 584)]),
                  len(scores[(scores["scores"] >= 584) & (scores["scores"] < 630)]), 
                  len(scores[scores["scores"] >= 630])])
    
   

    labels = ["<460 Pobre", "460-516 Regular", "517-583 Bueno", "584-629 Muy bueno", ">=630 excelente"]
    fig, ax = plt.subplots()
    ax.pie(y, labels = labels, explode=explode, autopct='%1.1f%%', shadow=True)

    return fig








