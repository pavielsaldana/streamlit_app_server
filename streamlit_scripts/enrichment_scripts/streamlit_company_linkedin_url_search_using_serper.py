import requests
import sseclient
import streamlit as st
import uuid

import os
import sys
sys.path.append(os.path.abspath('../streamlit_scripts/streamlit_utils'))
from streamlit_scripts.streamlit_utils.py import base_request_url, generate_task_id, key_dict


st.title("Company LinkedIn URL Search using Serper")
st.write("Before executing any script, please ensure that you share your spreadsheet with this account, granting editor permissions: kalungi-google-colab@invertible-now-393117.iam.gserviceaccount.com")

spreadsheet_url = st.text_input("Spreadsheet URL", key="spreadsheet_url")
sheet_name = st.text_input("Sheet name", key="sheet_name")
column_name = st.text_input("Domain column name", key="column_name")
serper_api_key = st.text_input("Serper API key", key="serper_api_key")

if st.button("Start searching"):
    if not spreadsheet_url:
        st.error("Please fill spreadsheet URL.")
    elif not serper_api_key:
        st.error("Please fill Serper API key.")
    else:
        try:
            task_id = generate_task_id()
            payload = {
                "spreadsheet_url": spreadsheet_url,
                "sheet_name": sheet_name,
                "key_dict": key_dict,
                "column_name": column_name,
                "serper_api_key": serper_api_key,
                "task_id": task_id,
            }

            response = requests.post(
                f"{base_request_url}/enrichment_scripts/company_linkedin_url_search_using_serper", json=payload)
            if response.status_code == 200:
                st.success(f"Task started. Task ID: {task_id}")
                sse_url = f"{base_request_url}/progress_stream/{task_id}"
                messages = sseclient.SSEClient(sse_url)
                progress_bar = st.progress(0)
                for msg in messages:
                    progress = int(msg.data)
                    progress_bar.progress(progress)
                    if progress == 100:
                        st.success("Search completed!")
                        break
            else:
                st.error(
                    f"Error starting task: {response.json().get('message')}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.exception(e)
