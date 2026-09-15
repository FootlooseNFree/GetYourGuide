# Import Libraries
import pandas as pd
import streamlit as st

# Set Streamlit Page Configuration
st.set_page_config(
    page_title = 'GetYourGuide Case Study',
    page_icon = '🔁',
    layout = 'wide',
    initial_sidebar_state = 'locked'
)

# Define colors
brand_color = '#ff5532'
brand_color_secondary = '#020226'
white_color = '#ffffff'

# Set title and description
st.markdown('# :color[GetYourGuide Case Study]{foreground="#ff5532" background="#ffffff"}',
            text_alignment="center", wrap=True)
st.markdown('#### :color[LQA, Human-in-the-loop and LLM-as-Judge Implementation]{foreground="#020226" background="#ffffff"}',
            text_alignment="center", wrap=True)


# Load data for streamlit
@st.cache_data
def load_data():
    github_data_url = 'https://raw.githubusercontent.com/FootlooseNFree/GetYourGuide/refs/heads/main/GetYourGuide_CaseStudy_Gemini_Evaluated.csv'
    df = pd.read_csv(github_data_url)
    return df

df = load_data()

st.divider()

# Calculate Metrics
total_titles = len(df)
human_score_column = 'human_clickability_score'
model_score_column = 'model_clickability_score'
human_localization_column = 'human_localization'
model_localization_column = 'model_localization'

exact_matches = (df[human_score_column] == df[model_score_column]).sum()
match_rate = (exact_matches / total_titles) * 100
discrepancy_count = total_titles - exact_matches

exact_title_match = (df[human_localization_column] == df[model_localization_column]).sum()

# Sidebar checkbox for metrics Overview
checkbox_metrics = st.checkbox(':color[Click to show metrics overview]{foreground="#020226"}', False)
st.divider()

if checkbox_metrics:
    # Metrics
    st.markdown('###### :color[Dataset & Agreement Overview]{foreground="#ffffff" background="#020226"}')

    # Metrics columns
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown('**Evaluated Activity Titles**<br><br>',
                    unsafe_allow_html=True)
        st.metric(
            label='',
            value=total_titles,
            help='Total number of activity titles in the case study dataset'
        )

    with m2:
        st.markdown('**Exact Score Matches <br> (Clickability: Human v/s Model)**',
                    unsafe_allow_html=True)
        st.metric(
            label='',
            value=f'{exact_matches} / {total_titles}',
            delta=f'{match_rate:.2f}% Match Rate',
            delta_color='normal'
        )

    with m3:
        st.markdown('**Discrepancy (Human v/s Model)<br>Clickability Score**',
                    unsafe_allow_html=True)
        st.metric(
            label='',
            value=discrepancy_count,
            delta=f'{(discrepancy_count / total_titles)*100:.2f}% deviation',
            delta_color='inverse'
        )

    with m4:
        st.markdown('**Exact Localization Matches<br>(Human v/s Model)**',
                    unsafe_allow_html=True)
        st.metric(
            label='',
            value=exact_title_match,
            help='Total instances where model localized titles matches exactly with human localized titles'
        )

    st.divider()

# Human v/s Model Comparison for each dimension
st.markdown('##### :color[Human v/s Model Comparison]{foreground="#ffffff" background="#020226"}')
st.markdown('**:color[Select Activity (en)]{foreground=#ff5532}**')
activity = st.selectbox(':color[Select Activity Title]{foreground="#ff5532"}',
            options=df['text_en'].unique(),
            label_visibility='collapsed',
            width=600)

# Display German MT title
activity_de = df[df['text_en'] == activity]['text_de'].iloc[0]
st.markdown(f'**:color[German Title (de) - ]{{foreground="#ff5532"}}:color[ {activity_de}]{{foreground="#020226"}}**')

# Rename df columns for readability
df_renamed = df.rename(columns={
                'human_evaluation_error_categories':'Error Categories (Human)',
                'model_evaluation_error_categories':'Error Categories (Model)',
                'human_clickability_score':'Clickability Score (Human)',
                'model_clickability_score':'Clickability Score (Model)',
                'human_localization':'Localized Title (Human)',
                'model_localization':'Localized Title (Model)',
                'human_reasoning':'Reasoning (Human)',
                'model_reasoning':'Reasoning (Model)'
                })

# Display comparison DataFrame
df_error_cat = df_renamed[df_renamed['text_en'] == activity][['Error Categories (Human)','Error Categories (Model)']]
df_click_score = df_renamed[df['text_en'] == activity][['Clickability Score (Human)','Clickability Score (Model)']]

# Display rewrite and reasoning
rewrite_human = df_renamed[df['text_en'] == activity]['Localized Title (Human)'].iloc[0]
rewrite_model = df_renamed[df['text_en'] == activity]['Localized Title (Model)'].iloc[0]
reasoning_human = df_renamed[df['text_en'] == activity]['Reasoning (Human)'].iloc[0]
reasoning_model = df_renamed[df['text_en'] == activity]['Reasoning (Model)'].iloc[0]

# Display ratings
st.dataframe(df_error_cat, hide_index=True, width=500)
st.dataframe(df_click_score, hide_index=True, width=500)

# Display rewrite
st.markdown(f':color[Title rewrite suggestion (Human) - ]{{foreground="#ff5532"}}:color[ {rewrite_human}]{{foreground="#020226"}}')
st.markdown(f':color[Title rewrite suggestion (Model) - ]{{foreground="#ff5532"}}:color[ {rewrite_model}]{{foreground="#020226"}}')

# Display reasoning
st.markdown(f':color[Reasoning (Human) - ]{{foreground="#ff5532"}} {reasoning_human}')
st.markdown(f':color[Reasoning (Model) - ]{{foreground="#ff5532"}}:color[ {reasoning_model}]{{foreground="#020226"}}')
