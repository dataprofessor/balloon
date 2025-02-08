import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Set page configuration - MUST BE FIRST ST COMMAND
st.set_page_config(
    page_title="Player Analytics",
    page_icon=":bar_chart:",
    layout="wide"
)

# Initialize session state to store data and settings
if 'color_trend_data' not in st.session_state:
    st.session_state.color_trend_data = None
if 'color_scheme' not in st.session_state:
    st.session_state.color_scheme = 'viridis'

# Settings in sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    # Color scheme selection
    color_schemes = [
        'viridis', 'magma', 'plasma', 'inferno',  # Sequential
        'blues', 'greens', 'oranges', 'reds',      # Single color
        'blueorange', 'brownbluegreen', 'purplegreen', 'pinkyellowgreen'  # Diverging
    ]
    st.session_state.color_scheme = st.selectbox(
        'Color Theme',
        options=color_schemes,
        index=color_schemes.index(st.session_state.color_scheme)
    )

@st.cache_data
def load_data():
    """Load and preprocess the color trend data."""
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
        
        # Convert time windows to datetime and extract hour
        color_trend['window_start'] = pd.to_datetime(color_trend['window_start'])
        color_trend['window_end'] = pd.to_datetime(color_trend['window_end'])
        color_trend['hour'] = color_trend['window_start'].dt.hour
        
        return color_trend
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def show_home():
    st.title("Welcome to Player Analytics")
    
    st.markdown("""
    ## Player Analytics Dashboard

    Welcome to the Player Analytics Dashboard! Use the sidebar to navigate through different sections:

    - **Leaderboard**: View player rankings and scores
    - **Color Analysis**: Analyze balloon color distributions and trends
    - **Performance Trends**: Track player performance and bonus achievements
    """)

def show_leaderboard():
    st.title("Leaderboard")
    
    if st.session_state.color_trend_data is not None:
        color_trend = st.session_state.color_trend_data
        
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

def show_color_analysis():
    st.title("Color Analysis")
    
    if st.session_state.color_trend_data is not None:
        color_trend = st.session_state.color_trend_data
        
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
            color=alt.Color('hits:Q', scale=alt.Scale(scheme=st.session_state.color_scheme)),
            tooltip=['player', 'balloon_color', 'hits']
        ).properties(
            title='Balloon Color Distribution by Player',
            height=500
        )

        # Display the chart
        st.altair_chart(heatmap, use_container_width=True)

def show_performance_trends():
    st.title("Balloon Activity Patterns")
    
    if st.session_state.color_trend_data is not None:
        color_trend = st.session_state.color_trend_data
        
        # Create player heatmap data
        player_hourly = color_trend.groupby(['player', 'hour'])['pop_count'].sum().reset_index()
        
        # Create color heatmap data
        color_hourly = color_trend.groupby(['balloon_color', 'hour'])['pop_count'].sum().reset_index()
        
        # Player Heatmap
        st.header("Player Activity by Hour")
        
        player_heatmap = alt.Chart(player_hourly).mark_rect().encode(
            x=alt.X('hour:O', title='Hour of Day'),
            y=alt.Y('player:N', title='Player'),
            color=alt.Color('pop_count:Q', 
                          title='Balloon Pops',
                          scale=alt.Scale(scheme=st.session_state.color_scheme)),
            tooltip=['player', 'hour', 'pop_count']
        ).properties(
            title='Balloon Pops by Player and Hour',
            height=400
        )
        
        st.altair_chart(player_heatmap, use_container_width=True)
        
        # Color Heatmap
        st.header("Balloon Colors by Hour")
        
        color_heatmap = alt.Chart(color_hourly).mark_rect().encode(
            x=alt.X('hour:O', title='Hour of Day'),
            y=alt.Y('balloon_color:N', title='Balloon Color'),
            color=alt.Color('pop_count:Q', 
                          title='Balloon Pops',
                          scale=alt.Scale(scheme=st.session_state.color_scheme)),
            tooltip=['balloon_color', 'hour', 'pop_count']
        ).properties(
            title='Balloon Pops by Color and Hour',
            height=300
        )
        
        st.altair_chart(color_heatmap, use_container_width=True)

# Load data once at startup
st.session_state.color_trend_data = load_data()

# Configure the pages with Material icons
pg = st.navigation([
    st.Page(show_home, title="Home", icon=":material/home:", default=True),
    st.Page(show_leaderboard, title="Leaderboard", icon=":material/leaderboard:"),
    st.Page(show_color_analysis, title="Color Analysis", icon=":material/palette:"),
    st.Page(show_performance_trends, title="Performance Trends", icon=":material/trending_up:")
])

# Run the selected page
pg.run()
