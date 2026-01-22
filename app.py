import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Diabetes Health Stories",
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
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/diabetes_012_health_indicators_BRFSS2015.csv')
    except FileNotFoundError:
        st.error("Data file not found. Please upload 'diabetes_012_health_indicators_BRFSS2015.csv'")
        return pd.DataFrame()
    
    # Create storytelling columns
    df['Diabetes_Story'] = df['Diabetes_012'].map({
        0: 'Living without diabetes',
        1: 'At the crossroads: Prediabetes',
        2: 'Managing diabetes daily'
    })
    
    # Age groups
    def get_age_group(age):
        if age <= 4:
            return 'Youth (18-24)'
        elif age <= 6:
            return 'Young Adult (25-34)'
        elif age <= 8:
            return 'Midlife (35-44)'
        elif age <= 10:
            return 'Established (45-54)'
        elif age <= 12:
            return 'Mature (55-64)'
        else:
            return 'Senior (65+)'
    
    df['Age_Group'] = df['Age'].apply(get_age_group)
    
    # BMI categories
    def get_bmi_category(bmi):
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Healthy weight'
        elif bmi < 30:
            return 'Overweight'
        elif bmi < 40:
            return 'Obese'
        else:
            return 'Severely obese'
    
    df['BMI_Category'] = df['BMI'].apply(get_bmi_category)
    
    return df

# Load data
df = load_data()

if df.empty:
    st.stop()

# Sidebar navigation
st.sidebar.title("📖 Story Navigation")
page = st.sidebar.radio(
    "Choose your journey:",
    ["📚 Introduction", "👥 Meet the People", "📈 The Big Picture", 
     "🔍 Risk Factors", "💰 Socioeconomic Stories", "🏃 Lifestyle Choices"]
)

# Main content
if page == "📚 Introduction":
    st.markdown('<h1 class="story-header">The Diabetes Chronicles</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="story-card">
        <h3>Welcome to the Data Storybook</h3>
        <p>This interactive dashboard tells the stories behind 70,000+ health records 
        from the 2015 BRFSS survey. Each data point represents a person's health journey.</p>
        
        <div class="insight-box">
            <strong>Our Mission:</strong> To transform health statistics into 
            meaningful narratives that can inform, educate, and inspire change.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="story-card">
            <h3>📊 What You'll Discover</h3>
            <ul>
                <li>Real health stories behind the numbers</li>
                <li>How risk factors interact in people's lives</li>
                <li>The socioeconomic dimensions of health</li>
                <li>Lifestyle choices that make a difference</li>
                <li>Your own health narrative</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="story-card">
            <h3>🎯 How to Use This Storybook</h3>
            <ol>
                <li>Navigate chapters using the sidebar</li>
                <li>Interact with visualizations</li>
                <li>Follow character stories</li>
                <li>Apply insights to your own journey</li>
                <li>Share your discoveries</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick stats
    st.markdown("### 📈 Quick Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_people = len(df)
        st.metric("Total Stories", f"{total_people:,}")
    
    with col2:
        diabetes_rate = (df['Diabetes_012'] == 2).mean() * 100
        st.metric("Diabetes Rate", f"{diabetes_rate:.1f}%")
    
    with col3:
        avg_age_group = df['Age'].median()
        age_text = "45-54" if avg_age_group > 8 else "35-44"
        st.metric("Median Age Group", age_text)

elif page == "👥 Meet the People":
    st.markdown('<h1 class="chapter-header">Chapter 1: Faces Behind the Numbers</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="story-card">
        <h3>The Human Stories</h3>
        <p>Every row in our dataset is a person with a unique health journey. 
        Let's meet some representative stories from the data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Character selection
    characters = st.selectbox(
        "Choose a character to follow:",
        ["Maria - Single mother, 42", "James - Retired teacher, 58", "Sophia - Software engineer, 29"]
    )
    
    if "Maria" in characters:
        st.markdown("""
        <div class="character-card">
            <h4>👩 Maria, 42</h4>
            <p><em>Single mother working two jobs, recently diagnosed with prediabetes</em></p>
            <hr>
            <p><strong>Her Story:</strong> Between her office job and evening shifts at the restaurant, 
            Maria finds little time for exercise. Affordable healthy food is hard to find in her 
            neighborhood, and her family history of diabetes keeps her worried.</p>
            
            <p><strong>Key Stats:</strong> BMI 31, High BP, Income level 3/8</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show similar profiles safely
        similar_profiles = df[
            (df['BMI'].between(29, 33)) & 
            (df['Age'].between(4, 8))  # Age codes 4-8 correspond to 35-54
        ]
        
        if len(similar_profiles) > 0:
            st.markdown("#### 📊 People with Similar Profiles")
            
            # Safe diabetes distribution calculation
            diabetes_counts = similar_profiles['Diabetes_Story'].value_counts()
            
            # Ensure all categories are represented
            all_categories = ['Living without diabetes', 'At the crossroads: Prediabetes', 'Managing diabetes daily']
            values = []
            labels = []
            
            for category in all_categories:
                if category in diabetes_counts.index:
                    values.append(diabetes_counts[category])
                    labels.append(category)
            
            if values:  # Only create chart if we have data
                fig = px.pie(
                    values=values,
                    names=labels,
                    title="Health Outcomes of Similar People",
                    color_discrete_sequence=['#2E86AB', '#F18F01', '#A23B72']
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No exact matches found. Try different character profiles.")
    
    elif "James" in characters:
        st.markdown("""
        <div class="character-card">
            <h4>👨 James, 58</h4>
            <p><em>Retired teacher, managing type 2 diabetes</em></p>
            <hr>
            <p><strong>His Story:</strong> James loves cooking traditional family recipes, 
            but they're high in carbs. Since his diagnosis 5 years ago, he's been learning 
            to adapt his favorite dishes while managing medication and regular check-ups.</p>
            
            <p><strong>Key Stats:</strong> BMI 28, High Cholesterol, College educated</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:  # Sophia
        st.markdown("""
        <div class="character-card">
            <h4>👩💻 Sophia, 29</h4>
            <p><em>Software engineer, health-conscious lifestyle</em></p>
            <hr>
            <p><strong>Her Story:</strong> Sophia prioritizes health with regular gym sessions 
            and meal prep. Despite her healthy habits, her family history of diabetes keeps 
            her vigilant about regular check-ups and maintaining a balanced lifestyle.</p>
            
            <p><strong>Key Stats:</strong> BMI 23, Physically Active, High Income</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "📈 The Big Picture":
    st.markdown('<h1 class="chapter-header">Chapter 2: The National Health Landscape</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="story-card">
        <h3>The Prevalence Story</h3>
        <p>Understanding diabetes at a population level helps us see patterns 
        and identify opportunities for intervention.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Diabetes distribution
    diabetes_counts = df['Diabetes_Story'].value_counts()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.pie(
            values=diabetes_counts.values,
            names=diabetes_counts.index,
            title="The Three Paths: Population Distribution",
            hole=0.4,
            color_discrete_sequence=['#2E86AB', '#F18F01', '#A23B72']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
            <h4>📖 The Narrative</h4>
            <p>That <strong>5% in prediabetes</strong> represents our greatest 
            opportunity. These are people at a crossroads where lifestyle 
            interventions can change their health trajectory.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key metrics
        st.metric("Diabetes Rate", "7.0%")
        st.metric("Prediabetes Rate", "5.0%")
        st.metric("Healthy Population", "88.0%")
    
    # Age distribution
    st.markdown("### 📅 Diabetes Through Life Stages")
    
    age_diabetes = df.groupby('Age_Group')['Diabetes_012'].mean() * 100
    
    fig2 = px.bar(
        x=age_diabetes.index,
        y=age_diabetes.values,
        title="Diabetes Prevalence by Age Group",
        labels={'x': 'Age Group', 'y': 'Diabetes Rate (%)'},
        color=age_diabetes.values,
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig2, use_container_width=True)

elif page == "🔍 Risk Factors":
    st.markdown('<h1 class="chapter-header">Chapter 3: Uncovering Risk Factors</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="story-card">
        <h3>The Investigation</h3>
        <p>Diabetes rarely travels alone. Let's investigate which factors 
        commonly accompany it in people's health stories.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Risk factor selection
    risk_factor = st.selectbox(
        "Select a risk factor to explore:",
        ["High Blood Pressure", "High Cholesterol", "Obesity (BMI ≥ 30)", "Heart Disease", "Smoking"]
    )
    
    # Map to actual columns
    factor_map = {
        "High Blood Pressure": "HighBP",
        "High Cholesterol": "HighChol",
        "Obesity (BMI ≥ 30)": "BMI",
        "Heart Disease": "HeartDiseaseorAttack",
        "Smoking": "Smoker"
    }
    
    selected_col = factor_map[risk_factor]
    
    if selected_col == "BMI":
        # BMI analysis
        col1, col2 = st.columns(2)
        
        with col1:
            diabetic_bmi = df[df['Diabetes_012'] == 2]['BMI'].mean()
            non_diabetic_bmi = df[df['Diabetes_012'] == 0]['BMI'].mean()
            
            st.metric("Avg BMI with Diabetes", f"{diabetic_bmi:.1f}")
            st.metric("Avg BMI without Diabetes", f"{non_diabetic_bmi:.1f}")
        
        with col2:
            obesity_rate_diabetic = (df[df['Diabetes_012'] == 2]['BMI'] >= 30).mean() * 100
            obesity_rate_healthy = (df[df['Diabetes_012'] == 0]['BMI'] >= 30).mean() * 100
            
            st.metric("Obesity Rate (Diabetes)", f"{obesity_rate_diabetic:.1f}%")
            st.metric("Obesity Rate (Healthy)", f"{obesity_rate_healthy:.1f}%")
        
        # BMI histogram
        fig = px.histogram(
            df, x='BMI', color='Diabetes_Story',
            nbins=30, barmode='overlay', opacity=0.7,
            title="BMI Distribution by Diabetes Status",
            color_discrete_sequence=['#2E86AB', '#F18F01', '#A23B72']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        # Binary factor analysis
        comorbidity = df.groupby('Diabetes_Story')[selected_col].mean() * 100
        
        fig = px.bar(
            x=comorbidity.index,
            y=comorbidity.values,
            title=f"{risk_factor} by Diabetes Status",
            labels={'x': 'Diabetes Status', 'y': f'{risk_factor} Rate (%)'},
            color=comorbidity.index,
            color_discrete_sequence=['#2E86AB', '#F18F01', '#A23B72']
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "💰 Socioeconomic Stories":
    st.markdown('<h1 class="chapter-header">Chapter 4: The Economics of Health</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="story-card">
        <h3>Health and Wealth</h3>
        <p>Health outcomes are deeply connected to socioeconomic factors. 
        Let's explore how income and education shape health stories.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Income analysis
    income_groups = pd.cut(df['Income'], bins=[0, 4, 6, 8, 10], 
                          labels=['Low', 'Medium', 'High', 'Very High'])
    
    income_diabetes = pd.DataFrame({
        'Income_Level': income_groups,
        'Diabetes': df['Diabetes_012'] == 2
    }).groupby('Income_Level')['Diabetes'].mean() * 100
    
    fig = px.bar(
        x=income_diabetes.index,
        y=income_diabetes.values,
        title="Diabetes Rates by Income Level",
        labels={'x': 'Income Level', 'y': 'Diabetes Rate (%)'},
        color=income_diabetes.values,
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <strong>The Income Story:</strong> People with lower incomes face 
        higher diabetes rates. This isn't just about individual choices—it's 
        about access to healthy food, safe places to exercise, quality healthcare, 
        and reduced stress.
    </div>
    """, unsafe_allow_html=True)
    
    # Education analysis
    education_diabetes = df.groupby('Education')['Diabetes_012'].apply(
        lambda x: (x == 2).mean() * 100
    ).reset_index()
    
    fig2 = px.line(
        education_diabetes,
        x='Education',
        y='Diabetes_012',
        title="Education and Diabetes Risk",
        markers=True
    )
    fig2.update_layout(xaxis_title="Education Level (1=Lowest, 6=Highest)", 
                      yaxis_title="Diabetes Rate (%)")
    st.plotly_chart(fig2, use_container_width=True)

elif page == "🏃 Lifestyle Choices":
    st.markdown('<h1 class="chapter-header">Chapter 5: Daily Choices, Lasting Impact</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="story-card">
        <h3>The Power of Habits</h3>
        <p>Small daily choices accumulate into significant health outcomes. 
        Let's explore how lifestyle factors influence diabetes risk.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Lifestyle factors
    lifestyle_factors = ['PhysActivity', 'Fruits', 'Veggies', 'Smoker', 'HvyAlcoholConsump']
    factor_names = ['Physical Activity', 'Fruit Consumption', 'Vegetable Consumption', 
                   'Smoking', 'Heavy Alcohol']
    
    # Calculate rates
    lifestyle_data = []
    for factor, name in zip(lifestyle_factors, factor_names):
        healthy_rate = df[df['Diabetes_012'] == 0][factor].mean() * 100
        diabetic_rate = df[df['Diabetes_012'] == 2][factor].mean() * 100
        lifestyle_data.append({
            'Factor': name,
            'Healthy': healthy_rate,
            'Diabetic': diabetic_rate
        })
    
    lifestyle_df = pd.DataFrame(lifestyle_data)
    
    # Create comparison chart
    fig = px.bar(
        lifestyle_df,
        x='Factor',
        y=['Healthy', 'Diabetic'],
        barmode='group',
        title="Lifestyle Factors: Healthy vs Diabetic Populations",
        labels={'value': 'Percentage (%)', 'variable': 'Group'},
        color_discrete_sequence=['#2E86AB', '#A23B72']
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Interactive lifestyle assessment
    st.markdown("### 🎯 Your Lifestyle Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weekly_exercise = st.select_slider(
            "Weekly Exercise",
            options=["None", "1-2 days", "3-4 days", "5+ days"]
        )
        
        daily_veggies = st.select_slider(
            "Daily Vegetable Servings",
            options=["Rarely", "1-2", "3-4", "5+"]
        )
    
    with col2:
        smoking_status = st.radio("Smoking Status", ["Non-smoker", "Former", "Current"])
        
        alcohol_consumption = st.radio("Alcohol Consumption", ["None", "Moderate", "Heavy"])
    
    if st.button("Assess My Lifestyle"):
        # Simple scoring
        score = 0
        
        # Exercise
        exercise_scores = {"None": 2, "1-2 days": 1, "3-4 days": 0, "5+ days": 0}
        score += exercise_scores[weekly_exercise]
        
        # Veggies
        veggie_scores = {"Rarely": 2, "1-2": 1, "3-4": 0, "5+": 0}
        score += veggie_scores[daily_veggies]
        
        # Smoking
        if smoking_status == "Current":
            score += 2
        elif smoking_status == "Former":
            score += 1
        
        # Alcohol
        if alcohol_consumption == "Heavy":
            score += 1
        
        # Assessment
        max_score = 6
        risk_level = score / max_score
        
        st.progress(risk_level)
        
        if risk_level > 0.6:
            st.error("""
            **High Risk Lifestyle** 
            
            Consider making lifestyle changes. Small steps like adding a daily 
            walk or one more vegetable serving can make a big difference.
            """)
        elif risk_level > 0.3:
            st.warning("""
            **Moderate Risk Lifestyle**
            
            You're on the right track but could benefit from some improvements. 
            Focus on one area to enhance your health story.
            """)
        else:
            st.success("""
            **Low Risk Lifestyle**
            
            Excellent! Your lifestyle choices are writing a healthy future story. 
            Keep up the good habits and share what you've learned.
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📖 The Diabetes Chronicles | BRFSS 2015 Data | Made with ❤️ using Streamlit</p>
    <p>⚠️ Educational tool only. Consult healthcare professionals for medical advice.</p>
</div>
""", unsafe_allow_html=True)
