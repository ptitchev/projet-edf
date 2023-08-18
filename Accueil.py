import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_helper.tools import init_data 

#st.session_state

pd_matchs, pd_players, pd_matchs_players, pd_matchs_players_score, pd_matchs_players_noScore = init_data()

def store():
    filter = ""
    if not ('years' not in st.session_state) :
        if st.session_state['years'] != (1926, 2023):
            st.session_state['years'] = st.session_state['years']
            filter += "Année >= " + str(st.session_state['years'][0]) + " & Année <= " + str(st.session_state['years'][1])
        else :
            del st.session_state['years']
    if not ('tm' not in st.session_state) :
        if st.session_state['tm'] != []:        
            st.session_state['tm'] = st.session_state['tm']
            if len(filter) > 0 :
                filter += ' & '
            for type in st.session_state['tm']:
                if type != st.session_state['tm'][0]:
                    filter += ' & '
                filter += "Genre == '" + type + "'"
        else :
            del st.session_state['tm']
    if not ('adv' not in st.session_state) :
        if st.session_state['adv'] != []:        
            st.session_state['adv'] = st.session_state['adv']
            if len(filter) > 0 :
                filter += ' & '
            for advs in st.session_state['adv']:
                if advs != st.session_state['adv'][0]:
                    filter += ' & '
                filter += "Adversaire == '" + advs + "'"
        else :
            del st.session_state['adv']
    if not ('place' not in st.session_state) :
        if st.session_state['place'] != []:        
            st.session_state['place'] = st.session_state['place']
            if len(filter) > 0 :
                filter += ' & '
            for places in st.session_state['place']:
                if places != st.session_state['place'][0]:
                    filter += ' & '
                filter += "Lieu == '" + places + "'"
        else :
            del st.session_state['place']
        
    st.write((filter))
    [filter]
    st.write(len(filter))
    if len(filter)>0:
        L = list(pd_matchs.query(filter)["index"])
        id_filter = "id_match in ("
        for id in L :
            id_filter += "'"+id+"', "
        id_filter += ")"
        L_jr = list(pd_matchs_players.query(id_filter).Nom.unique())
    else :
        L_jr =  list(pd_players.JOUEUR.values)
            
    
    rch = st.selectbox("Recherche", options = [''] + L_jr, help="Cherchez un joueur de l'équipe de France de Basket")#, placeholder = "Chercher un joueur")
    return rch

def reset_filter():
    if not ('years' not in st.session_state) :
        del st.session_state['years']
    if not ('tm' not in st.session_state) :
        del st.session_state['tm']
    if not ('adv' not in st.session_state) :
        del st.session_state['adv']
    if not ('place' not in st.session_state) :
        del st.session_state['place']

    
    

rch = store()

rch_adv = st.expander("Recherche avancée")
with rch_adv:

    RA_c1, RA_c2 = st.columns([1,2])
    with RA_c1 :
        type = st.radio('Type de la recherche :', ['Année', 'Type de match', 'Adversaire',"Lieu"], help="Utilisez ce menu pour filtrer la liste des joueurs", disabled=False)

        

    with RA_c2 :

        if type == 'Année' :
            years = st.slider('Année :',
                              pd_matchs.Date.dt.year.unique().tolist()[0], 
                              pd_matchs.Date.dt.year.unique().tolist()[-1], 
                              value=(pd_matchs.Date.dt.year.unique().tolist()[0],pd_matchs.Date.dt.year.unique().tolist()[-1]),
                              key="years")
            
        if type == "Type de match" :
            adv = st.multiselect(
                'Type de match',
                 pd_matchs.Genre.unique(),
                [], key = "tm")

        if type == "Adversaire" :
            adv = st.multiselect(
                'Adversaire',
                 pd_matchs.Adversaire.unique(),
                [], key = "adv")
            
        if type == "Lieu" :
            adv = st.multiselect(
                'Lieu',
                 pd_matchs.Lieu.unique(),
                [], key = "place")
            
        
    RAB_c1, RAB_c2 = st.columns([1,2])

    with RAB_c2 :
        RAC_c1, RAC_c2, RAC_c3, RAC_c4 = st.columns(4)

        if not ('years' not in st.session_state) :
            if st.session_state['years'] != (1926, 2023):
                with RAC_c1:
                    st.write('Année :',st.session_state["years"])
        if not ('tm' not in st.session_state) :
            if st.session_state['tm'] != []:
                with RAC_c2:
                    st.write("Type :", st.session_state["tm"])
        if not ('adv' not in st.session_state) :
            if st.session_state['adv'] != []:
                with RAC_c3:
                    st.write('Adversaire :', st.session_state["adv"])
        if not ('place' not in st.session_state) :
            if st.session_state['place'] != []:
                with RAC_c4:
                    st.write('Lieu :', st.session_state["place"])

    with RAB_c1 :
        st.write('')
        st.write('')
        st.button('Effacer les filtres', on_click=reset_filter)






viz = st.container()

with viz :

    if rch :
        sel = rch
        p = pd_players.query("JOUEUR == '"+sel+"'")
        mp = pd_matchs_players.query("Nom == '"+sel+"'")  #mp_i = mp.id_match
        mp = pd.merge(mp, pd_matchs, left_on = ['id_match'], right_on = ['index'], how="left").copy()
        r_mp = pd_matchs_players_score.query("Nom == '"+sel+"'")#r_mp_i = r_mp.id_match
        r_mp = pd.merge(r_mp, pd_matchs, left_on = ['id_match'], right_on = ['index'], how="left").copy()
        #m = pd_matchs.loc[mp['index']]
        #r_m = pd_matchs.loc[r_mp['index']]

        ss = r_mp.Victoire.count()
        pts = p.POINTS
        win = r_mp.query('Victoire == True').Victoire.count()
        max = r_mp.Points.max()
        wmoy = round(100 * win / ss, 1)
        pmoy = round(pts / ss, 1)


        C1, C2 = st.columns(2)

        with C2 : 
            c1, c2 = st.columns(2)
            with c1 :
                st.metric('Matchs joués', ss)
                st.metric('Matchs gagnés', win)
                st.metric('% Victoire', wmoy)
            with c2 :
                st.metric('Points marqués', pts)
                st.metric('Meilleure performance', max)
                st.metric('Moyenne points', pmoy)

        fig = px.bar(r_mp, x='Année', y="Points", color='Genre')
        st.plotly_chart(fig)

        match_details = st.expander('Détail matchs')
        with match_details :
            st.write(mp[["Infos",'Genre','Adversaire', 'Victoire', "Score vainqueur", "Score perdant", "Points", 'Club']])


        #st.scatter()
        #st.write(pd_players.query("JOUEUR == '"+joueur+"'"))
        #pd_rch = pd.merge(pd_matchs_players.query("Nom == '"+sel+"'"), pd_matchs.loc[mp_i], left_on = ['id_match'], right_on = ['Index']).copy()

        #st.write(pd_rch[["Infos",'Genre','Adversaire', 'Victoire', "Score vainqueur", "Score perdant", "Points", 'Club']])
        #st.bar_chart(r_mp,x = 'Année',y = "Points")
        
