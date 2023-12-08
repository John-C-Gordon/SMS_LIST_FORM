import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from twilio.rest import Client

account_sid = 'AC9013123df2b0b98901639b236ce3a1f4'
auth_token = 'ffd8e21fb908f33e0102ca36bd7023d1'
client = Client(account_sid, auth_token)
st.title("You're Almost There!")
col1, col2 = st.columns(2)

conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="Sheet1", usecols=list(range(3)), ttl=5)
existing_data = existing_data.dropna(how="all")

with col1:
    first = st.text_input('First Name:')

with col2:
    last = st.text_input('Last Name:')

num = st.text_input('Phone Number *(in the format "8935558787")*:')

send = st.button('Add Yourself to Our List!')

if send and first and last and num:
    message = client.messages \
                    .create(
                        body='NEW SUBSCRIBER:\n' + '{}'.format(first) + ' ' + '{}'.format(last) + ': {}'.format(num),
                        from_='+18558677021',
                        to='+17577105116'
                    )

    st.write('*Got it! You should receive a confirmation from in a few moments. If you do not hear from us within 24 hours, please reach out to cougarbeatrice@gmail.com.*')


    df = pd.DataFrame(
        [
            {
                "First":first,
                "Last":last,
                "Phone #":num
            }
        ]
    )
    updated_df = pd.concat([existing_data, df], ignore_index=True)

    conn.update(worksheet="Sheet1", data=updated_df)

if send and (not first or not last or not num):
    st.write('*Please fill in all fields.*')

# st.image('LFR_8458 (1).jpg')