import requests
import sseclient
import streamlit as st
import uuid

import os
import sys
sys.path.append(os.path.abspath('../streamlit_scripts/utils'))
from streamlit_scripts.utils import base_request_url, generate_task_id, zenrowsApiKey, OWLER_PC_cookie, key_dict


st.title("Owler revenue scripts")


def reset_inputs():
    st.session_state["spreadsheet_url"] = ""
    st.session_state["sheet_name"] = ""
    st.session_state["column_name"] = ""
    st.session_state["sheet_name_result"] = ""
    st.session_state["domain_column_name"] = ""
    st.session_state["owler_column_name"] = ""


if "previous_option" not in st.session_state:
    st.session_state["previous_option"] = "Select one Owler revenue script"

owler_revenue_option = st.selectbox(
    "Select one Owler revenue script",
    ("Select one Owler revenue script",
     "Search Owler URLs & Scraping Owler URLs",
     "Scraping Owler URLs",
     )
)

if owler_revenue_option != st.session_state["previous_option"]:
    reset_inputs()

st.session_state["previous_option"] = owler_revenue_option

if owler_revenue_option != "Select one Owler revenue script":
    st.write("Before executing any script, please ensure that you share your spreadsheet with this account, granting editor permissions: kalungi-google-colab@invertible-now-393117.iam.gserviceaccount.com")

if owler_revenue_option == "Search Owler URLs & Scraping Owler URLs":
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (Here you should paste the spreadsheet URL which you are going to use)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Here you should write the name of the sheet where your data is)", key="sheet_name")
    column_name = st.text_input(
        "Domain column name (Here you should write the column name where the domains are)", key="column_name")
    sheet_name_result = st.text_input(
        "Result sheet name (Here you should write the name of the sheet where your scraped data will be pasted)", key="sheet_name_result")

if owler_revenue_option == "Scraping Owler URLs":
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (Here you should paste the spreadsheet URL which you are going to use)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Here you should write the name of the sheet where your data is)", key="sheet_name")
    domain_column_name = st.text_input(
        "Domain column name (Here you should write the column name where the domains are)", key="domain_column_name")
    owler_column_name = st.text_input(
        "Owler URL column name (Here you should write the column name where the Owler URLs are.)", key="owler_column_name")
    sheet_name_result = st.text_input(
        "Result sheet name (Here you should write the name of the sheet where your scraped data will be pasted)", key="sheet_name_result")

if st.button("Start scraping"):
    if not spreadsheet_url:
        st.error("Please fill spreadsheet URL.")
    else:
        try:
            task_id = generate_task_id()
            if owler_revenue_option == "Search Owler URLs & Scraping Owler URLs":
                payload = {
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name,
                    "column_name": column_name,
                    "key_dict": key_dict,
                    "sheet_name_result": sheet_name_result,
                    "OWLER_PC_cookie": OWLER_PC_cookie,
                    "zenrowsApiKey": zenrowsApiKey,
                    "task_id": task_id,
                }
                response = requests.post(
                    f"{base_request_url}/enrichment_scripts/search_owler_urls", json=payload)
                if response.status_code == 200:
                    st.success(f"Task started. Task ID: {task_id}")
                    search_sse_url = f"{base_request_url}/progress_stream/search_{task_id}"
                    scrape_sse_url = f"{base_request_url}/progress_stream/scrape_{task_id}"
                    search_progress_bar = st.progress(0)
                    scrape_progress_bar = st.progress(0)
                    search_messages = sseclient.SSEClient(search_sse_url)
                    for msg in search_messages:
                        if msg.data and msg.data.strip().isdigit():
                            progress = int(msg.data)
                            search_progress_bar.progress(progress)
                            if progress == 100:
                                st.success("Search phase completed!")
                                break
                    scrape_messages = sseclient.SSEClient(scrape_sse_url)
                    for msg in scrape_messages:
                        if msg.data and msg.data.strip().isdigit():
                            progress = int(msg.data)
                            scrape_progress_bar.progress(progress)
                            if progress == 100:
                                st.success("Scraping phase completed!")
                                break
                        else:
                            st.error(
                                f"Invalid progress data received: {msg.data}")
                else:
                    st.error(
                        f"Error starting task: {response.json().get('message')}")
            if owler_revenue_option == "Scraping Owler URLs":
                payload = {
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name,
                    "domain_column_name": domain_column_name,
                    "owler_column_name": owler_column_name,
                    "key_dict": key_dict,
                    "sheet_name_result": sheet_name_result,
                    "zenrowsApiKey": zenrowsApiKey,
                    "task_id": task_id,
                }
                response = requests.post(
                    f"{base_request_url}/enrichment_scripts/scraping_owler_urls", json=payload)
                if response.status_code == 200:
                    st.success(f"Task started. Task ID: {task_id}")
                    sse_url = f"{base_request_url}/progress_stream/{task_id}"
                    progress_bar = st.progress(0)
                    messages = sseclient.SSEClient(sse_url)
                    for msg in messages:
                        if msg.data and msg.data.strip().isdigit():
                            progress = int(msg.data)
                            progress_bar.progress(progress)
                            if progress == 100:
                                st.success("Scraping completed!")
                                break
                        else:
                            st.error(f"Invalid progress data: {msg.data}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.exception(e)
