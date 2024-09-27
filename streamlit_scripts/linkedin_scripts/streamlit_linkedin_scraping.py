import requests
import sseclient
import streamlit as st
import uuid

import os
import sys
sys.path.append(os.path.abspath('../streamlit_scripts/utils'))
from streamlit_scripts.utils import base_request_url, generate_task_id, key_dict


st.title("LinkedIn scraping scripts")


def reset_inputs():
    st.session_state["li_at"] = ""
    st.session_state["spreadsheet_url"] = ""
    st.session_state["sheet_name"] = ""
    st.session_state["column_name"] = ""
    st.session_state["location_count"] = ""


def execute_progress_bar(payload):
    response = requests.post(
        f"{base_request_url}/linkedin_scripts/linkedin_scraping_scripts", json=payload)
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
                    st.success("Scraping completed!")
                    break
            else:
                st.error(f"Invalid progress data: {msg.data}")
    else:
        st.error(f"Failed to start task. Status code: {response.status_code}")


if "previous_option" not in st.session_state:
    st.session_state["previous_option"] = "Select one LinkedIn scraping script"

linkedin_scraping_option = st.selectbox(
    "Select one LinkedIn scraping script",
    ("Select one LinkedIn scraping script",
     "Sales Navigator lead search export",
     "Sales Navigator account export",
     "LinkedIn account scrape",
     "LinkedIn lead scrape",
     "LinkedIn account activity scrape",
     "LinkedIn lead activity scrape",
     "LinkedIn post commenters scrape",
     "LinkedIn job offers scrape",
     "LinkedIn job offer details scrape",
     )
)

if linkedin_scraping_option != st.session_state["previous_option"]:
    reset_inputs()

st.session_state["previous_option"] = linkedin_scraping_option

if linkedin_scraping_option != "Select one LinkedIn scraping script":
    st.write("Before executing any script, please ensure that you share your spreadsheet with this account, granting editor permissions: kalungi-google-colab@invertible-now-393117.iam.gserviceaccount.com")
if linkedin_scraping_option == "Sales Navigator lead search export":
    st.write("Use LinkedIn Sales Nave as a database and download any search results list from Sales Navigator. Use this when scraping contacts from a LinkedIn Sales Navigator query.")
    st.write("[Tutorial >](https://www.loom.com/looms/videos)")
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where the LinkedIn company links are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where the LinkedIn profile links are located)", key="sheet_name")
    column_name = st.text_input(
        "Column name (Name of the column where the LinkedIn profile links are located)", key="column_name")
if linkedin_scraping_option == "Sales Navigator account export":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where the LinkedIn company links are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where the LinkedIn profile links are located)", key="sheet_name")
    column_name = st.text_input(
        "Column name (Name of the column where the LinkedIn profile links are located)", key="column_name")
if linkedin_scraping_option == "LinkedIn account scrape":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where the LinkedIn company links are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where the LinkedIn company links are located)", key="sheet_name")
    column_name = st.text_input(
        "Column name (Name of the column where the LinkedIn company links are located)", key="column_name")
    location_count = st.text_input(
        "Location count (Number of locations to be scraped - choose between 0 and 100)", key="location_count")
if linkedin_scraping_option == "LinkedIn lead scrape":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where the LinkedIn profile links are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where the LinkedIn profile links are located)", key="sheet_name")
    column_name = st.text_input(
        "Column name (Name of the column where the LinkedIn profile links are located)", key="column_name")
if linkedin_scraping_option == "LinkedIn account activity scrape":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where the LinkedIn company links are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where the LinkedIn company links are located)", key="sheet_name")
    column_name = st.text_input(
        "Column name (Name of the column where the LinkedIn company links are located)", key="column_name")
if linkedin_scraping_option == "LinkedIn lead activity scrape":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where the LinkedIn profile links are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where the LinkedIn profile links are located)", key="sheet_name")
    column_name = st.text_input(
        "Column name (Name of the column where the LinkedIn profile links are located)", key="column_name")
if linkedin_scraping_option == "LinkedIn post commenters scrape":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where the LinkedIn activity links are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where the LinkedIn activity links are located)", key="sheet_name")
    column_name = st.text_input(
        "Column name (Name of the column where the LinkedIn activity links are located)", key="column_name")
if linkedin_scraping_option == "LinkedIn job offers scrape":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where the LinkedIn company links are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where the LinkedIn company links are located)", key="sheet_name")
    column_name = st.text_input(
        "Column name (Name of the column where the LinkedIn company links are located)", key="column_name")
if linkedin_scraping_option == "LinkedIn job offer details scrape":
    li_at = st.text_input(
        "li_at (LinkedIn authentication cookie)", key="li_at")
    spreadsheet_url = st.text_input(
        "Spreadsheet URL (URL of the spreadsheet where the IDs of the job offers are located)", key="spreadsheet_url")
    sheet_name = st.text_input(
        "Sheet name (Name of the sheet where the IDs of the job offers are located)", key="sheet_name")
    column_name = st.text_input(
        "Column name (Name of the column where the IDs of the job offers are located)", key="column_name")

if linkedin_scraping_option != "Select one LinkedIn scraping script":
    if st.button("Start scraping"):
        if not li_at:
            st.error("Please fill li_at.")
        if not spreadsheet_url:
            st.error("Please fill spreadsheet URL.")
        if li_at and spreadsheet_url:
            try:
                task_id = generate_task_id()
                if linkedin_scraping_option == "LinkedIn account scrape":
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "linkedin_scraping_option": linkedin_scraping_option,
                        "column_name": column_name,
                        "location_count": location_count,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
                else:
                    payload = {
                        "li_at": li_at,
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "linkedin_scraping_option": linkedin_scraping_option,
                        "column_name": column_name,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    execute_progress_bar(payload)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.exception(e)
