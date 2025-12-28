import streamlit as st
import requests
import os

st.set_page_config(page_title="Food Nutrition Analyzer", page_icon="🍎")

# USDA API Configuration
USDA_API_KEY = os.getenv("USDA_API_KEY", "DEMO_KEY")  # .env ကမရရင် DEMO_KEY သုံးမယ်
BASE_URL = "https://api.nal.usda.gov/fdc/v1"

# App Title
st.title("🍎 Food Nutrition Analyzer")
st.markdown("---")

# User input for food item
food_query = st.text_input(
    "🔍 **Enter any food item to analyze:**",
    placeholder="e.g., apple, chicken breast, rice, banana, pizza..."
)

# Search button
if st.button("🔬 Analyze Nutrition", type="primary") and food_query:
    with st.spinner(f'🔍 Searching nutrition data for "{food_query}"...'):
        try:
            # Make API request
            search_url = f"{BASE_URL}/foods/search"
            params = {
                "api_key": USDA_API_KEY,
                "query": food_query,
                "pageSize": 10,
                "dataType": ["Foundation", "SR Legacy"]
            }
            
            response = requests.get(search_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'foods' in data and data['foods']:
                    st.success(f"✅ Found {len(data['foods'])} results for '{food_query}'")
                    
                    # Show first 5 results
                    for i, food in enumerate(data['foods'][:5]):
                        with st.expander(f"🍽️ **{food.get('description', 'Unknown')}**", expanded=(i==0)):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**📁 Category:** {food.get('foodCategory', 'N/A')}")
                                st.write(f"**🏷️ Brand:** {food.get('brandOwner', 'Not specified')}")
                            
                            with col2:
                                st.write(f"**🔢 FDC ID:** {food.get('fdcId', 'N/A')}")
                                st.write(f"**📊 Data Type:** {', '.join(food.get('dataType', []))}")
                            
                            # Nutrition facts
                            st.subheader("📈 Nutrition Facts (per 100g):")
                            
                            # Common nutrients
                            nutrients = food.get('foodNutrients', [])
                            
                            if nutrients:
                                # Create columns for nutrients
                                cols = st.columns(3)
                                
                                nutrient_categories = {
                                    "Energy": ["Energy"],
                                    "Protein": ["Protein"],
                                    "Carbs": ["Carbohydrate", "Fiber", "Sugars"],
                                    "Fat": ["Total lipid", "Fatty acids", "Cholesterol"],
                                    "Minerals": ["Calcium", "Iron", "Sodium", "Potassium"],
                                    "Vitamins": ["Vitamin A", "Vitamin C", "Vitamin D"]
                                }
                                
                                for idx, (category, nutrient_names) in enumerate(nutrient_categories.items()):
                                    col_idx = idx % 3
                                    with cols[col_idx]:
                                        st.write(f"**{category}**")
                                        for nutrient in nutrients:
                                            nutrient_name = nutrient.get('nutrientName', '')
                                            value = nutrient.get('value', 0)
                                            unit = nutrient.get('unitName', '')
                                            
                                            if any(name in nutrient_name for name in nutrient_names):
                                                if value > 0:
                                                    st.write(f"• {nutrient_name}: {value} {unit}")
                            else:
                                st.info("No detailed nutrition data available")
                else:
                    st.warning(f"⚠️ No results found for '{food_query}'. Try a different food name.")
                    
            else:
                st.error(f"❌ API Error: Status code {response.status_code}")
                st.info("Please check your API key or try again later.")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Instructions in sidebar
with st.sidebar:
    st.title("ℹ️ How to Use")
    st.markdown("""
    1. **Enter any food name** in the search box
    2. **Click 'Analyze Nutrition'**
    3. **View detailed nutrition facts**
    4. **Expand each result** for more details
    
    ### 📋 Supported Foods:
    - Fruits (apple, banana, orange)
    - Vegetables (broccoli, carrot, spinach)
    - Meats (chicken, beef, pork)
    - Grains (rice, bread, pasta)
    - Dairy (milk, cheese, yogurt)
    - And many more!
    """)
    
    st.markdown("---")
    st.info("**Note:** Using DEMO_KEY has limited requests. For full access, add your USDA API key to `.env` file.")

# Footer
st.markdown("---")
st.caption("Powered by USDA FoodData Central API | Data provided for educational purposes")
