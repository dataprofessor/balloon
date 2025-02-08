import streamlit as st
import pandas as pd
import numpy as np

# Define page functions
def leaderboard():
    st.title("Leaderboard")
    
    try:
        # Read the CSV file
        df = pd.read_csv("data/game_events.leaderboard.csv", index_col=False)
        df
        
        # Convert numeric columns to Python native types
        df = df.astype({'total_score': int})
        max_score = int(df['total_score'].max())
        
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
    except FileNotFoundError:
        st.error("Could not find data/game_events.leaderboard.csv. Please ensure the file exists in the correct location.")
    except Exception as e:
        st.error(f"An error occurred while reading the leaderboard data: {str(e)}")

def player_stats_1():
    st.title("Player Stats 1")
    st.write("This page is ready for your player statistics content!")

def player_stats_2():
    st.title("Player Stats 2")
    st.write("This page is ready for additional player statistics content!")

def home():
    st.title("Welcome to Player Analytics")
    
    st.markdown("""
    ## Player Analytics Dashboard

    Welcome to the Player Analytics Dashboard! Use the sidebar to navigate through different sections:

    - **Leaderboard**: View player rankings and scores
    - **Player Stats 1**: First set of player statistics (coming soon)
    - **Player Stats 2**: Second set of player statistics (coming soon)
    """)

# Configure the pages with Material icons
pg = st.navigation([
    st.Page(home, title="Home", icon=":material/home:", default=True),
    st.Page(leaderboard, title="Leaderboard", icon=":material/leaderboard:"),
    st.Page(player_stats_1, title="Player Stats 1", icon=":material/analytics:"),
    st.Page(player_stats_2, title="Player Stats 2", icon=":material/trending_up:")
])

# Run the selected page
pg.run()
