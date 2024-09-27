import pandas as pd
import requests
import sseclient
import streamlit as st
import time
import uuid

from streamlit_scripts.streamlit_utils import base_request_url, generate_task_id, key_dict, OPENAI_API_KEY


st.title("Title Cleaning")

option = st.selectbox(
    "Select a Client ICP",
    ("Select Scraper Type", "Onfleet (DSP)", "Onfleet (Resellers)")
)

if option == "Onfleet (DSP)":
    st.write("Use this tool when you need to make Title Cleaning standarization for a list of contact. to use this tool you should have created a title repository and a database with your standardized titles, below is a video on how to do it. It is important to note that you will also have to share your spreadsheet with this account, granting editor permissions: kalungi-google-colab@invertible-now-393117.iam.gserviceaccount.com.")
    st.write("[Tutorial >](https://www.loom.com/looms/videos)")
    spreadsheet_url = st.text_input(
        "Select a spreadsheet Url", "https://docs.google.com/spreadsheets/d/19hsZxx29AuBJ4zGBh8iB7ImqbT_lWZHKeXFd3mExkb0/edit?gid=0#gid=0")
    sheet_name = st.text_input("Select Sheet Name", "TC")
    column_name = st.text_input("Select Column Name", "title")
    spreadsheetUrl_DB = st.text_input(
        "Select Title DB Url", "https://docs.google.com/spreadsheets/d/173_FgevHCEA9jTOlHyp16hYsTXxNzwclZiLjUbcMl4Q/edit#gid=87246784")

elif option == "Onfleet (Resellers)":
    st.write("Use This tool when you need to make Title Cleaning standarization for a list of contact. to use this tool you should have created a title repository and a database with your standardized titles, below is a video on how to do it. It is important to note that you will also have to share your spreadsheet with this account, granting editor permissions: kalungi-google-colab@invertible-now-393117.iam.gserviceaccount.com.")
    st.write("[Tutorial >](https://www.loom.com/looms/videos)")
    spreadsheet_url = st.text_input(
        "Select a spreadsheet Url", "https://docs.google.com/spreadsheets/d/19hsZxx29AuBJ4zGBh8iB7ImqbT_lWZHKeXFd3mExkb0/edit?gid=0#gid=0")
    sheet_name = st.text_input("Select Sheet Name", "TC")
    column_name = st.text_input("Select Column Name", "title")
    spreadsheetUrl_DB = st.text_input(
        "Select Title DB Url", "https://docs.google.com/spreadsheets/d/1tbNbX1y-FEbE4hZXB6B2jfHEN3Xa2c3BA7PLGNKu0-s/edit#gid=0")

if option != "Select Client ICP":
    if st.button("Iniciar procesamiento"):
        if not spreadsheet_url or not spreadsheetUrl_DB:
            st.error("Please enter both the Spreadsheet URL and a Title DB Url")
        else:
            with st.spinner("Running the TC Tool. This could take a few minutes depending on the list size..."):
                try:
                    task_id = generate_task_id()
                    payload = {
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "column_name": column_name,
                        "spreadsheetUrl_DB": spreadsheetUrl_DB,
                        "OPENAI_API_KEY": OPENAI_API_KEY,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    response = requests.post(
                        f"{base_request_url}/data_cleaning_scripts/ai_title_cleaning", json=payload)
                    if response.status_code == 200:
                        st.success(f"Task started. Task ID: {task_id}")
                        sse_url = f"{base_request_url}/progress_stream/{task_id}"
                        messages = sseclient.SSEClient(sse_url)
                        progress_bar = st.progress(0)
                        for msg in messages:
                            progress = int(msg.data)
                            progress_bar.progress(progress)
                            if progress == 100:
                                st.success("TC completed!")
                                break

                        result_url = f"{base_request_url}/data_cleaning_scripts/ai_title_cleaning/result/{task_id}"
                        poll_interval = 5
                        while True:
                            time.sleep(poll_interval)
                            result_response = requests.get(result_url)
                            if result_response.status_code == 200:
                                result_data = result_response.json()
                                data = result_data["data"]
                                columns_order = result_data.get(
                                    "columns_order", list(data[0].keys()))
                                result = pd.DataFrame(
                                    data, columns=columns_order)
                                st.dataframe(result)
                                break
                            elif result_response.status_code == 202:
                                pass
                            else:
                                st.error(
                                    f"Error: {result_response.json().get('message', 'Unknown error occurred')}")
                                break
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.exception(e)
