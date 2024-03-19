# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

st.title(":cup_with_straw: Your Flavour Our Smoothy")
st.write("Orders that need to be filled.")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()


if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:

        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
             og_dataset.merge(edited_dataset
                     , (og_dataset['order_uid'] == edited_dataset['order_uid'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
             st.success('someone clicked the button,', icon = "👍")
        except:
            st.write('Something went wrong.')

else:
    st.success('there are no pending orders right now.', icon = "👍")
    
