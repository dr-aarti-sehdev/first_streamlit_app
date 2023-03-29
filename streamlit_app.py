## key package
import streamlit

## add titles, headers and text
streamlit.title("My Parents New Healthy Diner")
streamlit.header("Breakfast Menu")
streamlit.text("🐔 Hard-boiled free range egg")
streamlit.text("🥗 Kale, spinach and rocket smoothie")
streamlit.text("🥣 Omega 3 and blueberry oatmeal")
streamlit.text("🥑🍞 Avocado toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

## add dataframe
import pandas as pd
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list.set_index('Fruit', inplace = True)
## add user interaction
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocados', 'Strawberry'])

## display dataframe
streamlit.dataframe(my_fruit_list)
