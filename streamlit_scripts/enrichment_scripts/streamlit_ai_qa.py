import pandas as pd
import requests
import sseclient
import streamlit as st
import time
import uuid

from streamlit_scripts.streamlit_utils import base_request_url, generate_task_id, OPENAI_API_KEY, zenrowsApiKey, key_dict


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
    ("Select Client ICP",
    "New ICP Fit QA",
    "Headlight Solutions (Chemical)",
    "Headlight Solutions (Steel)",
     "Onfleet (Groceries/Food/Prepared Meals/Delivery Review)",
    "Onfleet (General)",
    "Kalungi ABM",
    "Onfleet (Groceries/Food Delivery Review)",
    "Onfleet (Grocery Retailer Delivery Review)",
    "Onfleet (Prepared Meals Delivery Review)",
    "Onfleet (Retail Delivery Review)",
    "Onfleet (E-commerce Delivery Review)",
    )
)

if option == "New ICP Fit QA":
    keywords_input = "Keyword1_to_search, Keyword2_to_search, Keyword3_to_search..."
    prompt_input = "Assess if the company is a XXXXXX by searching for terms or phrases indicating this kind of services  including but not limited to XXXXXX. Respond in the following manner: Yes. Provide a brief explanation (no more than 300 characters) on why it qualifies. No. Provide a brief explanation (no more than 300 characters) on why it does not qualify. Maybe. If the information is ambiguous or insufficient, briefly explain (no more than 300 characters) why it's not possible to determine."
    verticals_input = ("Vertical1: \"Keyword1\", \"Keyword2\", \"Keyword3...\"\n"
                       "Vertical2: \"Keyword1\", \"Keyword2\", \"Keyword3...\"")

if option == "Kalungi ABM":
    keywords_input= "SaaS, Software as a Service, Software, Solution, Platform,e-commerce,ecommerce,e commerce"
    prompt_input= "Assess if the company offers any Software as a solution (SaaS); you can determine this by searching terms or phrases like solution, platform, book a demo, Cloud-based or references to a software solution offered to a customer. Respond in the following manner: Yes. Provide a brief explanation (no more than 300 characters) on why it qualifies. No. Provide a brief explanation (no more than 300 characters) on why it does not qualify. Maybe. If the information is ambiguous or insufficient, briefly explain (no more than 300 characters) why it's not possible to determine."
    verticals_input= ("Demo: \"Demo\", \"Contact for Sales\", \"Contact Sales\"\n"
                      "Software: \"Software\"\n"
                      "SaaS: \"Software as a Service\", \"SaaS\"\n"
                      "B2B: \"B2B\", \"Business to Business\"\n"
                      "Enterprise: \"Enterprise\"\n"
                      "Consulting: \"Consultors\", \"Consulting\", \"Audit\"\n"
                      "Platform_Migration: \"Platform Migration\", \"Integration\"\n"
                      "Development: \"App Development\", \"Software Development\"\n"
                      "Marketing: \"Marketing Agency\"\n"
                      "IT_Service: \"IT Service\"\n"
                      "AI: \"AI\, \"Artificial Intelligence\"")

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

if option == "Onfleet (Groceries/Food/Prepared Meals/Delivery Review)":
    keywords_input = "grocery delivery, fresh produce delivery, fruit delivery, vegetable delivery, home delivery, buy online, supermarket delivery, store pickup, meal delivery, ready-to-eat delivery, packaged meals, e-commerce store, buy online, raw meat, cheese"
    prompt_input = """
    Assess if the company falls into one of the following categories: Groceries Delivery, Grocery Retailer Delivery, Prepared Meals Delivery, Retail Delivery, or E-commerce Delivery.

    - **Groceries Delivery**: The company offers delivery services for fresh groceries and unprepared food items such as fruits, vegetables, raw meat, cheese, or other fresh food directly to the final consumer.
    - **Grocery Retailer Delivery**: The company is a grocery retailer with physical stores that offer delivery services to the final consumer.
    - **Prepared Meals Delivery**: The company offers delivery services for packaged, ready-to-eat meals to the final consumer.
    - **Retail Delivery**: The company has physical stores and offers delivery services to the final consumer, either through store pickup or home delivery.
    - **E-commerce Delivery**: The company operates exclusively online and offers delivery services directly to the final consumer.

    Respond in the following manner:
    - If it's a Groceries Delivery company: Groceries Delivery. Provide a brief explanation (no more than 300 characters) on why it qualifies.
    - If it's a Grocery Retailer Delivery company: Grocery Retailer Delivery. Provide a brief explanation (no more than 300 characters) on why it qualifies.
    - If it's a Prepared Meals Delivery company: Prepared Meals Delivery. Provide a brief explanation (no more than 300 characters) on why it qualifies.
    - If it's a Retail Delivery company: Retail Delivery. Provide a brief explanation (no more than 300 characters) on why it qualifies.
    - If it's an E-commerce Delivery company: E-commerce Delivery. Provide a brief explanation (no more than 300 characters) on why it qualifies.
    - If it doesn’t fit any category: Neither. Briefly explain (no more than 300 characters) why it's not possible to determine.
    """
    verticals_input = (
        "Groceries: \"Fresh produce\", \"Fruits\", \"Vegetables\", \"Raw meat\", \"Cheese\", \"Food delivery\"\n"
        "Supermarkets: \"Supermarket\", \"Physical stores\", \"In-store pickup\"\n"
        "Prepared_Meals: \"Ready-to-eat meals\", \"Packaged meals\", \"Meal delivery\"\n"
        "Retail: \"Physical stores\", \"In-store pickup\", \"Click and collect\"\n"
        "E-commerce: \"Online store\", \"Exclusively online\"\n"
        "Home_Delivery: \"Delivered to your door\",\"Delivery\", \"Home delivery\"\n"
        "Online_Purchase: \"Order online\", \"Buy online\"\n"
    )


if option == "Onfleet (General)":
    keywords_input= "last mile,delivery,courier,parcel delivery,final mile,package delivery,white glove,shipping,Home delivery,next day delivery"
    prompt_input= """
    Determine if the company falls under one of the following categories: Transport Logistics, Courier, Moving Services, or Delivery Operating.

    - **Transport Logistics**: These companies specialize in delivering goods directly from transportation hubs or distribution centers to the end user (either businesses or consumers), often handling heavier packages (over 150 pounds) and using terms like 3PL, LTL, 'last mile' or 'white glove' delivery. Exclude companies involved in oil, gas, liquid transportation, brokerage, or those not asset-based.

    - **Courier**: Courier companies primarily deliver packages under 150 pounds from warehouses, distribution centers, or retail stores directly to consumers using smaller vehicles such as cars or vans. They are not required to use specific delivery partners such as DHL, UPS, or USPS. Keywords include 'courier', 'express delivery', 'e-commerce delivery', 'home delivery', 'final mile', and 'last-mile delivery'.

    - **Moving Services**: Moving companies handle residential or commercial relocations, helping customers transport belongings from one location to another. Focus on terms like 'moving', 'relocation', or 'residential/commercial moves'.

    - **Delivery Operating**: Companies that offer delivery in their products but do not strictly fit the previous categories. For example, an e-commerce business that offers delivery or shipping in the products they offer.

    - **Neither**: If the company does not fit any of the above categories, classify it as "Neither" and explain why it doesn’t meet the criteria.

    Respond in the following format:
    - If it's a Transport Logistics company: Transport Logistics. brief explanation.
    - If it's a Courier: Courier. brief explanation.
    - If it's a Moving company: Moving. brief explanation.
    - If it doesn’t fit any category: Neither. brief explanation.
    """
    verticals_input = (
    "LastMile: \"Last Mile\", \"Last Mile Delivery\", \"Last-Mile\", \"Final Mile\", \"Final-Mile\"\n"
    "SupplyChain: \"Supply Chain\", \"Logistics\", \"Logistic\"\n"
    "WhiteGlove: \"White glove\", \"White-glove\"\n"
    "Bike: \"Bike\", \"Cargo bike\", \"Bike delivery\"\n"
    "Express: \"Express\", \"Express delivery\", \"Express Cargo\"\n"
    "Partner: \"DHL\", \"UPS\", \"USPS\", \"United Parcel Service\"\n"
    "Luxury: \"Luxury\", \"Limousine\"\n"
    "Moving: \"Move\", \"Moving\", \"Moving Storage\"\n"
    "Pallets: \"Pallets\", \"Pallet\"\n"
    "Materials: \"Oil\", \"Gas\", \"Sand\", \"Dirt\", \"Tandem axel tractor\", \"Water\", \"Bulk liquids\", \"Liquids\", \"Oversized\", \"Heavy Haul\", \"Auto Transport\", \"Chemical\", \"ISO tank\", \"SaaS\", \"Software as a Service\"\n"
    "Discard: \"Non-Asset\", \"Non Asset\", \"Broker\", \"Brokerage\"\n"
    "Keywords: \"Last mile\", \"Last-mile\", \"Courier\", \"Final mile\", \"Final-mile\", \"E-commerce delivery\", \"Ecommerce delivery\", \"White glove\", \"White-glove\", \"Home delivery\"\n"
    "Delivery: \"Shipping\", \"Delivery\"\n"
)

if option == "Onfleet (Groceries/Food Delivery Review)":
    keywords_input= "grocery delivery, fresh produce delivery, fruit delivery, vegetable delivery, home delivery, buy online"
    prompt_input= "Assess if the company offers delivery services for fresh groceries like fruits, vegetables, or other fresh food items directly to the final consumer. Respond in the following manner: Yes. Provide a brief explanation (no more than 300 characters) on why it qualifies. No. Provide a brief explanation (no more than 300 characters) on why it does not qualify. Maybe. If the information is ambiguous or insufficient, briefly explain (no more than 300 characters) why it's not possible to determine."
    verticals_input= ("Groceries: \"Fresh produce\", \"Fruits\", \"Vegetables\", \"Food delivery\"\n"
                      "Home_Delivery: \"Delivered to your door\", \"Home delivery\"\n"
                      "Online_Purchase: \"Order online\", \"Buy online\"\n")

if option == "Onfleet (Grocery Retailer Delivery Review)":
    keywords_input= "grocery delivery to home, supermarket delivery, shop online, store pickup, home delivery, buy groceries online"
    prompt_input= "Assess if the company is a grocery retailer with physical stores that offer delivery services to the final consumer. Respond in the following manner: Yes. Provide a brief explanation (no more than 300 characters) on why it qualifies. No. Provide a brief explanation (no more than 300 characters) on why it does not qualify. Maybe. If the information is ambiguous or insufficient, briefly explain (no more than 300 characters) why it's not possible to determine."
    verticals_input= ("Supermarkets: \"Supermarket\", \"Physical stores\", \"In-store pickup\"\n"
                      "Home_Delivery: \"Delivered to your door\", \"Home delivery\"\n"
                      "Online_Purchase: \"Order online\", \"Shop online\"\n")

if option == "Onfleet (Prepared Meals Delivery Review)":
    keywords_input= "meal delivery to home, packaged food delivery, ready-to-eat delivery, prepared meal kit, buy meals online, home delivery"
    prompt_input= "Assess if the company offers delivery services for packaged, ready-to-eat meals to the final consumer. Respond in the following manner: Yes. Provide a brief explanation (no more than 300 characters) on why it qualifies. No. Provide a brief explanation (no more than 300 characters) on why it does not qualify. Maybe. If the information is ambiguous or insufficient, briefly explain (no more than 300 characters) why it's not possible to determine."
    verticals_input= ("Prepared_Meals: \"Ready-to-eat meals\", \"Packaged meals\", \"Meal delivery\"\n"
                      "Home_Delivery: \"Delivered to your door\", \"Home delivery\"\n"
                      "Online_Purchase: \"Order online\", \"Buy meals online\"\n")

if option == "Onfleet (Retail Delivery Review)":
    keywords_input= "delivery to home, click and collect, store pickup, shipping to home, buy online, home delivery"
    prompt_input= "Assess if the retail company has physical stores and offers delivery services to the final consumer. Respond in the following manner: Yes. Provide a brief explanation (no more than 300 characters) on why it qualifies. No. Provide a brief explanation (no more than 300 characters) on why it does not qualify. Maybe. If the information is ambiguous or insufficient, briefly explain (no more than 300 characters) why it's not possible to determine."
    verticals_input= ("Retail: \"Physical stores\", \"In-store pickup\", \"Click and collect\"\n"
                      "Home_Delivery: \"Delivered to your door\", \"Home delivery\"\n"
                      "Online_Purchase: \"Order online\", \"Buy online\"\n")

if option == "Onfleet (E-commerce Delivery Review)":
    keywords_input= "delivery to home, online shipping, e-commerce store, free shipping to home, buy online, direct-to-consumer"
    prompt_input= "Assess if the e-commerce company offers delivery services directly to the final consumer, operating exclusively online. Respond in the following manner: Yes. Provide a brief explanation (no more than 300 characters) on why it qualifies. No. Provide a brief explanation (no more than 300 characters) on why it does not qualify. Maybe. If the information is ambiguous or insufficient, briefly explain (no more than 300 characters) why it's not possible to determine."
    verticals_input= ("E-commerce: \"Online store\", \"Exclusively online\"\n"
                      "Home_Delivery: \"Delivered to your door\", \"Home delivery\"\n"
                      "Online_Purchase: \"Order online\", \"Buy online\"\n")

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
