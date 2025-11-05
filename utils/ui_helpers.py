import streamlit as st

def render_intro_text():
    st.markdown("""
    Ez az alkalmazás segít **elemezni az edzésnaplódat** és vizualizálni a fejlődésedet.  
    Töltsd fel a saját edzésnaplódat `.csv` formátumban, vagy próbáld ki a **demo adatokat**!

    ---

    ### 🏋️ Mit tud az alkalmazás?
    - 📈 **Trendek** megjelenítése: súly, ismétlésszám, edzésgyakoriság időben  
    - 🏆 **Top gyakorlatok** statisztikái (legtöbbet végzett, legnagyobb súly, stb.)  
    - 🔥 **Heatmap** az edzések intenzitásáról  
    - 🎯 **Célok és kihívások** követése  
    - 🌟 **Motivációs / Achievements** szekció – inspiráció a folytatáshoz  

    ---

    ### 📂 Hogyan használd?
    1. Töltsd fel az edzésnaplódat a lenti oszlopokkal `.csv` formátumban.  
    2. Vagy kattints a *„💾 Demo adat betöltése”* gombra, hogy kipróbáld a funkciókat.  
    3. A bal oldali menü segítségével navigálhatsz az egyes oldalak között.

    ---

    ### 📂 Kötelező CSV oszlopok
    A fájlodnak a következő oszlopokat **mindenképpen tartalmaznia kell**:
    
    - `start_time` – az edzés kezdete (dátum/óra formátumban)  
    - `end_time` – az edzés vége (dátum/óra formátumban)  
    - `exercise_name` – a gyakorlat neve  
    - `sets` – sorozatok száma  
    - `reps` – ismétlések száma  
    - `weight` – használt súly (kg)
    
    ---

    📍 **Ha tetszik a projekt, nézd meg a portfóliómat is**!  
    [🌐 Portfólió](https://jehunat.github.io/portfolio)
    """)

def render_restart_button():
    if st.session_state.get("workout_df") is not None:
        if st.button("🔄 Újrakezdés / adat törlése"):
            st.session_state.workout_df = None
            st.session_state.demo_mode = False
            st.rerun()