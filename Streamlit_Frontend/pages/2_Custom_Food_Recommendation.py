import streamlit as st
from Generate_Recommendations import Generator
from ImageFinder.ImageFinder import get_images_links as find_image
import pandas as pd
from streamlit_echarts import st_echarts

st.set_page_config(
    page_title="Custom Food Recommendation",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS & STYLING ====================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Manrope', sans-serif;
    }
    
    .main {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(10px);
    }
    
    .stApp {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 58, 138, 0.8));
    }
    
    h1, h2, h3 {
        font-family: 'Manrope', sans-serif;
        font-weight: 700;
        color: #06b6d4;
    }
    
    h2 {
        border-bottom: 2px solid rgba(6, 182, 212, 0.3);
        padding-bottom: 0.8rem;
    }
    
    .stExpander {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.4), rgba(6, 182, 212, 0.05));
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 12px;
    }
    
    p, .stMarkdown {
        color: #e2e8f0;
    }
    
    .stTextInput, .stNumberInput, .stSlider {
        color: #e2e8f0;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

glass_css = """
<style>
    .stApp {
        background:
            radial-gradient(circle at 78% 12%, rgba(20, 184, 166, 0.18), transparent 30%),
            radial-gradient(circle at 18% 18%, rgba(37, 99, 235, 0.22), transparent 34%),
            linear-gradient(135deg, #09070d 0%, #0b1020 48%, #061520 100%);
    }

    .main,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background: transparent;
    }

    section[data-testid="stSidebar"] {
        background: rgba(11, 10, 17, 0.84);
        border-right: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(24px) saturate(130%);
        -webkit-backdrop-filter: blur(24px) saturate(130%);
    }

    h1, h2, h3 {
        color: #f8fafc;
    }

    div[data-testid="stExpander"],
    [data-testid="stForm"] {
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.28);
        border-radius: 18px;
        background:
            linear-gradient(145deg, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0.055)),
            rgba(31, 33, 33, 0.48);
        backdrop-filter: blur(28px) saturate(135%);
        -webkit-backdrop-filter: blur(28px) saturate(135%);
        box-shadow:
            0 24px 68px rgba(0, 0, 0, 0.38),
            inset 0 1px 0 rgba(255, 255, 255, 0.34);
    }

    .stButton > button {
        border: 1px solid rgba(255, 255, 255, 0.24);
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
    }
</style>
"""

st.markdown(glass_css, unsafe_allow_html=True)

nutrition_values=['Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent']
if 'generated' not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations=None

class Recommendation:
    def __init__(self,nutrition_list,nb_recommendations,ingredient_txt):
        self.nutrition_list=nutrition_list
        self.nb_recommendations=nb_recommendations
        self.ingredient_txt=ingredient_txt
        pass
    def generate(self,):
        params={'n_neighbors':self.nb_recommendations,'return_distance':False}
        ingredients=self.ingredient_txt.split(';')
        generator=Generator(self.nutrition_list,ingredients,params)
        recommendations=generator.generate()
        recommendations = recommendations.json()['output']
        if recommendations!=None:              
            for recipe in recommendations:
                recipe['image_link']=find_image(recipe['Name'])
        return recommendations

class Display:
    def __init__(self):
        self.nutrition_values=nutrition_values

    def display_recommendation(self,recommendations):
        st.subheader('Recommended recipes:')
        if recommendations!=None:
            rows=len(recommendations)//5
            for column,row in zip(st.columns(5),range(5)):
                with column:
                    for recipe in recommendations[rows*row:rows*(row+1)]:                             
                        recipe_name=recipe['Name']
                        expander = st.expander(recipe_name)
                        recipe_link=recipe['image_link']
                        recipe_img=f'<div><center><img src={recipe_link} alt={recipe_name}></center></div>'     
                        nutritions_df=pd.DataFrame({value:[recipe[value]] for value in nutrition_values})      
                        
                        expander.markdown(recipe_img,unsafe_allow_html=True)  
                        expander.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Nutritional Values (g):</h5>', unsafe_allow_html=True)                   
                        expander.dataframe(nutritions_df)
                        expander.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Ingredients:</h5>', unsafe_allow_html=True)
                        for ingredient in recipe['RecipeIngredientParts']:
                            expander.markdown(f"""
                                        - {ingredient}
                            """)
                        expander.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Recipe Instructions:</h5>', unsafe_allow_html=True)    
                        for instruction in recipe['RecipeInstructions']:
                            expander.markdown(f"""
                                        - {instruction}
                            """) 
                        expander.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Cooking and Preparation Time:</h5>', unsafe_allow_html=True)   
                        expander.markdown(f"""
                                - Cook Time       : {recipe['CookTime']}min
                                - Preparation Time: {recipe['PrepTime']}min
                                - Total Time      : {recipe['TotalTime']}min
                            """)                       
        else:
            st.info('Couldn\'t find any recipes with the specified ingredients')
    def display_overview(self,recommendations):
        if recommendations!=None:
            st.subheader('Overview:')
            col1,col2,col3=st.columns(3)
            with col2:
                selected_recipe_name=st.selectbox('Select a recipe',[recipe['Name'] for recipe in recommendations])
            st.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Nutritional Values:</h5>', unsafe_allow_html=True)
            for recipe in recommendations:
                if recipe['Name']==selected_recipe_name:
                    selected_recipe=recipe
            options = {
        "title": {"text": "Nutrition values", "subtext": f"{selected_recipe_name}", "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left",},
        "series": [
            {
                "name": "Nutrition values",
                "type": "pie",
                "radius": "50%",
                "data": [{"value":selected_recipe[nutrition_value],"name":nutrition_value} for nutrition_value in self.nutrition_values],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }
            st_echarts(options=options, height="600px",)
            st.caption('You can select/deselect an item (nutrition value) from the legend.')

title="<h1 style='text-align: center;'>Custom Food Recommendation</h1>"
st.markdown(title, unsafe_allow_html=True)


display=Display()

with st.form("recommendation_form"):
    st.header('Nutritional values:')
    Calories = st.slider('Calories', 0, 4000, 500)
    FatContent = st.slider('FatContent', 0, 100, 50)
    SaturatedFatContent = st.slider('SaturatedFatContent', 0, 13, 0)
    CholesterolContent = st.slider('CholesterolContent', 0, 300, 0)
    SodiumContent = st.slider('SodiumContent', 0, 2300, 400)
    CarbohydrateContent = st.slider('CarbohydrateContent', 0, 325, 100)
    FiberContent = st.slider('FiberContent', 0, 50, 10)
    SugarContent = st.slider('SugarContent', 0, 40, 10)
    ProteinContent = st.slider('ProteinContent', 0, 100, 10)
    nutritions_values_list=[Calories,FatContent,SaturatedFatContent,CholesterolContent,SodiumContent,CarbohydrateContent,FiberContent,SugarContent,ProteinContent]
    st.header('Recommendation options (OPTIONAL):')
    nb_recommendations = st.slider('Number of recommendations', 5, 20,step=5)
    ingredient_txt=st.text_input('Specify ingredients to include in the recommendations separated by ";" :',placeholder='Ingredient1;Ingredient2;...')
    st.caption('Example: Milk;eggs;butter;chicken...')
    generated = st.form_submit_button("Generate")
if generated:
    with st.spinner('Generating recommendations...'): 
        recommendation=Recommendation(nutritions_values_list,nb_recommendations,ingredient_txt)
        recommendations=recommendation.generate()
        st.session_state.recommendations=recommendations
    st.session_state.generated=True 

if st.session_state.generated:
    with st.container():
        display.display_recommendation(st.session_state.recommendations)
    with st.container():
        display.display_overview(st.session_state.recommendations)
