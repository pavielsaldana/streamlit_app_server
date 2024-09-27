import requests
import sseclient
import streamlit as st
import uuid

import os
import sys
sys.path.append(os.path.abspath('../streamlit_scripts/utils'))
from streamlit_scripts.utils import base_request_url, generate_task_id, key_dict


st.title("LinkedIn search scripts")


def reset_inputs():
    st.session_state["li_at"] = ""
    st.session_state["spreadsheet_url"] = ""
    st.session_state["sheet_name"] = ""
    st.session_state["first_name_column_name"] = ""
    st.session_state["last_name_column_name"] = ""
    st.session_state["company_name_column_name"] = ""
    st.session_state["query_column_name"] = ""
    st.session_state["company_column_name"] = ""


def execute_progress_bar(payload):
    response = requests.post(
        f"{base_request_url}/linkedin_scripts/linkedin_search_scripts", json=payload)
    if response.status_code == 200:
        st.success(f"Task ID: {task_id}")
        sse_url = f"{base_request_url}/progress_stream/{task_id}"
        progress_bar = st.progress(0)
        messages = sseclient.SSEClient(sse_url)
        for msg in messages:
            if msg.data and msg.data.strip().isdigit():
                progress = int(msg.data)
                progress_bar.progress(progress)
                if progress == 100:
                    st.success("Search completed!")
                    break
            else:
                st.error(f"Invalid progress data: {msg.data}")
    else:
        st.error(f"Failed to start task. Status code: {response.status_code}")


if "previous_option" not in st.session_state:
    st.session_state["previous_option"] = "Select one LinkedIn search script"

linkedin_search_option = st.selectbox(
    "Select one LinkedIn search script",
    ("Select one LinkedIn search script",
     "Get the first result from lead search (first name, last name and company name)",
     "Get the first result from lead search (any query)",
     "Get the first result from account search (company name)",
     )
)

if linkedin_search_option != st.session_state["previous_option"]:
    reset_inputs()
st.session_state["previous_option"] = linkedin_search_option

if linkedin_search_option != "Select one LinkedIn search script":
    st.write("Before executing any script, please ensure that you share your spreadsheet with this account, granting editor permissions: kalungi-google-colab@invertible-now-393117.iam.gserviceaccount.com")
if linkedin_search_option == "Get the first result from lead search (first name, last name and company name)":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where the first names, last names and company names are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where the first names, last names, and company names are located)", key="sheet_name")
    first_name_column_name = st.text_input(
        "First name column name (Name of the column where the first names are located)", key="first_name_column_name")
    last_name_column_name = st.text_input(
        "Last name column name (Name of the column where the last names are located)", key="last_name_column_name")
    company_name_column_name = st.text_input(
        "Company name column name (Name of the column where the company names are located)", key="company_name_column_name")
if linkedin_search_option == "Get the first result from lead search (any query)":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where the queries are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where the queries are located)", key="sheet_name")
    query_column_name = st.text_input(
        "Query column name (Name of the column where the queries are located)", key="query_column_name")
if linkedin_search_option == "Get the first result from account search (company name)":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where the company names are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where the company names are located)", key="sheet_name")
    company_column_name = st.text_input(
        "Company name column name (Name of the column where the company names are located)", key="company_column_name")

if linkedin_search_option != "Select one LinkedIn search script":
    if st.button("Start searching"):
        if not li_at:
            st.error("Please fill li_at.")
        if not spreadsheet_url:
            st.error("Please fill spreadsheet URL.")
        if li_at and spreadsheet_url:
            try:
                task_id = generate_task_id()
                if linkedin_search_option == "Get the first result from lead search (first name, last name and company name)":
                    script_type = 'people_search_first_name_last_name_company_name'
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "first_name_column_name": first_name_column_name,
                        "last_name_column_name": last_name_column_name,
                        "company_name_column_name": company_name_column_name,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_search_option == "Get the first result from lead search (any query)":
                    script_type = 'people_search_any_query'
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "query_column_name": query_column_name,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                if linkedin_search_option == "Get the first result from account search (company name)":
                    script_type = 'company_search_company_name'
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "script_type": script_type,
                        "company_column_name": company_column_name,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.exception(e)
