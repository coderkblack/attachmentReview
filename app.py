import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Internship Survey Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("/home/jakes/Documents/notebooks/practice/eac_questionnaire .csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

df = df.rename(columns={
    "Q1_valuable_experiences_group_work": "Group Work",
    "Q1_valuable_experiences_involved_in_meetings": "Involved in Meetings",
    "actual_experience_vs_initial_expectations": "Expectations",
    "Q1_valuable_experiences_discussions": "Involved in Discussions",
    "Q1_valuable_experiences_skills_developed": "Developed a skill",
    "Q1_valuable_experiences_working_with_experts": "Working with Experts",
})

st.title("📊 Internship/Attachment Survey Analysis")

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Valuable Experiences", 
    "Expectations vs Reality", 
    "Skills Developed", 
    "Challenges",
    "Feedback on Program",
    "Directorate Insights",
    "Future Plans",
    "Advice & Recommendation"
])

# --- Tab 1: Valuable Experiences ---
with tab1:
    st.header("Valuable Experiences (Q1)")
    q1_cols = [
        "Group Work",
        "Involved in Meetings",
        "Involved in Discussions",
        "Developed a skill",
        "Working with Experts"
    ]
    q1_summary = df[q1_cols].sum().reset_index()
    q1_summary.columns = ["Experience", "Count"]
    q1_summary["Percentage"] = (q1_summary["Count"] / len(df) * 100).round(1)

    fig = px.bar(
        q1_summary, x="Experience", y="Count", text="Percentage",
        color="Count", color_continuous_scale="Blues",
        title="Most Valuable Experiences"
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Analysis")
    st.markdown(f"""
    - The most common experience was **{q1_summary.iloc[q1_summary['Count'].idxmax(),0]}**.  
    - Around **{q1_summary['Percentage'].max()}%** of respondents selected it.  
    - Other experiences such as group work and discussions were also valued, but less frequent.  
    """)

# --- Tab 2: Expectations vs Reality ---
with tab2:
    st.header("Expectations vs Reality")
    exp_summary = df["Expectations"].value_counts().reset_index()
    exp_summary.columns = ["Expectation", "Count"]

    fig = px.pie(exp_summary, names="Expectation", values="Count", color="Expectation", title="Experience vs Expectations")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        - Most respondents rated their experience as **Above Expectations**.  
        - Very few reported "Met Expectations".  
        - None reported "Below Expectations", suggesting overall high satisfaction.  
        """)

    # Cross Analysis
    df = df.rename(columns={
    "new_skills_developed_critical_thinking": "Critical Thinking",
    "new_skills_developed_Administrative_skills": "Administrative Skills",
    "new_skills_developed_professional_communication": "Professional Communication",
    "new_skills_developed_research_and_analysis": "Research and Analysis",
    "new_skills_developed_IT_literacy": "IT skills"
})

    skills_cols = [
        "Critical Thinking",
        "Administrative Skills",
        "Professional Communication",
        "Research and Analysis",
        "IT skills"
    ]

    df["skills_count"] = df[skills_cols].sum(axis=1)
    skills_by_expectation = df.groupby("Expectations")["skills_count"].mean().reset_index()

    fig = px.bar(
        skills_by_expectation, x="Expectations", y="skills_count",
        text="skills_count", color="skills_count", color_continuous_scale="Purples",
        title="Average Skills Developed by Expectation Level"
    )
    fig.update_traces(textposition="outside")
    with col2:
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        - Respondents with **Above Expectations** generally reported developing more skills.  
        - Suggests a positive link between overall satisfaction and perceived skill growth.  
        """)

# --- Tab 3: Skills Developed ---
with tab3:
    st.header("Skills Developed")

    skills_summary = df[skills_cols].sum().reset_index()
    skills_summary.columns = ["Skill", "Count"]
    skills_summary["Percentage"] = (skills_summary["Count"] / len(df) * 100).round(1)

    fig = px.bar(
        skills_summary, x="Count", y="Skill", text="Percentage",
        orientation="h", color="Count", color_continuous_scale="Greens",
        title="What New Skills Were Developed During Attachment"
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    # st.subheader("Analysis")
    # st.markdown("""
    # - Critical thinking, communication, and teamwork appear as top skills.  
    # - A smaller percentage developed IT literacy.  
    # - This suggests the program emphasizes professional and analytical skills.  
    # """)

    competency_cols = [col for col in df.columns if "Q3_professional_competencies" in col]
    competency_counts = df[competency_cols].sum().reset_index()
    competency_counts.columns = ["Competency", "Count"]
    competency_counts["Competency"] = competency_counts["Competency"].str.replace("Q3_professional_competencies_", "").str.replace("_", " ").str.title()

    fig_competencies = px.bar(
        competency_counts,
        x="Count",
        y="Competency",
        orientation="h",
        title="Professional Competencies Most Confident In Now",
        text="Count"
    )
    fig_competencies.update_traces(textposition="outside")

    st.plotly_chart(fig_competencies, use_container_width=True)

    dev_cols = [col for col in df.columns if "Q3_areas_develop_further" in col]
    dev_counts = df[dev_cols].sum().reset_index()
    dev_counts.columns = ["Area", "Count"]
    dev_counts["Area"] = dev_counts["Area"].str.replace("Q3_areas_develop_further_", "").str.replace("_", " ").str.title()

    fig_development = px.pie(
        dev_counts,
        names="Area",
        values="Count",
        hole=0.5,
        title="Areas for Further Development"
    )
    fig_development.update_traces(textinfo="percent+label")

    st.plotly_chart(fig_development, use_container_width=True)



# --- Tab 4: Challenges ---
with tab4:
    # st.write("""
    # This Sankey diagram shows how challenges encountered by respondents 
    # are connected to the strategies they used to overcome them.  
    # The thickness of each flow represents how many respondents gave that pairing.
    # """)

    # # Drop NaN values
    # df_filtered = df[['challenges_encountered', 'overcome_challenges']].dropna()

    # # Build label list
    # all_labels = list(pd.concat([df_filtered['challenges_encountered'], 
    #                          df_filtered['overcome_challenges']]).unique())

    # label_to_index = {label: i for i, label in enumerate(all_labels)}

    # # Group by Challenge-Solution pairs
    # link_data = df_filtered.groupby(['challenges_encountered', 'overcome_challenges']).size().reset_index(name='count')

    # # Convert labels to indices
    # sources = link_data['challenges_encountered'].map(label_to_index)
    # targets = link_data['overcome_challenges'].map(label_to_index)
    # values = link_data['count']

    # # Sankey figure
    # fig = go.Figure(data=[go.Sankey(
    # node=dict(
    #     pad=20,
    #     thickness=20,
    #     line=dict(color="black", width=0.5),
    #     label=all_labels,
    #     color="lightblue"
    # ),
    # link=dict(
    #     source=sources,
    #     target=targets,
    #     value=values,
    #     color="rgba(0, 100, 200, 0.4)"
    # )
    # )])

    # fig.update_layout(title_text="Challenges → Solutions", font_size=14)

    # # Display in Streamlit
    # st.plotly_chart(fig, use_container_width=True)


    # Page title
    st.title("Challenges vs How They Were Overcome")

    st.write("""
    This treemap shows the main challenges encountered by respondents 
    and the strategies they used to overcome them.  
    """)

    # Drop NaN values
    df_filtered = df[['challenges_encountered', 'overcome_challenges']].dropna()

    # Build treemap
    fig = px.treemap(
    df_filtered,
    path=['challenges_encountered', 'overcome_challenges'],  # hierarchy
    title="Challenges and How They Were Overcome",
    width=900,
    height=600
    )

    #  Increase font size for labels
    fig.update_traces(textfont_size=18)   # default is ~12

    # Increase title and general font
    fig.update_layout(
    title_font_size=24,
    font=dict(size=16)   # affects axis labels, legends, etc.
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Key Insights:**
    - Common challenges included lack of payment, long commutes, and technical jargon.  
    - Most overcame challenges by seeking help or adapting routines.    
    """)

# --- Tab 5: Overall Feedback ---
with tab5:
    # Workplace Support Feedback
    st.header("Feedback on Program")
    support_cols = ["orientation_effective", "adequate_supervision_mentorship", "meaningful_tasks"]
    support_counts = df[support_cols].melt(var_name="Support_Area", value_name="Response")

    fig_support = px.histogram(
        support_counts,
        x="Support_Area",
        color="Response",
        barmode="group",
        title="Workplace Support Feedback"
    )

    st.plotly_chart(fig_support, use_container_width=True)

    # Suggested Aspects to Improve
    improve_cols = [col for col in df.columns if "Q4_aspects_to_improve" in col]
    improve_counts = df[improve_cols].sum().reset_index()
    improve_counts.columns = ["Improvement", "Count"]
    improve_counts["Improvement"] = improve_counts["Improvement"].str.replace("Q4_aspects_to_improve_", "").str.replace("_", " ").str.title()

    fig_improve = px.treemap(
        improve_counts,
        path=["Improvement"],
        values="Count",
        title="Suggested Aspects to Improve"
    )

    # Increase title and general font
    fig_improve.update_layout(
    title_font_size=24,
    font=dict(size=16)   # affects axis labels, legends, etc.
    )

    st.plotly_chart(fig_improve, use_container_width=True)


# --- Tab 6: Directorate Features ---
with tab6:
    st.header("Directorate Analysis")
    # 1. Directorate Strengths (count how many times each strength is selected)
    strengths_cols = [
        "Q1_directorate_strengths_clear_coordination",
        "Q1_directorate_strengths_timely_communication",
        "Q1_directorate_strengths_competent_leadership",
        "Q1_directorate_strengths_welcoming_and_accomodative",
        "Q1_directorate_strengths_division_of_labour"
    ]

    strength_counts = df[strengths_cols].sum().reset_index()
    strength_counts.columns = ["Strength", "Count"]
    strength_counts["Strength"] = strength_counts["Strength"].str.replace("Q1_directorate_strengths_", "").str.replace("_", " ").str.title()

    fig_strengths = px.bar(
        strength_counts,
        x="Count",
        y="Strength",
        orientation="h",
        title="Directorate Strengths"
    )
    fig_strengths.update_traces(text=strength_counts["Count"], textposition="outside")

    # 2. Improvement Suggestions (Yes/No)
    fig_improvement = px.pie(
        df,
        names="directorate_process_improve_suggestion",
        hole=0.5,
        title="Are there any Processes You would Suggest Reviewing or Improving?"
    )
    fig_improvement.update_traces(textinfo="percent+label")

    # 3. Satisfaction with Directorate Mandate
    satisfaction_counts = df["directorate_address_mandate"].value_counts().reset_index()
    satisfaction_counts.columns = ["Satisfaction", "Count"]

    fig_satisfaction = px.bar(
        satisfaction_counts,
        x="Satisfaction",
        y="Count",
        text="Count",
        title="Satisfaction with Directorate Addressing Mandate Regarding EAC Affairs"
    )
    fig_satisfaction.update_traces(textposition="outside")

    # Display side by side in Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_strengths, use_container_width=True)
    with col2:
        st.plotly_chart(fig_improvement, use_container_width=True)

    st.plotly_chart(fig_satisfaction, use_container_width=True)

# --- Tab 6: Career Development ---
with tab7:
    st.header("Career Prospects")

    # 1. Career Influence (Pie)
    # Count yes vs no
    counts = {
        "Yes": df["Q1_future_career_influence_further_studies"].sum(),
        "No": len(df) - df["Q1_future_career_influence_further_studies"].sum()
    }


    col1, col2 = st.columns(2)
    with col1:
        # Create donut chart
        fig_donut = px.pie(
            names=list(counts.keys()),
            values=list(counts.values()),
            hole=0.5,  # <--- makes it a donut
            title="Did The Attachment Influence Your Career Plans Or Academic Focus?"
        )

        # Improve style
        fig_donut.update_traces(textinfo="percent+label", pull=[0.05, 0])  # highlight "Yes"
        fig_donut.update_layout(showlegend=True)

        st.plotly_chart(fig_donut, use_container_width=True)

    # 2. Future Opportunities Interest (Pie)
    fig_future = px.pie(
        df,
        names="future_opportunities_interest",
        title="Interested in Future Opportunities Working With EAC?"
    )
    with col2:
        st.plotly_chart(fig_future, use_container_width=False)

# 3. Knowledge Application Areas (Bar Chart)
    knowledge_cols = [
        "Q3_future_knowledge_apply_improve_communication",
        "Q3_future_knowledge_apply_work_with_different_agencies",
        "Q3_future_knowledge_apply_academic_work"
    ]

    knowledge_counts = df[knowledge_cols].sum().reset_index()
    knowledge_counts.columns = ["Area", "Count"]

    # Clean names for display
    knowledge_counts["Area"] = knowledge_counts["Area"].str.replace("Q3_future_knowledge_apply_", "").str.replace("_", " ").str.title()

    fig_knowledge = px.bar(
        knowledge_counts,
        x="Area",
        y="Count",
        title="Planned Areas of Knowledge Application",
        text="Count"
    )
    fig_knowledge.update_traces(textposition="outside")

    # Streamlit Display

    st.subheader("Knowledge Application")
    st.plotly_chart(fig_knowledge, use_container_width=False)

# --- Tab 7: Advice incoming ---
with tab8:
    st.header("Advice for incoming attachees")
    
    # 1. Recommend Others (Pie)
    fig_recommend = px.pie(
        df,
        names="recommend_others",
        title="Would You Recommend Others To Join?"
    )

    # 2. Reasons for Recommendation (Bar Chart)
    reason_cols = [
        "why_recommend_others_coducive_work_environment",
        "why_recommend_others_realtime_experience",
        "why_recommend_others_coducive_encouraging_officers",
        "why_recommend_others_insightful_moments"
    ]

    reason_counts = df[reason_cols].sum().reset_index()
    reason_counts.columns = ["Reason", "Count"]

    # Clean names for display
    reason_counts["Reason"] = reason_counts["Reason"].str.replace("why_recommend_others_", "").str.replace("_", " ").str.title()

    fig_reasons = px.bar(
        reason_counts,
        x="Reason",
        y="Count",
        title="Reasons for Recommending",
        text="Count"
    )   
    fig_reasons.update_traces(textposition="outside")

    # Streamlit Display
    st.plotly_chart(fig_recommend, use_container_width=True)

    st.plotly_chart(fig_reasons, use_container_width=False)

    
    # 1. Data Preparation
    # Original advice mapped to themes
    data = {
        "Advice": [
            "Actively ask questions",
            "Be open and curious to learn about EAC",
            "Take the initiative to engage the supervisors",
            "Enjoy the experience",
            "Be patient",
            "Be good in communication",
            "Network with others",
            "Be disciplined",
            "Be respectful",
            "Be willing to learn",
            "Be confident",
            "Be committed",
            "Don't be afraid to ask for help",
            "Be good time managers",
            "Explore other departments",
            "Ask for assignments",
            "Researching and making use of the library",
            "Stay professional",
        ],
        "Theme": [
            "Curiosity & Learning",
            "Curiosity & Learning",
            "Initiative & Engagement",
            "Confidence & Attitude",
            "Confidence & Attitude",
            "Communication & Networking",
            "Communication & Networking",
            "Professionalism & Discipline",
            "Professionalism & Discipline",
            "Curiosity & Learning",
            "Confidence & Attitude",
            "Professionalism & Discipline",
            "Curiosity & Learning",
            "Time Management",
            "Initiative & Engagement",
            "Initiative & Engagement",
            "Curiosity & Learning",
            "Professionalism & Discipline"
        ]
    }

    df2 = pd.DataFrame(data)

    # Sankey Diagram

    # Encode nodes
    all_nodes = list(df2['Theme'].unique()) + list(df2['Advice'].unique())
    node_indices = {node: i for i, node in enumerate(all_nodes)}

    # Build links
    links = df2.apply(
        lambda row: dict(
            source=node_indices[row['Theme']],
            target=node_indices[row['Advice']],
            value=1
        ), axis=1
    ).tolist()

    # Sankey
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=40,
            thickness=25,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color="lightblue",
            hovertemplate='%{label}<extra></extra>'
        ),
        link=dict(
            source=[l['source'] for l in links],
            target=[l['target'] for l in links],
            value=[l['value'] for l in links],
            color="rgba(150,150,150,0.6)",
     )
    )])

    fig_sankey.update_layout(
        title_text="What Advice Would You give to incoming attachment students?", 
        font=dict(size=15),
        width=950,
        height=800,
        margin=dict(l=20,r=20, t=50, b=20)
        )

    # Display in Streamlit
    col1, col2, col3 = st.columns([1,3,1])

    st.plotly_chart(fig_sankey, use_container_width=True)

    st.markdown(
        """
        Advice for incoming interns centers around being open to learning, time management, and networking.
        """
    )
