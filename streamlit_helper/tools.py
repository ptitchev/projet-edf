import pandas as pd
import streamlit as st

def init_data():
    pd_matchs = pd.read_csv("./data/matchs.csv", index_col=0)
    pd_matchs.reset_index(inplace = True)
    pd_players = pd.read_csv("./data/players.csv", index_col=0)
    pd_players.reset_index(inplace = True)
    pd_matchs_players = pd.read_csv("./data/matchs_players.csv", index_col=0)
    pd_matchs.Date = pd.to_datetime(pd_matchs.Date)#.dt.strftime("%d-%m-%Y")
    #pd_matchs.dtypes #Nan si sans score --> remplacer par null ?adv = None        years = None
    pd_matchs["Année"] = pd_matchs.Date.dt.year

    pd_matchs_players_score = pd_matchs_players.query("Points != 'NPJ' & Points != 'ND'").copy()
    pd_matchs_players_score.Points = pd.to_numeric(pd_matchs_players_score.Points)
    pd_matchs_players_noScore = pd_matchs_players.query("Points == 'NPJ' | Points == 'ND'").copy()
    return pd_matchs, pd_players, pd_matchs_players, pd_matchs_players_score, pd_matchs_players_noScore