"""
Story generator utilities for the diabetes dashboard
"""

import random
from typing import Dict, List
import pandas as pd

class DiabetesStoryGenerator:
    """Generate human-readable stories from diabetes data"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    def generate_persona_story(self, row: pd.Series) -> str:
        """Generate a story for an individual data point"""
        
        age_story = {
            (0, 3): "a young adult starting their journey",
            (4, 6): "in the prime working years",
            (7, 9): "navigating midlife challenges",
            (10, 13): "in the wisdom years of life"
        }
        
        bmi_story = {
            (0, 18.5): "maintaining a lean physique",
            (18.5, 25): "keeping a healthy weight",
            (25, 30): "carrying some extra weight",
            (30, 100): "facing weight management challenges"
        }
        
        # Find age category
        age_category = next(
            (desc for (low, high), desc in age_story.items() 
             if low <= row['Age'] <= high),
            "at an unspecified age"
        )
        
        # Find BMI category
        bmi_category = next(
            (desc for (low, high), desc in bmi_story.items() 
             if low <= row['BMI'] <= high),
            "with an unspecified weight"
        )
        
        # Diabetes status
        diabetes_map = {
            0: "managing to stay diabetes-free",
            1: "navigating the prediabetes warning zone",
            2: "living with diabetes"
        }
        
        diabetes_story = diabetes_map.get(row['Diabetes_012'], "with unspecified diabetes status")
        
        # Build the story
        story_templates = [
            f"This person is {age_category}, {bmi_category}, and {diabetes_story}.",
            f"At this life stage, they're {age_category} and {diabetes_story}, while {bmi_category}.",
            f"{diabetes_story.capitalize()} while {age_category} and {bmi_category}."
        ]
        
        return random.choice(story_templates)
    
    def generate_insight_story(self, insight_type: str, data: Dict) -> str:
        """Generate narrative insights from data patterns"""
        
        insight_templates = {
            "age_trend": [
                "As people move through life chapters, diabetes risk evolves. {age_group} see "
                "{change} in diabetes rates compared to younger groups.",
                
                "The story of diabetes changes with age. {age_group} experience "
                "{change}, telling us about cumulative lifestyle effects."
            ],
            
            "income_effect": [
                "Health stories are written with different resources. Those with {income_level} "
                "face {comparison} diabetes rates, highlighting healthcare access narratives.",
                
                "Economic circumstances shape health journeys. {income_level} individuals "
                "have {comparison} diabetes prevalence, revealing opportunity gaps."
            ],
            
            "lifestyle_impact": [
                "Daily choices write health futures. People who {habit} show "
                "{effect} in diabetes rates compared to those who don't.",
                
                "Small habits create big health stories. {habit} is associated with "
                "{effect}, demonstrating lifestyle's narrative power."
            ]
        }
        
        template = random.choice(insight_templates.get(insight_type, ["{data}"]))
        return template.format(**data)
    
    def create_data_point_character(self, index: int) -> Dict:
        """Create a character profile from a data point"""
        if index >= len(self.df):
            index = random.randint(0, len(self.df)-1)
        
        row = self.df.iloc[index]
        
        # Generate a name
        names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Drew"]
        
        # Create character profile
        character = {
            "name": random.choice(names),
            "age_group": self._get_age_group(row['Age']),
            "bmi_category": self._get_bmi_category(row['BMI']),
            "diabetes_status": self._get_diabetes_status(row['Diabetes_012']),
            "challenges": self._identify_challenges(row),
            "strengths": self._identify_strengths(row),
            "story": self.generate_persona_story(row)
        }
        
        return character
    
    def _get_age_group(self, age: int) -> str:
        groups = {
            (0, 3): "Young Adult (18-24)",
            (4, 6): "Established Adult (25-44)",
            (7, 9): "Midlife (45-64)",
            (10, 13): "Senior (65+)"
        }
        return next((name for (low, high), name in groups.items() if low <= age <= high), "Unknown")
    
    def _get_bmi_category(self, bmi: float) -> str:
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def _get_diabetes_status(self, status: int) -> str:
        return ["No Diabetes", "Prediabetes", "Diabetes"][int(status)]
    
    def _identify_challenges(self, row: pd.Series) -> List[str]:
        challenges = []
        
        if row['HighBP'] == 1:
            challenges.append("High blood pressure")
        if row['HighChol'] == 1:
            challenges.append("High cholesterol")
        if row['Smoker'] == 1:
            challenges.append("Smoking habit")
        if row['PhysActivity'] == 0:
            challenges.append("Sedentary lifestyle")
        if row['NoDocbcCost'] == 1:
            challenges.append("Healthcare access due to cost")
        
        return challenges or ["Managing general health"]
    
    def _identify_strengths(self, row: pd.Series) -> List[str]:
        strengths = []
        
        if row['PhysActivity'] == 1:
            strengths.append("Physically active")
        if row['Fruits'] == 1 or row['Veggies'] == 1:
            strengths.append("Healthy eating habits")
        if row['AnyHealthcare'] == 1:
            strengths.append("Access to healthcare")
        if row['Education'] >= 5:
            strengths.append("Higher education")
        
        return strengths or ["Resilience in health journey"]


# Example usage in your Streamlit app
def add_storytelling_elements():
    """Add storytelling elements to your dashboard"""
    
    # Initialize story generator
    story_gen = DiabetesStoryGenerator(df)
    
    # Generate a random character story
    character = story_gen.create_data_point_character(42)
    
    # Display the character story
    st.markdown(f"""
    <div class="character-spotlight">
        <h3>👤 Meet {character['name']}</h3>
        <p><strong>Age:</strong> {character['age_group']}</p>
        <p><strong>Health Status:</strong> {character['diabetes_status']}</p>
        <p><strong>Challenges:</strong> {', '.join(character['challenges'])}</p>
        <p><strong>Strengths:</strong> {', '.join(character['strengths'])}</p>
        <hr>
        <p><em>{character['story']}</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate insight story
    insight_data = {
        "age_group": "adults over 45",
        "change": "a significant increase"
    }
    
    insight_story = story_gen.generate_insight_story("age_trend", insight_data)
    
    st.markdown(f"""
    <div class="story-quote">
        {insight_story}
    </div>
    """, unsafe_allow_html=True)