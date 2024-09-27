import pandas as pd
import requests
import sseclient
import streamlit as st
import time
import uuid

import os
import sys
sys.path.append(os.path.abspath('../streamlit_scripts/utils'))
from streamlit_scripts.utils import base_request_url, generate_task_id, OPENAI_API_KEY, zenrowsApiKey, key_dict


def process_vertical_input(input_text):
    vertical_dict = {}
    lines = input_text.split('\n')
    for line in lines:
        if ':' in line:
            vertical, keywords = line.split(':', 1)
            keywords = [kw.strip().strip('"') for kw in keywords.split(',')]
            vertical_dict[vertical.strip()] = keywords
    return vertical_dict


st.title("QA with Searching Keyword")

option = st.selectbox(
    "Select a Client ICP",
    ("Select Client ICP", "New ICP Fit QA",
     "Headlight Solutions (Chemical)", "Headlight Solutions (Steel)")
)

if option == "New ICP Fit QA":
    keywords_input = "Keyword1_to_search, Keyword2_to_search, Keyword3_to_search..."
    prompt_input = "Assess if the company is a XXXXXX by searching for terms or phrases indicating this kind of services  including but not limited to XXXXXX. Respond in the following manner: Yes. Provide a brief explanation (no more than 300 characters) on why it qualifies. No. Provide a brief explanation (no more than 300 characters) on why it does not qualify. Maybe. If the information is ambiguous or insufficient, briefly explain (no more than 300 characters) why it's not possible to determine."
    verticals_input = ("Vertical1: \"Keyword1\", \"Keyword2\", \"Keyword3...\"\n"
                       "Vertical2: \"Keyword1\", \"Keyword2\", \"Keyword3...\"")

if option == "Headlight Solutions (Chemical)":
    keywords_input = "Delivery, Shipping, Chemical"
    prompt_input = "Assess if the company is a manufacturer or provides any delivery or shipping of Chemical products or derivatives by searching for terms or phrases indicating this kind of services  including but not limited to 'Chemical Distributors', 'Chemical Manufacturers', 'Shipping', 'Delivery'. Respond in the following manner: Yes. Provide a brief explanation (no more than 300 characters) on why it qualifies. No. Provide a brief explanation (no more than 300 characters) on why it does not qualify. Maybe. If the information is ambiguous or insufficient, briefly explain (no more than 300 characters) why it's not possible to determine."
    verticals_input = (
        "Shipping: \"Shipping\", \"Logistics\", \"Freight\"\n"
        "Chemicals: \"Chemical\", \"Chemicals\"\n"
        "Distributor: \"Distributor\", \"Distributors\"\n"
        "Delivery: \"Delivery\"\n"
        "Fleet: \"Fleet\"\n"
        "Truck: \"Truck\"\n"
        "Products: \"Aldehyde\", \"Aldehydes\", \"Alcohol\", \"Alcohols\", \"Ester\", \"Esters\", \"Ether\", \"Ethers\", \"Amine\", \"Amines\", \"Carboxylic Acid\", \"Carboxylic Acids\", \"Anhydride\", \"Anhydrides\", \"Aromatic Compound\", \"Aromatic Compounds\", \"Phenol\", \"Phenols\", \"Alkane\", \"Alkanes\", \"Alkene\", \"Alkenes\", \"Alkyne\", \"Alkynes\", \"Oxide\", \"Oxides\", \"Hydroxide\", \"Hydroxides\", \"Nitrate\", \"Nitrates\", \"Sulfate\", \"Sulfates\", \"Phosphate\", \"Phosphates\", \"Chloride\", \"Chlorides\", \"Carbonate\", \"Carbonates\", \"Surfactant\", \"Surfactants\", \"Adhesive\", \"Adhesives\", \"Coating\", \"Coatings\", \"Sealant\", \"Sealants\", \"Flame Retardant\", \"Flame Retardants\", \"Plasticizer\", \"Plasticizers\", \"Biocide\", \"Biocides\", \"Catalyst\", \"Catalysts\", \"Inhibitor\", \"Inhibitors\", \"Pigment\", \"Pigments\", \"Additive\", \"Additives\", \"Preservative\", \"Preservatives\", \"Polymer\", \"Polymers\", \"Methanol\", \"Acid\", \"Acids\", \"Ethanol\", \"Acetone\", \"Formaldehyde\", \"Lubricant\", \"Lubricants\", \"Ethylene\", \"Propylene\", \"Benzene\", \"Polyethylene\", \"Polypropylene\", \"Polyvinyl\", \"Pesticide\", \"Pesticides\", \"Emulsion\", \"Emulsions\"\n"
        "partner: \"DHL\", \"UPS\", \"USPS\", \"United Parcel Service\", \"Fedex\"\n"
        "Association: \"Association\""
    )

if option == "Headlight Solutions (Steel)":
    keywords_input = "Delivery, Shipping, Steel"
    prompt_input = "Assess if the company is a Steel products manufacturer or distributor or supplier. Respond in the following manner: Yes. Provide a brief explanation (no more than 300 characters) on why it qualifies. No. Provide a brief explanation (no more than 300 characters) on why it does not qualify. Maybe. If the information is ambiguous or insufficient, briefly explain (no more than 300 characters) why it's not possible to determine."
    verticals_input = (
        "Steel: \"Steel distributor\", \"Steel products supplier\", \"Steel wholesale\", \"Steel stockist\", \"Structural steel\", \"Steel fabrication\", \"Stainless steel\", \"Carbon steel\", \"Alloy steel\", \"Steel sheets\", \"Steel plates\", \"Steel bars\", \"Steel coils\", \"Steel pipes\", \"Steel tubing\", \"Steel beams\", \"Steel channels\", \"Steel angles\", \"Steel rods\", \"Steel wire\", \"Steel mesh\", \"Metal fabrication\", \"Industrial steel\", \"Steel processing\", \"Cold rolled steel\", \"Hot rolled steel\", \"Galvanized steel\", \"Mild steel\", \"Tool steel\", \"Steel service center\"\n"
        "Metal: \"Metal\", \"Iron\", \"Aluminium\", \"Copper\", \"Brass\", \"Bronze\", \"Nickel\", \"Titanium\", \"Zinc\", \"Lead\", \"Tin\", \"Chromium\", \"Magnesium\", \"Cobalt\", \"Manganese\", \"Tungsten\", \"Vanadium\"\n"
        "Distributor: \"Distributor\", \"Distributors\"\n"
        "Delivery: \"Delivery\"\n"
        "Fleet: \"Fleet\"\n"
        "Shipping: \"Shipping\"\n"
        "Truck: \"Truck\", \"Trucks\"\n"
        "Warehouse: \"warehouse\"\n"
        "Manufacturer: \"manufacturer\"\n"
        "Partner: \"DHL\", \"UPS\", \"USPS\", \"United Parcel Service\", \"Fedex\"\n"
        "Association: \"Association\""
    )

if option != "Select Client ICP":
    st.write("Use the IA QA tool when you have a list of domains that you need to do QA to check if the companies are fit with the ICP, you can also check if there are mention of certain keywords in the webpages.")
    st.write("[Tutorial >](https://www.loom.com/looms/videos)")

    spreadsheet_url = st.text_input(
        "Select a Google Sheets URL", "https://docs.google.com/spreadsheets/d/1WdRriLXggLZlz1dIoyiGMEdu13YVWibJLp7u5-Z6Gjo/edit?gid=352666901#gid=352666901")
    sheet_name = st.text_input("Select the Sheet Name", "Test")
    column_name = st.text_input("Select the Column Name", "domain")
    serper_api = st.text_input(
        "Select a Serper API", "091de71c94b24d78f85f38e527c370ae6c2f2f59")

    keywords = st.text_area(
        "Enter keywords separated by commas", keywords_input)
    keywords_list = [keyword.strip() for keyword in keywords.split(',')]
    keywords_final = ['"' + keyword + '"' for keyword in keywords_list]
    formatted_keywords = " | ".join(keywords_final)
    st.write("Formatted Keywords:", formatted_keywords)

    prompt = st.text_area("Enter the prompt", prompt_input)

    verticals = st.text_area(
        "Enter the verticals and their keywords", verticals_input)

    if verticals:
        vertical_dict = process_vertical_input(verticals)

    if st.button("Start processing"):
        if not spreadsheet_url or not serper_api:
            st.error("Please enter both the Spreadsheet URL and the Serper API key")
        else:
            with st.spinner("Running the scraper. This could take a few minutes depending on the list size..."):
                try:
                    task_id = generate_task_id()
                    payload = {
                        "spreadsheet_url": spreadsheet_url,
                        "sheet_name": sheet_name,
                        "column_name": column_name,
                        "serper_api": serper_api,
                        "zenrowsApiKey": zenrowsApiKey,
                        "OPENAI_API_KEY": OPENAI_API_KEY,
                        "formatted_keywords": formatted_keywords,
                        "prompt": prompt,
                        "vertical_dict": vertical_dict,
                        "key_dict": key_dict,
                        "task_id": task_id,
                    }
                    response = requests.post(
                        f"{base_request_url}/enrichment_scripts/ai_qa", json=payload)
                    if response.status_code == 200:
                        st.success(f"Task started. Task ID: {task_id}")
                        sse_url = f"{base_request_url}/progress_stream/{task_id}"
                        messages = sseclient.SSEClient(sse_url)
                        progress_bar = st.progress(0)
                        for msg in messages:
                            progress = int(msg.data)
                            progress_bar.progress(progress)
                            if progress == 100:
                                st.success("Enrichment completed!")
                                break

                        result_url = f"{base_request_url}/enrichment_scripts/ai_qa/result/{task_id}"
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
                                totalcost = result_data["totalcost"]
                                st.dataframe(result)
                                st.write(
                                    f"El costo total fue: ${totalcost:.6f}")
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
