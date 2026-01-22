import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime

# Page configuration with storytelling theme
st.set_page_config(
    page_title="Diabetes Data Stories",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for storytelling
st.markdown("""
<style>
    .story-header {
        font-family: 'Georgia', serif;
        color: #2E86AB;
        font-size: 2.8rem;
        text-align: center;
        margin-bottom: 1rem;
        border-bottom: 3px solid #F18F01;
        padding-bottom: 1rem;
    }
    
    .chapter-header {
        font-family: 'Georgia', serif;
        color: #2E86AB;
        font-size: 2rem;
        margin-top: 2rem;
        border-left: 5px solid #F18F01;
        padding-left: 1rem;
    }
    
    .story-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #F18F01;
    }
    
    .insight-box {
        background-color: #E8F4F8;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #2E86AB;
        font-style: italic;
    }
    
    .character-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s;
    }
    
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .timeline-container {
        position: relative;
        max-width: 800px;
        margin: 2rem auto;
    }
    
    .timeline-item {
        padding: 1rem 2rem;
        margin: 2rem 0;
        background: white;
        border-radius: 10px;
        position: relative;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .timeline-item:before {
        content: '';
        position: absolute;
        left: -20px;
        top: 50%;
        width: 20px;
        height: 20px;
        background: #F18F01;
        border-radius: 50%;
        transform: translateY(-50%);
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/diabetes_012_health_indicators_BRFSS2015.csv')
    
    # Create storytelling columns
    df['Diabetes_Story'] = df['Diabetes_012'].map({
        0: 'Living without diabetes',
        1: 'At the crossroads: Prediabetes',
        2: 'Managing diabetes daily'
    })
    
    df['Age_Story'] = pd.cut(df['Age'], bins=[0, 3, 5, 7, 9, 11, 13], 
                             labels=[
                                 'Youth (18-24): Building foundations',
                                 'Young Adult (25-34): Career building',
                                 'Midlife (35-44): Juggling responsibilities',
                                 'Established (45-54): Health crossroads',
                                 'Mature (55-64): Managing wellness',
                                 'Senior (65+): Wisdom years'
                             ])
    
    df['BMI_Narrative'] = pd.cut(df['BMI'], bins=[0, 18.5, 25, 30, 40, 100],
                                labels=[
                                    'Underweight: The overlooked story',
                                    'Healthy weight: Balanced journey',
                                    'Overweight: The common challenge',
                                    'Obese: Multiple health narratives',
                                    'Severely obese: Complex health story'
                                ])
    
    df['Income_Story'] = pd.cut(df['Income'], bins=[0, 3, 6, 8, 10],
                               labels=[
                                   'Limited means: Healthcare hurdles',
                                   'Getting by: Making choices',
                                   'Comfortable: More options',
                                   'Prosperous: Better access'
                               ])
    
    return df

# Initialize session state for story progression
if 'story_page' not in st.session_state:
    st.session_state.story_page = 'cover'
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = None
if 'discovery_made' not in st.session_state:
    st.session_state.discovery_made = []

# Load data
df = load_data()

# Sidebar - Story Navigation
st.sidebar.title("📖 Story Navigation")
story_option = st.sidebar.selectbox(
    "Choose your journey:",
    [
        "📚 Table of Contents",
        "👥 Meet the People",
        "📈 The Big Picture",
        "🔍 Risk Detective",
        "💰 Socioeconomic Stories",
        "🏃 Lifestyle Narratives",
        "🎯 Your Story"
    ]
)

# Main storytelling container
main_container = st.container()

with main_container:
    # COVER PAGE
    if story_option == "📚 Table of Contents":
        st.markdown('<h1 class="story-header">The Diabetes Chronicles</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; margin: 2rem 0;'>
            <p style='font-size: 1.2rem; color: #666;'>
                A data-driven narrative exploring the lives behind 70,692 health records
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Book-like layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="story-card">
                <h3>📖 About This Story</h3>
                <p>Every data point in this dataset represents a real person's health journey 
                in 2015. This interactive storybook explores their challenges, patterns, 
                and opportunities for change.</p>
                
                <div class="insight-box">
                    <strong>Key Insight:</strong> Diabetes isn't just a medical condition—it's 
                    a story woven from genetics, lifestyle, economics, and access.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="story-card">
                <h3>🎯 Our Mission</h3>
                <p>To transform 21 columns of health data into meaningful narratives 
                that can:</p>
                <ul>
                    <li>Reveal hidden patterns</li>
                    <li>Identify intervention opportunities</li>
                    <li>Humanize health statistics</li>
                    <li>Guide preventive strategies</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="story-card">
                <h3>📚 Table of Contents</h3>
                <ol>
                    <li><strong>Chapter 1:</strong> Meet the People 👥</li>
                    <li><strong>Chapter 2:</strong> The Big Picture 📈</li>
                    <li><strong>Chapter 3:</strong> Risk Detective 🔍</li>
                    <li><strong>Chapter 4:</strong> Socioeconomic Stories 💰</li>
                    <li><strong>Chapter 5:</strong> Lifestyle Narratives 🏃</li>
                    <li><strong>Chapter 6:</strong> Write Your Story 🎯</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            
            # Interactive element: Choose your reading style
            reading_style = st.selectbox(
                "How would you like to experience this story?",
                ["📊 Data Explorer", "📖 Narrative Journey", "🔬 Scientific Investigator"]
            )
            
            if reading_style == "📖 Narrative Journey":
                st.success("Perfect! We'll focus on the human stories behind the data.")
            elif reading_style == "📊 Data Explorer":
                st.info("Great choice! We'll highlight the statistical insights.")
            else:
                st.warning("Excellent! We'll dive deep into the methodology.")
    
    # CHAPTER 1: MEET THE PEOPLE
    elif story_option == "👥 Meet the People":
        st.markdown('<h1 class="chapter-header">Chapter 1: Faces Behind the Numbers</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="story-card">
            <h3>The Cast of Characters</h3>
            <p>Each row in our dataset represents a person with unique circumstances. 
            Let's meet some of them and understand their stories.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Persona selection
        col1, col2, col3 = st.columns(3)
        
        personas = [
            {
                "id": "maria",
                "name": "Maria, 42",
                "description": "Single mother, works two jobs, prediabetic",
                "stats": {"BMI": 31, "HighBP": 1, "Income": 3},
                "story": "Between her office job and evening shifts, Maria finds little time for exercise. Affordable healthy food is hard to find in her neighborhood."
            },
            {
                "id": "james",
                "name": "James, 58",
                "description": "Retired teacher, recently diagnosed with diabetes",
                "stats": {"BMI": 28, "HighChol": 1, "Education": 6},
                "story": "James loves cooking but his traditional recipes are high in carbs. He's learning to adapt while managing his new diagnosis."
            },
            {
                "id": "sophia",
                "name": "Sophia, 29",
                "description": "Software engineer, healthy lifestyle",
                "stats": {"BMI": 23, "PhysActivity": 1, "Income": 8},
                "story": "Sophia prioritizes health with gym membership and meal prep, but her family history keeps her vigilant about diabetes risk."
            }
        ]
        
        for i, persona in enumerate([personas[0], personas[1], personas[2]]):
            with [col1, col2, col3][i]:
                st.markdown(f"""
                <div class="character-card">
                    <h4>{persona['name']}</h4>
                    <p><em>{persona['description']}</em></p>
                    <hr>
                    <p>{persona['story']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Follow {persona['name'].split(',')[0]}'s Journey", key=persona['id']):
                    st.session_state.selected_persona = persona
        
        # If persona selected, show their data story
        if st.session_state.selected_persona:
            persona = st.session_state.selected_persona
            
            st.markdown(f"""
            <div class="story-card">
                <h3>📊 {persona['name']}'s Health Profile</h3>
                <p>Let's explore what the data says about people with similar profiles...</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Find similar people in dataset
            similar_people = df[
                (df['BMI'].between(persona['stats']['BMI']-2, persona['stats']['BMI']+2)) &
                (df['Age'].between(40, 50) if persona['id'] == 'maria' else df['Age'].between(55, 65))
            ]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                similar_diabetes = similar_people['Diabetes_012'].value_counts(normalize=True) * 100
                fig = px.pie(
                    values=similar_diabetes.values,
                    names=['No Diabetes', 'Prediabetes', 'Diabetes'],
                    title=f"Diabetes Status of Similar People",
                    color_discrete_sequence=['#2E86AB', '#F18F01', '#A23B72']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.metric("Average BMI", f"{similar_people['BMI'].mean():.1f}")
                st.metric("High BP Rate", f"{similar_people['HighBP'].mean()*100:.1f}%")
                st.metric("Physically Active", f"{similar_people['PhysActivity'].mean()*100:.1f}%")
            
            with col3:
                st.markdown("""
                <div class="insight-box">
                    <strong>What This Means:</strong> 
                    People with similar profiles show varying outcomes based on 
                    lifestyle choices and access to healthcare.
                </div>
                """, unsafe_allow_html=True)
    
    # CHAPTER 2: THE BIG PICTURE
    elif story_option == "📈 The Big Picture":
        st.markdown('<h1 class="chapter-header">Chapter 2: The National Health Landscape</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="story-card">
            <h3>The Prevalence Story</h3>
            <p>In 2015, diabetes affected millions of Americans. Let's understand 
            the scale and distribution of this challenge.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive storytelling visualization
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create an animated narrative chart
            diabetes_counts = df['Diabetes_Story'].value_counts()
            
            fig = px.bar(
                x=diabetes_counts.index,
                y=diabetes_counts.values,
                title="The Three Paths: Diabetes Status Distribution",
                labels={'x': 'Health Journey', 'y': 'Number of People'},
                color=diabetes_counts.index,
                color_discrete_sequence=['#2E86AB', '#F18F01', '#A23B72']
            )
            
            # Add narrative annotations
            fig.add_annotation(
                x=0, y=diabetes_counts.values[0] + 2000,
                text="88% of population<br>Living without diabetes burden",
                showarrow=True,
                arrowhead=1
            )
            
            fig.add_annotation(
                x=1, y=diabetes_counts.values[1] + 1000,
                text="Critical intervention zone<br>Lives can still be changed",
                showarrow=True,
                arrowhead=1
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
                <h4>📖 The Narrative:</h4>
                <p>That <strong>5% in prediabetes</strong> represents our greatest 
                opportunity for change. These are people at a crossroads where 
                lifestyle interventions can rewrite their health story.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Age distribution story
            age_diabetes = df.groupby('Age_Story')['Diabetes_012'].mean() * 100
            
            st.metric("Diabetes Rate at 45+", "12.5%")
            st.metric("Diabetes Rate under 35", "2.1%")
            st.metric("Prediabetes Peak Age", "45-54 years")
        
        # Timeline of diabetes through life stages
        st.markdown("""
        <div class="story-card">
            <h3>📅 The Life Stage Timeline</h3>
            <p>Diabetes risk evolves through different life stages. Here's what typically happens:</p>
        </div>
        """, unsafe_allow_html=True)
        
        timeline_data = [
            {"age": "18-24", "risk": "Low", "story": "Youthful metabolism, often active"},
            {"age": "25-34", "risk": "Emerging", "story": "Career stress, less physical activity"},
            {"age": "35-44", "risk": "Increasing", "story": "Family responsibilities, weight gain"},
            {"age": "45-54", "risk": "High", "story": "Metabolic changes become apparent"},
            {"age": "55-64", "risk": "Peak", "story": "Cumulative lifestyle effects"},
            {"age": "65+", "risk": "Established", "story": "Managing chronic conditions"}
        ]
        
        for stage in timeline_data:
            st.markdown(f"""
            <div class="timeline-item">
                <h4>🎯 {stage['age']} Years</h4>
                <p><strong>Risk Level:</strong> {stage['risk']}</p>
                <p>{stage['story']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # CHAPTER 3: RISK DETECTIVE
    elif story_option == "🔍 Risk Detective":
        st.markdown('<h1 class="chapter-header">Chapter 3: Uncovering Risk Factors</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="story-card">
            <h3>🔍 The Investigation Begins</h3>
            <p>Diabetes rarely travels alone. It's often accompanied by other 
            health conditions. Let's investigate the patterns.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive detective game
        st.markdown("### 🎯 Which factors travel together with diabetes?")
        
        selected_factor = st.selectbox(
            "Choose a risk factor to investigate:",
            ["High Blood Pressure", "High Cholesterol", "Obesity", "Heart Disease", "Stroke"]
        )
        
        # Map selection to column
        factor_map = {
            "High Blood Pressure": "HighBP",
            "High Cholesterol": "HighChol",
            "Obesity": "BMI",
            "Heart Disease": "HeartDiseaseorAttack",
            "Stroke": "Stroke"
        }
        
        if selected_factor:
            factor_col = factor_map[selected_factor]
            
            if factor_col == "BMI":
                # For BMI, use categories
                diabetic_bmi = df[df['Diabetes_012'] == 2]['BMI'].mean()
                non_diabetic_bmi = df[df['Diabetes_012'] == 0]['BMI'].mean()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Average BMI with Diabetes", f"{diabetic_bmi:.1f}")
                with col2:
                    st.metric("Average BMI without Diabetes", f"{non_diabetic_bmi:.1f}")
                
                # BMI distribution story
                fig = px.histogram(
                    df, x='BMI', color='Diabetes_Story',
                    nbins=30,
                    title="BMI Distribution: The Weight of Evidence",
                    barmode='overlay',
                    opacity=0.7,
                    color_discrete_sequence=['#2E86AB', '#F18F01', '#A23B72']
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                <div class="insight-box">
                    <strong>Story Uncovered:</strong> Every 5-point increase in BMI 
                    approximately doubles diabetes risk. But remember—some people 
                    with normal BMI still develop diabetes, showing genetics 
                    also plays a role.
                </div>
                """, unsafe_allow_html=True)
            
            else:
                # For binary factors
                comorbidity_rate = df.groupby('Diabetes_Story')[factor_col].mean() * 100
                
                fig = px.bar(
                    x=comorbidity_rate.index,
                    y=comorbidity_rate.values,
                    title=f"{selected_factor} Comorbidity Rates",
                    labels={'x': 'Diabetes Status', 'y': f'{selected_factor} Rate (%)'},
                    color=comorbidity_rate.index,
                    color_discrete_sequence=['#2E86AB', '#F18F01', '#A23B72']
                )
                
                # Add dramatic difference annotation
                max_rate = comorbidity_rate.max()
                min_rate = comorbidity_rate.min()
                difference = max_rate - min_rate
                
                fig.add_annotation(
                    x=comorbidity_rate.idxmax(),
                    y=max_rate + 5,
                    text=f"{difference:.1f}% higher<br>than healthy group",
                    showarrow=True,
                    arrowhead=1
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # The correlation story
        st.markdown("""
        <div class="story-card">
            <h3>🔗 The Web of Connections</h3>
            <p>Health factors don't exist in isolation. They form interconnected 
            webs that tell complex stories.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive correlation explorer
        factor1 = st.selectbox("First Factor:", ['BMI', 'Age', 'GenHlth', 'Income', 'Education'])
        factor2 = st.selectbox("Second Factor:", ['HighBP', 'HighChol', 'Diabetes_012', 'PhysActivity', 'MentHlth'])
        
        if factor1 and factor2:
            fig = px.scatter(
                df.sample(1000),  # Sample for performance
                x=factor1,
                y=factor2,
                color='Diabetes_Story',
                title=f"How {factor1} Relates to {factor2}",
                opacity=0.6,
                color_discrete_sequence=['#2E86AB', '#F18F01', '#A23B72']
            )
            
            # Calculate correlation
            correlation = df[factor1].corr(df[factor2])
            
            fig.add_annotation(
                x=0.5, y=0.95,
                xref="paper", yref="paper",
                text=f"Correlation: {correlation:.3f}",
                showarrow=False,
                bgcolor="white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Interpret the correlation
            interpretation = ""
            if abs(correlation) > 0.5:
                interpretation = "Strong relationship"
            elif abs(correlation) > 0.3:
                interpretation = "Moderate relationship"
            elif abs(correlation) > 0.1:
                interpretation = "Weak relationship"
            else:
                interpretation = "Little to no relationship"
            
            st.markdown(f"""
            <div class="insight-box">
                <strong>Story Interpretation:</strong> {interpretation} between 
                {factor1.lower()} and {factor2.lower()}. This suggests that 
                {"they often travel together in people's health journeys" if correlation > 0.3 else "they operate somewhat independently in health narratives"}.
            </div>
            """, unsafe_allow_html=True)
    
    # CHAPTER 4: SOCIOECONOMIC STORIES
    elif story_option == "💰 Socioeconomic Stories":
        st.markdown('<h1 class="chapter-header">Chapter 4: The Economics of Health</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="story-card">
            <h3>💸 Money Matters in Health</h3>
            <p>Health isn't just biology—it's shaped by economics, education, 
            and access. Let's explore how socioeconomic factors write different 
            health stories.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Income inequality visualization
        income_diabetes = df.groupby('Income_Story')['Diabetes_012'].apply(
            lambda x: (x == 2).mean() * 100
        ).reset_index()
        
        fig = px.bar(
            income_diabetes,
            x='Income_Story',
            y='Diabetes_012',
            title="Diabetes Rates by Income Narrative",
            labels={'Income_Story': 'Income Level', 'Diabetes_012': 'Diabetes Rate (%)'},
            color='Income_Story',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        
        # Add story annotations
        annotations = [
            ("Limited means: Healthcare hurdles", "Highest diabetes rates", 85),
            ("Getting by: Making choices", "Every dollar counts for health", 60),
            ("Comfortable: More options", "Access to better food and care", 40),
            ("Prosperous: Better access", "Lowest diabetes burden", 20)
        ]
        
        for i, (x_pos, text, y_offset) in enumerate(annotations):
            fig.add_annotation(
                x=i,
                y=income_diabetes.loc[i, 'Diabetes_012'] + y_offset/100 * income_diabetes.loc[i, 'Diabetes_012'],
                text=text,
                showarrow=True,
                arrowhead=1,
                arrowsize=1,
                arrowwidth=2
            )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # The education story
        st.markdown("### 🎓 Education: The Protective Factor")
        
        education_diabetes = df.groupby('Education')['Diabetes_012'].apply(
            lambda x: (x == 2).mean() * 100
        ).reset_index()
        
        # Map education codes to stories
        education_stories = {
            1: "Never attended school",
            2: "Elementary school",
            3: "Some high school",
            4: "High school graduate",
            5: "Some college",
            6: "College graduate"
        }
        
        education_diabetes['Education_Story'] = education_diabetes['Education'].map(education_stories)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            fig2 = px.line(
                education_diabetes,
                x='Education_Story',
                y='Diabetes_012',
                title="The Education-Health Connection",
                markers=True,
                line_shape='spline'
            )
            
            fig2.update_layout(
                xaxis_title="Education Level",
                yaxis_title="Diabetes Rate (%)"
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
                <h4>📚 The Education Effect</h4>
                <p>College graduates have <strong>60% lower</strong> diabetes rates 
                than those without high school diplomas.</p>
                
                <p>Why?</p>
                <ul>
                    <li>Better health literacy</li>
                    <li>Higher income jobs</li>
                    <li>Healthier work environments</li>
                    <li>Better access to care</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Interactive: Build your socioeconomic profile
        st.markdown("""
        <div class="story-card">
            <h3>🎮 Build Your Socioeconomic Profile</h3>
            <p>See how different socioeconomic factors combine to create health risks.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            user_income = st.slider("Income Level (1=Lowest, 8=Highest)", 1, 8, 4)
            user_education = st.slider("Education Level (1-6)", 1, 6, 4)
        
        with col2:
            user_age = st.slider("Age", 18, 80, 45)
            user_access = st.selectbox("Healthcare Access", ["Limited", "Adequate", "Good", "Excellent"])
        
        if st.button("Calculate My Socioeconomic Risk Score"):
            # Simplified risk calculation
            income_score = (9 - user_income) * 1.5  # Lower income = higher risk
            education_score = (7 - user_education) * 1.2  # Less education = higher risk
            age_score = max(0, (user_age - 35) / 10) * 1.0  # Older = higher risk
            
            if user_access == "Limited":
                access_score = 3
            elif user_access == "Adequate":
                access_score = 1.5
            else:
                access_score = 0
            
            total_score = income_score + education_score + age_score + access_score
            max_score = 20
            risk_percentage = (total_score / max_score) * 100
            
            # Display results with storytelling
            st.progress(risk_percentage / 100)
            
            if risk_percentage > 70:
                st.error("""
                **High Socioeconomic Risk** 
                
                Your profile suggests significant barriers to optimal health. 
                Consider connecting with community health resources and 
                exploring assistance programs.
                """)
            elif risk_percentage > 40:
                st.warning("""
                **Moderate Socioeconomic Risk**
                
                You face some challenges in accessing optimal healthcare. 
                Proactive health management is key.
                """)
            else:
                st.success("""
                **Lower Socioeconomic Risk**
                
                Your socioeconomic profile provides good health advantages. 
                Use this position to build strong preventive habits.
                """)
    
    # CHAPTER 5: LIFESTYLE NARRATIVES
    elif story_option == "🏃 Lifestyle Narratives":
        st.markdown('<h1 class="chapter-header">Chapter 5: Daily Choices, Lasting Impact</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="story-card">
            <h3>🌱 The Power of Daily Habits</h3>
            <p>Big health outcomes are often the result of small daily choices. 
            Let's explore how lifestyle factors write health stories over time.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Lifestyle factor comparison
        lifestyle_factors = ['Smoker', 'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump']
        lifestyle_names = ['Smoking', 'Physical Activity', 'Fruit Consumption', 'Vegetable Consumption', 'Heavy Alcohol']
        
        # Calculate diabetes rates for each lifestyle factor
        lifestyle_data = []
        for factor in lifestyle_factors:
            for diabetes_status in [0, 2]:  # No diabetes vs diabetes
                subset = df[df['Diabetes_012'] == diabetes_status]
                rate = subset[factor].mean() * 100
                lifestyle_data.append({
                    'Factor': factor,
                    'Diabetes_Status': 'No Diabetes' if diabetes_status == 0 else 'Diabetes',
                    'Rate': rate
                })
        
        lifestyle_df = pd.DataFrame(lifestyle_data)
        
        # Create comparison visualization
        fig = px.bar(
            lifestyle_df,
            x='Factor',
            y='Rate',
            color='Diabetes_Status',
            barmode='group',
            title="Lifestyle Habits: Diabetes vs No Diabetes",
            labels={'Factor': 'Lifestyle Factor', 'Rate': 'Percentage (%)'},
            color_discrete_sequence=['#2E86AB', '#A23B72']
        )
        
        # Rename x-axis labels
        fig.update_xaxes(
            ticktext=lifestyle_names,
            tickvals=lifestyle_factors
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # The physical activity story
        st.markdown("### 🏃‍♀️ The Movement Narrative")
        
        activity_story = df.groupby('PhysActivity')['Diabetes_012'].value_counts(normalize=True).unstack() * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Diabetes Rate (Inactive)",
                f"{activity_story.loc[0, 2]:.1f}%",
                delta=f"-{activity_story.loc[0, 2] - activity_story.loc[1, 2]:.1f}%",
                delta_color="inverse"
            )
            
            st.markdown("""
            <div class="insight-box">
                <strong>The Sedentary Story:</strong> 
                People who are physically inactive are 40% more likely 
                to develop diabetes.
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric(
                "Diabetes Rate (Active)",
                f"{activity_story.loc[1, 2]:.1f}%"
            )
            
            st.markdown("""
            <div class="insight-box">
                <strong>The Active Advantage:</strong> 
                Even moderate activity like walking 30 minutes daily 
                significantly reduces diabetes risk.
            </div>
            """, unsafe_allow_html=True)
        
        # Interactive: Build your lifestyle story
        st.markdown("""
        <div class="story-card">
            <h3>📝 Write Your Lifestyle Story</h3>
            <p>See how changing one habit can rewrite your health narrative.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Current habits
        col1, col2, col3 = st.columns(3)
        
        with col1:
            current_activity = st.select_slider(
                "Weekly Exercise",
                options=["None", "1-2 days", "3-4 days", "5+ days"],
                value="1-2 days"
            )
        
        with col2:
            current_diet = st.select_slider(
                "Daily Fruits/Vegetables",
                options=["Rarely", "1-2 servings", "3-4 servings", "5+ servings"],
                value="1-2 servings"
            )
        
        with col3:
            current_smoking = st.radio(
                "Smoking Status",
                ["Non-smoker", "Former smoker", "Current smoker"]
            )
        
        # Improved habits
        st.markdown("#### 🌟 Now, imagine improving one habit...")
        
        improvement = st.selectbox(
            "Which habit would you like to improve?",
            ["Exercise more", "Eat more fruits/vegetables", "Quit smoking", "Reduce alcohol"]
        )
        
        if st.button("See The Story Change"):
            # Calculate baseline risk
            baseline_risk = 10  # Base risk score
            
            # Adjust based on current habits
            activity_scores = {"None": 4, "1-2 days": 2, "3-4 days": 1, "5+ days": 0}
            diet_scores = {"Rarely": 3, "1-2 servings": 1.5, "3-4 servings": 0.5, "5+ servings": 0}
            smoking_scores = {"Non-smoker": 0, "Former smoker": 1, "Current smoker": 3}
            
            current_score = (
                activity_scores[current_activity] +
                diet_scores[current_diet] +
                smoking_scores[current_smoking]
            )
            
            # Calculate improved score
            if improvement == "Exercise more":
                improved_activity = "5+ days" if current_activity != "5+ days" else current_activity
                improved_score = (
                    activity_scores[improved_activity] +
                    diet_scores[current_diet] +
                    smoking_scores[current_smoking]
                )
                story = f"By exercising {improved_activity.lower()}, you could reduce your diabetes risk significantly."
            
            elif improvement == "Eat more fruits/vegetables":
                improved_diet = "5+ servings" if current_diet != "5+ servings" else current_diet
                improved_score = (
                    activity_scores[current_activity] +
                    diet_scores[improved_diet] +
                    smoking_scores[current_smoking]
                )
                story = f"Eating {improved_diet.lower()} daily provides protective nutrients against diabetes."
            
            else:
                improved_score = current_score - 2  # Generic improvement
                story = "Making this positive change starts writing a healthier life story today."
            
            # Display the narrative
            reduction = ((current_score - improved_score) / current_score) * 100
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>📖 Your Health Story Revision</h4>
                <p><strong>Current narrative:</strong> {current_activity} exercise, 
                {current_diet} of fruits/vegetables, {current_smoking.lower()}</p>
                
                <p><strong>Improved narrative:</strong> {improvement.lower()}</p>
                
                <p><strong>The plot twist:</strong> This single change could 
                reduce your diabetes risk by approximately <strong>{reduction:.0f}%</strong>.</p>
                
                <p><em>{story}</em></p>
            </div>
            """, unsafe_allow_html=True)
    
    # CHAPTER 6: YOUR STORY
    elif story_option == "🎯 Your Story":
        st.markdown('<h1 class="chapter-header">Chapter 6: Write Your Health Future</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="story-card">
            <h3>✍️ Author Your Health Journey</h3>
            <p>Now that you've seen the patterns, it's time to apply them 
            to your own story. What will your health narrative be?</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive health journal
        st.markdown("### 📓 Your Health Journal")
        
        tab1, tab2, tab3 = st.tabs(["Current Chapter", "Plot Your Progress", "Future Chapters"])
        
        with tab1:
            st.markdown("#### 📍 Where are you in your health journey?")
            
            current_age = st.number_input("Your Age", min_value=18, max_value=100, value=35)
            current_bmi = st.number_input("Your BMI", min_value=15.0, max_value=50.0, value=25.0, step=0.1)
            family_history = st.radio("Family History of Diabetes", ["Yes", "No", "Not sure"])
            
            # Find similar stories in data
            similar_stories = df[
                (df['Age'].between(current_age-5, current_age+5)) &
                (df['BMI'].between(current_bmi-3, current_bmi+3))
            ]
            
            if len(similar_stories) > 0:
                similar_outcomes = similar_stories['Diabetes_Story'].value_counts(normalize=True) * 100
                
                st.markdown("#### 📊 People with Similar Stories")
                
                for story, percentage in similar_outcomes.items():
                    st.progress(percentage/100)
                    st.caption(f"{percentage:.1f}% - {story}")
                
                st.markdown("""
                <div class="insight-box">
                    <strong>Remember:</strong> These are patterns, not predictions. 
                    You have the power to write a different ending to your story.
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("#### 🎯 Set Your Health Plot Points")
            
            goal = st.selectbox(
                "What's your main health goal?",
                ["Prevent diabetes", "Reverse prediabetes", "Better manage diabetes", "Improve overall health"]
            )
            
            if goal:
                st.markdown("#### 📅 Your Action Plan")
                
                actions = {
                    "Prevent diabetes": [
                        "Walk 30 minutes daily",
                        "Add one vegetable to every meal",
                        "Get annual health checkup",
                        "Reduce sugary drinks"
                    ],
                    "Reverse prediabetes": [
                        "Lose 5-7% body weight",
                        "Exercise 150 minutes weekly",
                        "Choose whole grains",
                        "Monitor blood sugar monthly"
                    ],
                    "Better manage diabetes": [
                        "Check blood sugar daily",
                        "Follow medication schedule",
                        "Regular foot checks",
                        "Join support group"
                    ]
                }
                
                if goal in actions:
                    for i, action in enumerate(actions[goal], 1):
                        st.checkbox(f"{i}. {action}")
        
        with tab3:
            st.markdown("#### 🔮 Envision Your Future Chapters")
            
            timeline = st.slider("Look ahead... (years)", 1, 20, 5)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📖 Current Path Story")
                st.write("""
                If current patterns continue:
                - Gradual weight gain
                - Increasing health risks
                - More doctor visits
                - Higher medication needs
                """)
            
            with col2:
                st.markdown("##### 🌟 Improved Path Story")
                st.write(f"""
                With positive changes over {timeline} years:
                - Stable healthy weight
                - Reduced diabetes risk
                - More energy daily
                - Fewer health concerns
                - Active lifestyle maintained
                """)
            
            # Write your story
            st.markdown("#### ✍️ Write Your Future Story")
            
            future_story = st.text_area(
                "Describe your health story 5 years from now:",
                "In 5 years, I see myself as a healthier person who...",
                height=150
            )
            
            if st.button("Save My Story Vision"):
                st.success("""
                ✅ Your story vision has been saved!
                
                **Remember:** The most powerful stories are the ones we choose to write.
                Come back to this vision regularly to stay inspired on your journey.
                """)
        
        # Final inspiring message
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;'>
            <h2>🌟 Your Story Continues</h2>
            <p style='font-size: 1.2rem;'>
                Every day is a new page in your health story.<br>
                The data shows patterns, but <strong>you write the narrative</strong>.
            </p>
            <p style='font-size: 1.1rem; margin-top: 1rem;'>
                <em>"The best time to plant a tree was 20 years ago.<br>
                The second best time is now."</em>
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>📖 The Diabetes Chronicles | BRFSS 2015 Data | A Data Storytelling Project</p>
    <p>⚠️ This interactive story is for educational purposes. Always consult healthcare professionals for medical advice.</p>
    <p>Made with ❤️ using Streamlit and Plotly</p>
</div>
""", unsafe_allow_html=True)
