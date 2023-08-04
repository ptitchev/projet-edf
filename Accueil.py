import pandas as pd
import streamlit as st

pd_matchs = pd.read_csv("./data/matchs.csv", index_col=0)
pd_players = pd.read_csv("./data/players.csv", index_col=0)
pd_matchs_players = pd.read_csv("./data/matchs_players.csv", index_col=0)
pd_matchs.Date = pd.to_datetime(pd_matchs.Date)#.dt.strftime("%d-%m-%Y")
#pd_matchs.dtypes #Nan si sans score --> remplacer par null ?
pd_matchs_players_score = pd_matchs_players.query("Points != 'NPJ' & Points != 'ND'").copy()
pd_matchs_players_score.Points = pd.to_numeric(pd_matchs_players_score.Points)
pd_matchs_players_noScore = pd_matchs_players.query("Points == 'NPJ' | Points == 'ND'").copy()

rch = st.selectbox("Recherche", options = [''] + list(pd_players.JOUEUR.values))

rch_adv = st.expander("Recherche avancée")
with rch_adv:
    type = st.radio('Type de la recherche :', ['Joueur', 'Compétition', 'Année'], disabled=True)

    # if type == 'Joueur':date = 

    rch2 = st.button("Rechercher")

#with st.expander('Affiner la recherche :'):
#    st.selectbox("Selection d'une année", options = pd_players.JOUEUR.values)



    sel = rch
    p = pd_players.query("JOUEUR == '"+sel+"'")
    mp = pd_matchs_players.query("Nom == '"+sel+"'")
    mp_i = mp.id_match
    r_mp = pd_matchs_players_score.query("Nom == '"+sel+"'")
    r_mp_i = r_mp.id_match
    m = pd_matchs.loc[mp_i]
    r_m = pd_matchs.loc[r_mp_i]

viz = st.container()

