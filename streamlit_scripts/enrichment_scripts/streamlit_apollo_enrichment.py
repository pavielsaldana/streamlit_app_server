import requests
import sseclient
import streamlit as st
import uuid

import os
import sys
sys.path.append(os.path.abspath('../streamlit_scripts/utils'))
from streamlit_scripts.utils import base_request_url, generate_task_id, key_dict


st.title("Apollo enrichment scripts")


def reset_inputs():
    st.session_state["api_key_option"] = "Select an API key"
    st.session_state["spreadsheet_url"] = ""
    st.session_state["sheet_name"] = ""
    st.session_state["first_name_column_name"] = ""
    st.session_state["last_name_column_name"] = ""
    st.session_state["name_column_name"] = ""
    st.session_state["email_column_name"] = ""
    st.session_state["organization_name_column_name"] = ""
    st.session_state["domain_column_name"] = ""


if "previous_option" not in st.session_state:
    st.session_state["previous_option"] = "Select one Apollo enrichment script"
if "api_key_option" not in st.session_state:
    st.session_state["api_key_option"] = "Select an API key"

apollo_enrichment_option = st.selectbox(
    "Select one Apollo enrichment script",
    ("Select one Apollo enrichment script",
     "Contact enrichment",
     "Company enrichment",
     )
)
if apollo_enrichment_option != st.session_state["previous_option"]:
    reset_inputs()
    # Reset the API key selectbox
    st.session_state["api_key_option"] = "Select an API key"

st.session_state["previous_option"] = apollo_enrichment_option
if apollo_enrichment_option != "Select one Apollo enrichment script":
    st.write("Before executing any script, please ensure that you share your spreadsheet with this account, granting editor permissions: kalungi-google-colab@invertible-now-393117.iam.gserviceaccount.com")
    st.write("You can enrich 900 contacts/companies per hour using each API key.")
if apollo_enrichment_option == "Contact enrichment":
    api_key_option = st.selectbox("Select an API key", [
        'Select an API key',
        'API key 1',
        'API key 2',
        'API key 3',
        'API key 4',
        'API key 5',
        'API key 6',
    ], key="api_key_option")
    if api_key_option == 'API key 1':
        api_key = st.secrets["APOLLO_API_KEY_OCC"]["value"]
    elif api_key_option == 'API key 2':
        api_key = st.secrets["APOLLO_API_KEY_A360"]["value"]
    elif api_key_option == 'API key 3':
        api_key = st.secrets["APOLLO_API_KEY_N"]["value"]
    elif api_key_option == 'API key 4':
        api_key = st.secrets["APOLLO_API_KEY_S"]["value"]
    elif api_key_option == 'API key 5':
        api_key = st.secrets["APOLLO_API_KEY_SG"]["value"]
    elif api_key_option == 'API key 6':
        api_key = st.secrets["APOLLO_API_KEY_M"]["value"]
    else:
        api_key = None
    spreadsheet_url = st.text_input("Spreadsheet URL", key="spreadsheet_url")
    sheet_name = st.text_input("Sheet name", key="sheet_name")
    st.write(
        "All the following columns are optional, leave them empty if you do not have them.")
    first_name_column_name = st.text_input(
        "First name column name (The person's first name)", key="first_name_column_name")
    last_name_column_name = st.text_input(
        "Last name column name (The person's last name)", key="last_name_column_name")
    name_column_name = st.text_input(
        "Full name column name (The person's full name)", key="name_column_name")
    email_column_name = st.text_input(
        "Email column name (The person's email)", key="email_column_name")
    organization_name_column_name = st.text_input(
        "Company name column name (The person's company name)", key="organization_name_column_name")
    domain_column_name = st.text_input(
        "Domain column name (The person's company domain)", key="domain_column_name")
if apollo_enrichment_option == "Company enrichment":
    api_key_option = st.selectbox("Select an API key", [
        'Select an API key',
        'API key 1',
        'API key 2',
        'API key 3',
        'API key 4',
        'API key 5',
        'API key 6',
    ], key="api_key_option")
    if api_key_option == 'API key 1':
        api_key = st.secrets["APOLLO_API_KEY_OCC"]["value"]
    elif api_key_option == 'API key 2':
        api_key = st.secrets["APOLLO_API_KEY_A360"]["value"]
    elif api_key_option == 'API key 3':
        api_key = st.secrets["APOLLO_API_KEY_N"]["value"]
    elif api_key_option == 'API key 4':
        api_key = st.secrets["APOLLO_API_KEY_S"]["value"]
    elif api_key_option == 'API key 5':
        api_key = st.secrets["APOLLO_API_KEY_SG"]["value"]
    elif api_key_option == 'API key 6':
        api_key = st.secrets["APOLLO_API_KEY_M"]["value"]
    else:
        api_key = None
    spreadsheet_url = st.text_input("Spreadsheet URL", key="spreadsheet_url")
    sheet_name = st.text_input("Sheet name", key="sheet_name")
    domain_column_name = st.text_input(
        "Domain column name (The person's company domain)", key="domain_column_name")

if apollo_enrichment_option != "Select one Apollo enrichment script":
    if st.button("Start enrichment"):
        if not api_key:
            st.error("Please select an API key.")
        if not spreadsheet_url:
            st.error("Please fill spreadsheet URL.")
        if api_key and spreadsheet_url:
            try:
                task_id = generate_task_id()
                if apollo_enrichment_option == "Contact enrichment":
                    payload = {
                        "api_key": api_key,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "first_name_column_name": first_name_column_name,
                        "last_name_column_name": last_name_column_name,
                        "name_column_name": name_column_name,
                        "email_column_name": email_column_name,
                        "organization_name_column_name": organization_name_column_name,
                        "domain_column_name": domain_column_name,
                        "task_id": task_id,
                        "key_dict": key_dict,
                    }
                    response = requests.post(
                        f"{base_request_url}/enrichment_scripts/apollo_enrichment_contact", json=payload)
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
                                    st.success("Enrichment completed!")
                                    break
                            else:
                                st.error(f"Invalid progress data: {msg.data}")
                if apollo_enrichment_option == "Company enrichment":
                    payload = {
                        "api_key": api_key,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "domain_column_name": domain_column_name,
                        "task_id": task_id,
                        "key_dict": key_dict,
                    }
                    response = requests.post(
                        f"{base_request_url}/enrichment_scripts/apollo_enrichment_company", json=payload)
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
                                    st.success("Enrichment completed!")
                                    break
                            else:
                                st.error(f"Invalid progress data: {msg.data}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.exception(e)
