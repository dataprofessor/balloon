import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def leaderboard():
    st.title("Leaderboard")
    
    try:
        # Load and process color trend data for total score and bonus hits
        color_trend = pd.read_csv("data/game_events.player_color_trend.csv", index_col=False)
        color_trend = color_trend.drop('Unnamed: 0', axis=1)
        color_trend = color_trend.astype({
            'score_in_window': int,
            'bonus_hits': int,
            'pop_count': int
        })
        
        # Calculate total score per player
        total_scores = color_trend.groupby('player')['score_in_window'].sum().reset_index()
        total_scores = total_scores.rename(columns={'score_in_window': 'total_score'})
        total_scores = total_scores.sort_values('total_score', ascending=False)
        
        # Calculate total bonus hits per player
        bonus_hits = color_trend.groupby('player')['bonus_hits'].sum().reset_index()
        bonus_hits = bonus_hits.sort_values('bonus_hits', ascending=False)
        
        # Create two columns for the leaderboards
        col1, col2 = st.columns(2)
        
        # Display main leaderboard in first column
        with col1:
            st.header("Overall Score")
            st.dataframe(
                total_scores,
                column_config={
                    "player": "Player",
                    "total_score": st.column_config.ProgressColumn(
                        "Total Score",
                        help="Player's total score with visual progress bar",
                        format="%d",
                        min_value=0,
                        max_value=int(total_scores['total_score'].max()),
                    )
                },
                hide_index=True
            )
        
        # Display bonus hits leaderboard in second column
        with col2:
            st.header("Bonus Performance")
            st.dataframe(
                bonus_hits,
                column_config={
                    "player": "Player",
                    "bonus_hits": st.column_config.ProgressColumn(
                        "Bonus Hits",
                        help="Number of bonus hits achieved",
                        format="%d",
                        min_value=0,
                        max_value=int(bonus_hits['bonus_hits'].max()),
                    )
                },
                hide_index=True
            )
    except Exception as e:
        st.error(f"Error loading leaderboard: {str(e)}")

def color_analysis():
    st.title("Color Analysis")
    
    try:
        # Load color trend data
        color_trend = pd.read_csv("data/game_events.player_color_trend.csv", index_col=False)
        color_trend = color_trend.drop('Unnamed: 0', axis=1)
        
        # Convert numeric columns to Python native types
        color_trend = color_trend.astype({
            'pop_count': int,
            'score_in_window': int,
            'bonus_hits': int
        })
        
        # Create color distribution from color_trend data
        color_dist = color_trend.groupby(['player', 'balloon_color'])['pop_count'].sum().reset_index()
        color_dist = color_dist.rename(columns={'pop_count': 'hits'})
        
        # Color Distribution Section
        st.header("Balloon Color Distribution")

        # Calculate high-level metrics
        total_pops = color_dist['hits'].sum()
        most_common_color = color_dist.groupby('balloon_color')['hits'].sum().idxmax()
        least_common_color = color_dist.groupby('balloon_color')['hits'].sum().idxmin()
        unique_colors = len(color_dist['balloon_color'].unique())

        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Balloon Pops", f"{total_pops:,}")
        with col2:
            st.metric("Most Popular Color", most_common_color)
        with col3:
            st.metric("Least Popular Color", least_common_color)
        with col4:
            st.metric("Unique Colors", unique_colors)

        # Simple heatmap with adjusted height
        heatmap = alt.Chart(color_dist).mark_rect().encode(
            x='balloon_color:N',
            y='player:N',
            color='hits:Q',
            tooltip=['player', 'balloon_color', 'hits']
        ).properties(
            title='Balloon Color Distribution by Player',
            height=500
        )

        # Display the chart
        st.altair_chart(heatmap, use_container_width=True)
        
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
        # Load and preprocess color trend data
        color_trend = pd.read_csv("data/game_events.player_color_trend.csv", index_col=False)
        color_trend = color_trend.drop('Unnamed: 0', axis=1)
        
        # Convert numeric columns to Python native types
        color_trend = color_trend.astype({
            'pop_count': int,
            'score_in_window': int,
            'bonus_hits': int
        })
        
        # Aggregate data by player and time window
        pop_trend = color_trend.groupby(['player', 'window_start', 'window_end']).agg({
            'pop_count': 'sum',
            'score_in_window': 'sum'
        }).reset_index()
        
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

# Set page configuration
st.set_page_config(
    page_title="Player Analytics",
    page_icon=":bar_chart:",
    layout="wide"
)

# Configure the pages with Material icons
pg = st.navigation([
    st.Page(home, title="Home", icon=":material/home:", default=True),
    st.Page(leaderboard, title="Leaderboard", icon=":material/leaderboard:"),
    st.Page(color_analysis, title="Color Analysis", icon=":material/palette:"),
    st.Page(performance_trends, title="Performance Trends", icon=":material/trending_up:")
])

# Run the selected page
pg.run()
