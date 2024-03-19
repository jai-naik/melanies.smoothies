# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Your Flavour Our Smoothy")
st.write("Choose the fruit which you want us to add in your customizable smoothy")

name_on_order = st.text_input("Name on the Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients', my_dataframe
    , max_selections = 5)
if ingredients_list:
	ingredients_string = ''

	for fruit_chosen in ingredients_list:
		ingredients_string += fruit_chosen + ' '
		st.subheader(fruit_chosen + 'Nutrition Information')
		fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon"+ fruit_chosen)
		fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
	st.write(ingredients_string)

    	my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
    	values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
  
    	# my_insert_stmt = f"INSERT INTO smoothies.public.orders (ingredients) VALUES ('{ingredients_string}', '{name_on_order}')"
    	time_to_insert = st.button('Submit Order')
    
    	#st.write(my_insert_stmt)
    	#st.stop()
    
    	if time_to_insert:
        	session.sql(my_insert_stmt).collect()
	    
        	st.success(f"Your Smoothie is ordered,  {name_on_order}", icon = "✅",)
    



