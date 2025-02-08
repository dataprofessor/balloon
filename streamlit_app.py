import streamlit as st
import pandas as pd
import numpy as np

def leaderboard():
    st.title("Leaderboard")
    
    try:
        df = pd.read_csv("data/game_events.leaderboard.csv", index_col=False)
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
    except Exception as e:
        st.error(f"Error loading leaderboard: {str(e)}")

def color_analysis():
    st.title("Color Analysis")
    
    try:
        # Load color distribution data
        color_dist = pd.read_csv("data/game_events.player_colored_pops.csv", index_col=False)
        color_trend = pd.read_csv("data/game_events.player_color_trend.csv", index_col=False)
        
        # Convert numeric columns to Python native types
        color_dist = color_dist.astype({'hits': int})
        color_trend = color_trend.astype({
            'pop_count': int,
            'score_in_window': int,
            'bonus_hits': int
        })
        
        # Color Distribution Section
        st.header("Balloon Color Distribution")
        
        # Create percentage distribution
        color_dist['percentage'] = color_dist.groupby('player')['hits'].transform(
            lambda x: (x / x.sum()) * 100
        ).astype(float)  # Convert to float
        
        # Display color distribution
        st.dataframe(
            color_dist,
            column_config={
                "player": "Player",
                "balloon_color": "Color",
                "hits": st.column_config.NumberColumn(
                    "Total Hits",
                    format="%d"
                ),
                "percentage": st.column_config.ProgressColumn(
                    "Distribution",
                    help="Percentage of hits by color",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                )
            },
            hide_index=True
        )
        
        # Color Trend Analysis
        st.header("Color Performance Over Time")
        
        # Convert time windows to datetime
        color_trend['window_start'] = pd.to_datetime(color_trend['window_start'])
        color_trend['window_end'] = pd.to_datetime(color_trend['window_end'])
        
        # Allow user to select a player
        players = sorted(color_trend['player'].unique())
        selected_player = st.selectbox("Select Player", players)
        
        # Filter data for selected player
        player_trend = color_trend[color_trend['player'] == selected_player]
        
        # Display trend metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Pops", int(player_trend['pop_count'].sum()))
        with col2:
            st.metric("Total Score", int(player_trend['score_in_window'].sum()))
        with col3:
            st.metric("Bonus Hits", int(player_trend['bonus_hits'].sum()))
            
    except Exception as e:
        st.error(f"Error loading color analysis: {str(e)}")

def performance_trends():
    st.title("Performance Trends")
    
    try:
        # Load performance data
        pop_trend = pd.read_csv("data/game_events.player_pop_trend.csv", index_col=False)
        bonus_pops = pd.read_csv("data/game_events.player_bonus_pops.csv", index_col=False)
        
        # Convert numeric columns to Python native types
        pop_trend = pop_trend.astype({
            'pop_count': int,
            'score_in_window': int
        })
        bonus_pops = bonus_pops.astype({'bonus_hits': int})
        
        # Overall Performance Metrics
        st.header("Bonus Performance")
        
        # Display bonus hits leaderboard
        st.dataframe(
            bonus_pops,
            column_config={
                "player": "Player",
                "bonus_hits": st.column_config.ProgressColumn(
                    "Bonus Hits",
                    help="Number of bonus hits achieved",
                    format="%d",
                    min_value=0,
                    max_value=int(bonus_pops['bonus_hits'].max()),
                )
            },
            hide_index=True
        )
        
        # Performance Trend Analysis
        st.header("Performance Over Time")
        
        # Convert time windows to datetime
        pop_trend['window_start'] = pd.to_datetime(pop_trend['window_start'])
        pop_trend['window_end'] = pd.to_datetime(pop_trend['window_end'])
        
        # Allow user to select a player
        players = sorted(pop_trend['player'].unique())
        selected_player = st.selectbox("Select Player", players)
        
        # Filter data for selected player
        player_trend = pop_trend[pop_trend['player'] == selected_player]
        
        # Display trend metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Pops", int(player_trend['pop_count'].sum()))
        with col2:
            st.metric("Total Score", int(player_trend['score_in_window'].sum()))
            
        # Calculate and display averages
        st.header("Average Performance")
        avg_stats = player_trend.agg({
            'pop_count': 'mean',
            'score_in_window': 'mean'
        }).round(2)
        
        st.write(f"Average pops per window: {float(avg_stats['pop_count'])}")
        st.write(f"Average score per window: {float(avg_stats['score_in_window'])}")
        
    except Exception as e:
        st.error(f"Error loading performance trends: {str(e)}")

def home():
    st.title("Welcome to Player Analytics")
    
    st.markdown("""
    ## Player Analytics Dashboard

    Welcome to the Player Analytics Dashboard! Use the sidebar to navigate through different sections:

    - **Leaderboard**: View player rankings and scores
    - **Color Analysis**: Analyze balloon color distributions and trends
    - **Performance Trends**: Track player performance and bonus achievements
    """)

# Configure the pages with Material icons
pg = st.navigation([
    st.Page(home, title="Home", icon=":material/home:", default=True),
    st.Page(leaderboard, title="Leaderboard", icon=":material/leaderboard:"),
    st.Page(color_analysis, title="Color Analysis", icon=":material/palette:"),
    st.Page(performance_trends, title="Performance Trends", icon=":material/trending_up:")
])

# Run the selected page
pg.run()
