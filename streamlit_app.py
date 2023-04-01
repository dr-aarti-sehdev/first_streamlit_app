## key imports
import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

## add titles, headers and text
streamlit.title("My Parents New Healthy Diner")
streamlit.header("Breakfast Menu")
streamlit.text("🐔 Hard-boiled free range egg")
streamlit.text("🥗 Kale, spinach and rocket smoothie")
streamlit.text("🥣 Omega 3 and blueberry oatmeal")
streamlit.text("🥑🍞 Avocado toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

## add independent dataframe 

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list.set_index('Fruit', inplace = True)
## add user interaction
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])

## display the selected fruits
fruits_to_show = my_fruit_list.loc[fruits_selected]

## display dataframe
streamlit.dataframe(fruits_to_show)

## define fruityvice data function
def get_fruityvice_data(this_fruit_choice):
     ## call fruityvice API from app
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    ## take the json version of the response and normalise it
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

## add header with text from fruityvice containng info about the fruit
streamlit.header("Fruityvice Fruit Advice!")

try:
    ## ask for input from user to enter a type of fruit they want to know about
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        fruitydat = get_fruityvice_data(fruit_choice)
        # display normalised data as a table
        streamlit.dataframe(fruitydat)

except URLError as e:
    streamlit.error()

## connect to snowflake

streamlit.header("The fruit load list contains: ")
## snowflake related functions
def get_fruit_load_list():
     with my_cnx.cursor() as my_cur:
          my_cur.execute("SELECT * FROM fruit_load_list")
          return my_cur.fetchall()

## add button to load the fruit
if streamlit.button('Get fruit load list'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     my_data_rows = get_fruit_load_list()
     streamlit.dataframe(my_data_rows)

     
streamlit.stop()
## allow user to add fruit to the list 
def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
          my_cur.execute("INSERT INTO fruit_load_list VALUES (new_fruit)")
          return "Thanks for adding " + new_fruit 
     
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     my_added_fruit = insert_row_snowflake(add_my_fruit)
     streamlit.text(my_added_fruit)

