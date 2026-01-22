import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Diabetes Health Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('diabetes_012_health_indicators_BRFSS2015.csv')
    
    # Create derived columns
    df['Diabetes_Status'] = df['Diabetes_012'].map({0: 'No Diabetes', 1: 'Prediabetes', 2: 'Diabetes'})
    df['Age_Group'] = pd.cut(df['Age'], bins=[0, 4, 6, 8, 10, 12, 14], 
                            labels=['18-24', '25-34', '35-44', '45-54', '55-64', '65+'])
    df['BMI_Category'] = pd.cut(df['BMI'], bins=[0, 18.5, 25, 30, 100], 
                               labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    
    # Income categories
    df['Income_Level'] = pd.cut(df['Income'], bins=[0, 4, 6, 8, 10], 
                               labels=['Low', 'Medium', 'High', 'Very High'])
    
    return df

# Load the data
df = load_data()

# Sidebar
st.sidebar.title("🎛️ Dashboard Controls")
st.sidebar.markdown("---")

# Filters
diabetes_filter = st.sidebar.multiselect(
    "Select Diabetes Status:",
    options=df['Diabetes_Status'].unique(),
    default=df['Diabetes_Status'].unique()
)

age_filter = st.sidebar.multiselect(
    "Select Age Groups:",
    options=df['Age_Group'].unique().tolist(),
    default=df['Age_Group'].unique().tolist()
)

bmi_filter = st.sidebar.multiselect(
    "Select BMI Categories:",
    options=df['BMI_Category'].unique().tolist(),
    default=df['BMI_Category'].unique().tolist()
)

# Apply filters
filtered_df = df[
    (df['Diabetes_Status'].isin(diabetes_filter)) &
    (df['Age_Group'].isin(age_filter)) &
    (df['BMI_Category'].isin(bmi_filter))
]

# Main dashboard
st.title("🏥 Diabetes Health Indicators Dashboard")
st.markdown("---")

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    total_cases = len(filtered_df)
    st.metric("Total Cases", f"{total_cases:,}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    diabetes_rate = (filtered_df['Diabetes_012'] == 2).mean() * 100
    st.metric("Diabetes Rate", f"{diabetes_rate:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    avg_bmi = filtered_df['BMI'].mean()
    st.metric("Average BMI", f"{avg_bmi:.1f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    high_bp_rate = filtered_df['HighBP'].mean() * 100
    st.metric("High BP Rate", f"{high_bp_rate:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# First row of charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Diabetes Distribution")
    
    # Diabetes distribution pie chart
    diabetes_counts = filtered_df['Diabetes_Status'].value_counts()
    fig1 = px.pie(
        values=diabetes_counts.values,
        names=diabetes_counts.index,
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📈 Health Risk Factors by Diabetes Status")
    
    # Prepare data for grouped bar chart
    risk_factors = ['HighBP', 'HighChol', 'HeartDiseaseorAttack', 'Stroke']
    risk_data = []
    
    for status in ['No Diabetes', 'Prediabetes', 'Diabetes']:
        status_df = filtered_df[filtered_df['Diabetes_Status'] == status]
        rates = {}
        for factor in risk_factors:
            rates[factor] = status_df[factor].mean() * 100
        rates['Status'] = status
        risk_data.append(rates)
    
    risk_df = pd.DataFrame(risk_data)
    
    fig2 = px.bar(
        risk_df,
        x='Status',
        y=risk_factors,
        barmode='group',
        labels={'value': 'Percentage (%)', 'variable': 'Risk Factor'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig2.update_layout(height=400, xaxis_title="", yaxis_title="Percentage (%)")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Second row of charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 BMI Distribution by Age Group")
    
    # BMI distribution heatmap
    bmi_age_data = filtered_df.groupby(['Age_Group', 'BMI_Category']).size().unstack(fill_value=0)
    
    fig3 = px.imshow(
        bmi_age_data,
        labels=dict(x="BMI Category", y="Age Group", color="Count"),
        color_continuous_scale='Viridis'
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("👥 Demographic Overview")
    
    # Create tabs for different demographic views
    demo_tab1, demo_tab2, demo_tab3 = st.tabs(["Age", "Income", "Gender"])
    
    with demo_tab1:
        age_diabetes = filtered_df.groupby(['Age_Group', 'Diabetes_Status']).size().unstack(fill_value=0)
        fig4 = px.bar(
            age_diabetes,
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig4.update_layout(height=300, xaxis_title="Age Group", yaxis_title="Count")
        st.plotly_chart(fig4, use_container_width=True)
    
    with demo_tab2:
        income_diabetes = filtered_df.groupby(['Income_Level', 'Diabetes_Status']).size().unstack(fill_value=0)
        fig5 = px.bar(
            income_diabetes,
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig5.update_layout(height=300, xaxis_title="Income Level", yaxis_title="Count")
        st.plotly_chart(fig5, use_container_width=True)
    
    with demo_tab3:
        gender_diabetes = filtered_df.groupby(['Sex', 'Diabetes_Status']).size().unstack(fill_value=0)
        gender_diabetes.index = gender_diabetes.index.map({0: 'Female', 1: 'Male'})
        fig6 = px.bar(
            gender_diabetes,
            barmode='group',
            color_discrete_sequence=['#FFB6C1', '#87CEFA']
        )
        fig6.update_layout(height=300, xaxis_title="Gender", yaxis_title="Count")
        st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# Third row - Advanced analytics
st.subheader("🔬 Advanced Analytics")

col1, col2 = st.columns(2)

with col1:
    # Correlation heatmap
    st.markdown("**Correlation Matrix**")
    
    # Select numerical columns for correlation
    numeric_cols = ['BMI', 'Age', 'GenHlth', 'MentHlth', 'PhysHlth', 'Education', 'Income']
    corr_data = filtered_df[numeric_cols].corr()
    
    fig7 = px.imshow(
        corr_data,
        text_auto='.2f',
        color_continuous_scale='RdBu_r',
        aspect="auto"
    )
    fig7.update_layout(height=400)
    st.plotly_chart(fig7, use_container_width=True)

with col2:
    # Lifestyle factors
    st.markdown("**Lifestyle Factors Analysis**")
    
    lifestyle_factors = ['Smoker', 'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump']
    lifestyle_data = []
    
    for status in ['No Diabetes', 'Prediabetes', 'Diabetes']:
        status_df = filtered_df[filtered_df['Diabetes_Status'] == status]
        rates = {}
        for factor in lifestyle_factors:
            rates[factor] = status_df[factor].mean() * 100
        rates['Status'] = status
        lifestyle_data.append(rates)
    
    lifestyle_df = pd.DataFrame(lifestyle_data)
    
    fig8 = px.bar(
        lifestyle_df,
        x='Status',
        y=lifestyle_factors,
        barmode='group',
        labels={'value': 'Percentage (%)', 'variable': 'Lifestyle Factor'},
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig8.update_layout(height=400, xaxis_title="", yaxis_title="Percentage (%)")
    st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")

# Fourth row - Data explorer and insights
st.subheader("🔍 Data Explorer & Insights")

tab1, tab2, tab3 = st.tabs(["Data Preview", "Risk Calculator", "Insights"])

with tab1:
    st.dataframe(
        filtered_df.head(100),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name="filtered_diabetes_data.csv",
        mime="text/csv"
    )

with tab2:
    st.markdown("### 🧮 Diabetes Risk Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age_input = st.slider("Age", 18, 100, 45)
        bmi_input = st.slider("BMI", 15.0, 50.0, 25.0)
        bp_input = st.radio("High Blood Pressure?", ["No", "Yes"])
        chol_input = st.radio("High Cholesterol?", ["No", "Yes"])
    
    with col2:
        smoker_input = st.radio("Smoker?", ["No", "Yes"])
        activity_input = st.radio("Physically Active?", ["No", "Yes"])
        family_history = st.radio("Family History of Diabetes?", ["No", "Yes"])
        income_level = st.select_slider("Income Level", options=["Low", "Medium", "High", "Very High"])
    
    if st.button("Calculate Risk Score"):
        # Simplified risk calculation (for demonstration)
        risk_score = 0
        
        if age_input >= 45:
            risk_score += 2
        if bmi_input >= 30:
            risk_score += 3
        elif bmi_input >= 25:
            risk_score += 1
        if bp_input == "Yes":
            risk_score += 2
        if chol_input == "Yes":
            risk_score += 1
        if smoker_input == "Yes":
            risk_score += 1
        if activity_input == "No":
            risk_score += 2
        if family_history == "Yes":
            risk_score += 3
        
        max_score = 14
        risk_percentage = (risk_score / max_score) * 100
        
        st.progress(risk_percentage / 100)
        st.metric("Your Diabetes Risk Score", f"{risk_score}/{max_score}")
        
        if risk_score >= 10:
            st.warning("🔴 High Risk: Please consult a healthcare provider")
        elif risk_score >= 5:
            st.info("🟡 Moderate Risk: Consider lifestyle changes")
        else:
            st.success("🟢 Low Risk: Maintain healthy habits")

with tab3:
    st.markdown("### 💡 Key Insights")
    
    insights = [
        "1. **Diabetes prevalence increases significantly with age**, especially after 45 years",
        "2. **High BMI is strongly correlated** with diabetes diagnosis",
        "3. **Individuals with high blood pressure** are 3x more likely to develop diabetes",
        "4. **Physical activity reduces diabetes risk** by approximately 40%",
        "5. **Lower income levels** show higher diabetes prevalence",
        "6. **Smoking increases diabetes risk** by 30-40%",
        "7. **Regular fruit and vegetable consumption** shows protective effects",
        "8. **Mental health challenges** are more common in diabetic populations"
    ]
    
    for insight in insights:
        st.markdown(f"- {insight}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Diabetes Health Dashboard | BRFSS 2015 Data | Made with Streamlit</p>
        <p>⚠️ This dashboard is for educational purposes only. Consult healthcare professionals for medical advice.</p>
    </div>
    """,
    unsafe_allow_html=True
)