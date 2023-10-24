import streamlit as st

# Title and header
st.title("Simple Streamlit Greeting App")
st.header("Enter your name and click the button")

# User input
user_name = st.text_input("Enter your name")
button_clicked = st.button("Generate Greeting")

# Display the greeting message
if button_clicked:
    if user_name:
        st.write(f"Hello, {user_name}!")
    else:
        st.warning("Please enter your name and click the button.")