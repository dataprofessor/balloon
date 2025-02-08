import streamlit as st

# Define page functions
def player_scores():
    st.title("Player Scores Dashboard")
    
    # Assuming df is already loaded with your data
    # For demonstration, let's create sample data
    import pandas as pd
    df = pd.DataFrame({
        'player': ['Player1', 'Player2', 'Player3'],
        'total_score': [100, 75, 90]
    })
    
    max_score = df['total_score'].max()
    
    st.dataframe(
        df,
        column_config={
            "player": "Player",
            "total_score": st.column_config.ProgressColumn(
                "Total Score",
                help="Player's total score with visual progress bar",
                format="%d",
                min_value=0,
                max_value=max_score,
            )
        },
        hide_index=True
    )

def player_stats_1():
    st.title("Player Stats 1")
    st.write("This page is ready for your player statistics content!")

def player_stats_2():
    st.title("Player Stats 2")
    st.write("This page is ready for additional player statistics content!")

def home():
    st.title("Welcome to Player Analytics")
    
    st.markdown("""
    ## 📊 Player Analytics Dashboard

    Welcome to the Player Analytics Dashboard! Use the sidebar to navigate through different sections:

    - **Player Scores**: View detailed player scores with visual progress bars
    - **Player Stats 1**: First set of player statistics (coming soon)
    - **Player Stats 2**: Second set of player statistics (coming soon)
    """)

pg = st.navigation([
    st.Page(home, title="Home", icon=":material/home:", default=True),
    st.Page(player_scores, title="Player Scores", icon=":material/scoreboard:"),
    st.Page(player_stats_1, title="Player Stats 1", icon=":material/analytics:"),
    st.Page(player_stats_2, title="Player Stats 2", icon=":material/trending_up:")
])

# Run the selected page
pg.run()
