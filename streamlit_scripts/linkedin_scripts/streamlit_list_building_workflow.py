import pandas as pd
import requests
import sseclient
import streamlit as st
import time
import uuid

from streamlit_scripts.streamlit_utils import base_request_url, generate_task_id, key_dict

st.title("List Building Workflow")

option = st.selectbox(
    "Select a Client ICP",
    ("Select Client ICP", "Onfleet (DSP)", "Onfleet (Resellers)", "Headlight Solutions", "Agility Health")
)

if option != "Select Client ICP":
    st.write("Generic List Building workflow. It is important to note that you will also have to share your spreadsheet with this account, granting editor permissions: kalungi-google-colab@invertible-now-393117.iam.gserviceaccount.com.")
    st.write("[Tutorial >](https://www.loom.com/looms/videos)")
    spreadsheet_url = st.text_input("Select a spreadsheet Url", "")
    sheet_name = st.text_input("Select Sheet Name", "")
    column_name = st.text_input("Select Column Name", "")
    li_at = st.text_input("LinkedIn authentication cookie", "")
    if option == "Onfleet (DSP)":
        sales_navigator_query_1 = st.text_input("Sales Navigator query 1", "https://www.linkedin.com/sales/search/people?query=(recentSearchParam%3A(id%3A2744797746%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3ACURRENT_COMPANY%2Cvalues%3AList((id%3Aurn%253Ali%253Aorganization%253A18875652%2Ctext%3ARedwood%2520Logistics%2CselectionType%3AINCLUDED%2Cparent%3A(id%3A0))))%2C(type%3ACURRENT_TITLE%2Cvalues%3AList((text%3A%2528%25E2%2580%259Cdirector%25E2%2580%259D%2520AND%2520%2528%25E2%2580%259Ce-commerce%25E2%2580%259D%2520OR%2520%25E2%2580%259Cdigital%2520transformation%25E2%2580%259D%2520OR%2520%25E2%2580%259CIT%25E2%2580%259D%2520OR%2520%25E2%2580%259Cinformation%2520technology%25E2%2580%259D%2520OR%2520%25E2%2580%259Coperations%25E2%2580%259D%2520OR%2520%25E2%2580%259Ctechnology%2520transformation%25E2%2580%259D%2520OR%2520%25E2%2580%259Csupply%2520chain%25E2%2580%259D%2520OR%2520%25E2%2580%259Clast%2520mile%25E2%2580%259D%2520OR%2520%25E2%2580%259Ccustomer%2520experience%25E2%2580%259D%2520OR%2520%25E2%2580%259Ccustomer%2520success%25E2%2580%259D%2520OR%2520%25E2%2580%259Clogistics%25E2%2580%259D%2520OR%2520%25E2%2580%259CTransportation%25E2%2580%259D%2520OR%2520%25E2%2580%259COmni-channel%25E2%2580%259D%2520OR%2520%25E2%2580%259CFinal%2520Mile%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CLast%2520mile%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CWhite%2520Glove%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CHome%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CSystems%25E2%2580%259D%2520OR%2520%25E2%2580%259CIntegrations%25E2%2580%259D%2520OR%2520%25E2%2580%259CProject%2520Management%25E2%2580%259D%2520OR%2520%25E2%2580%259CDelivery%25E2%2580%259D%2529%2529%2CselectionType%3AINCLUDED)%2C(text%3A%2528%25E2%2580%259Cmanager%25E2%2580%259D%2520AND%2520%2528%25E2%2580%259Cdigital%2520transformation%25E2%2580%259D%2520OR%2520%25E2%2580%259Coperations%25E2%2580%259D%2520OR%2520%25E2%2580%259Clogistics%25E2%2580%259D%2520OR%2520%25E2%2580%259Cfleet%25E2%2580%259D%2520OR%2520%25E2%2580%259Ctransportation%25E2%2580%259D%2529%2529%2520OR%2520%2528%25E2%2580%259Chead%25E2%2580%259D%2520AND%2520%2528%25E2%2580%259Clogistics%25E2%2580%259D%2520OR%2520%25E2%2580%259Clast%2520mile%25E2%2580%259D%2529%2529%2520OR%2520%2528%25E2%2580%259CVP%25E2%2580%259D%2520OR%2520%25E2%2580%259Cvice%2520president%25E2%2580%259D%2520AND%2520%2528%25E2%2580%259Clogistics%25E2%2580%259D%2520OR%2520%25E2%2580%259CTransportation%25E2%2580%259D%2520OR%2520%25E2%2580%259COmni-channel%25E2%2580%259D%2520OR%2520%25E2%2580%259CFinal%2520Mile%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CLast%2520mile%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CWhite%2520Glove%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CHome%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CSystems%25E2%2580%259D%2520OR%2520%25E2%2580%259CIntegrations%25E2%2580%259D%2520OR%2520%25E2%2580%259CProject%2520Management%25E2%2580%259D%2520OR%2520%25E2%2580%259CDelivery%25E2%2580%259D%2520OR%2520%25E2%2580%259Ce-commerce%25E2%2580%259D%2520OR%2520%25E2%2580%259CIT%25E2%2580%259D%2520OR%2520%25E2%2580%259Cinformation%2520technology%25E2%2580%259D%2529%2529%2CselectionType%3AINCLUDED)))%2C(type%3AREGION%2Cvalues%3AList((id%3A102221843%2Ctext%3ANorth%2520America%2CselectionType%3AINCLUDED)))))&sessionId=Jw%2BJm9jCTDC8NeUOv2pBoA%3D%3D")
        sales_navigator_query_2 = st.text_input("Sales Navigator query 2", "https://www.linkedin.com/sales/search/people?query=(recentSearchParam%3A(id%3A2744797746%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3ACURRENT_COMPANY%2Cvalues%3AList((id%3Aurn%253Ali%253Aorganization%253A18875652%2Ctext%3ARedwood%2520Logistics%2CselectionType%3AINCLUDED%2Cparent%3A(id%3A0))))%2C(type%3AREGION%2Cvalues%3AList((id%3A102221843%2Ctext%3ANorth%2520America%2CselectionType%3AINCLUDED)))%2C(type%3ACURRENT_TITLE%2Cvalues%3AList((text%3A%25E2%2580%259Cfounder%25E2%2580%259D%2520OR%2520%2528%25E2%2580%259Cdirector%25E2%2580%259D%2520AND%2520%25E2%2580%259Ctechnology%25E2%2580%259D%2529%2520OR%2520%25E2%2580%259Cpresident%25E2%2580%259D%2520OR%2520%25E2%2580%259CCEO%25E2%2580%259D%2520OR%2520%25E2%2580%259Cchief%2520executive%2520officer%25E2%2580%259D%2520OR%2520%25E2%2580%259CCOO%25E2%2580%259D%2520OR%2520%25E2%2580%259Cchief%2520operations%2520officer%25E2%2580%259D%2520OR%2520%25E2%2580%259CCTO%25E2%2580%259D%2520OR%2520%25E2%2580%259Cchief%2520technology%2520officer%25E2%2580%259D%2520OR%2520%25E2%2580%259Cchief%2520information%2520officer%25E2%2580%259D%2520OR%2520%25E2%2580%259CCIO%25E2%2580%259D%2520OR%2520%25E2%2580%259CCSO%25E2%2580%259D%2520OR%2520%25E2%2580%259Cchief%2520strategy%2520officer%25E2%2580%259D%2520OR%2520%2528%25E2%2580%259Chead%25E2%2580%259D%2520AND%2520%25E2%2580%259Ce-commerce%25E2%2580%259D%2529%2CselectionType%3AINCLUDED)))))&sessionId=Jw%2BJm9jCTDC8NeUOv2pBoA%3D%3D")
        sales_navigator_query_3 = st.text_input("Sales Navigator query 3", "")
    elif option == "Onfleet (Resellers)":
        sales_navigator_query_1 = st.text_input("Sales Navigator query 1", "https://www.linkedin.com/sales/search/people?query=(recentSearchParam%3A(id%3A3036553874%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3ACURRENT_COMPANY%2Cvalues%3AList((id%3Aurn%253Ali%253Aorganization%253A18875652%2Ctext%3AAmperity%2CselectionType%3AINCLUDED%2Cparent%3A(id%3A0))))%2C(type%3ACURRENT_TITLE%2Cvalues%3AList((id%3A175%2Ctext%3AAccount%2520Director%2CselectionType%3AINCLUDED)%2C(id%3A20%2Ctext%3AAccount%2520Executive%2CselectionType%3AINCLUDED)%2C(id%3A11%2Ctext%3AAccount%2520Manager%2CselectionType%3AINCLUDED)%2C(text%3AAllience%2CselectionType%3AINCLUDED)%2C(text%3ABusiness%2520Development%2CselectionType%3AINCLUDED)%2C(text%3AClient%2520Service%2CselectionType%3AINCLUDED)%2C(text%3ACustomer%2520Servic%2CselectionType%3AINCLUDED)%2C(text%3ACustomer%2520Success%2CselectionType%3AINCLUDED)%2C(text%3ADigital%2520Transformation%2CselectionType%3AINCLUDED)%2C(id%3A8%2Ctext%3AChief%2520Executive%2520Officer%2CselectionType%3AINCLUDED)%2C(text%3AExpansion%2520Head%2CselectionType%3AINCLUDED)%2C(text%3AField%2520Director%2CselectionType%3AINCLUDED)%2C(id%3A68%2Ctext%3AChief%2520Financial%2520Officer%2CselectionType%3AINCLUDED)%2C(id%3A35%2Ctext%3AFounder%2CselectionType%3AINCLUDED)%2C(text%3AGrowth%2CselectionType%3AINCLUDED)%2C(text%3AImprementation%2CselectionType%3AINCLUDED)%2C(id%3A203%2Ctext%3AChief%2520Information%2520Officer%2CselectionType%3AINCLUDED)%2C(text%3AInnovation%2CselectionType%3AINCLUDED)%2C(id%3A716%2Ctext%3AChief%2520Marketing%2520Officer%2CselectionType%3AINCLUDED)%2C(id%3A280%2Ctext%3AChief%2520Operating%2520Officer%2CselectionType%3AINCLUDED)%2C(id%3A2498%2Ctext%3APartnerships%2520Manager%2CselectionType%3AINCLUDED)%2C(text%3APartner%2520Manager%2CselectionType%3AINCLUDED)%2C(text%3APartnership%2520Director%2CselectionType%3AINCLUDED)%2C(text%3APartnership%2520VP%2CselectionType%3AINCLUDED)%2C(text%3APresident%2CselectionType%3AINCLUDED)%2C(text%3AProject%2520Manager%2520Director%2CselectionType%3AINCLUDED)%2C(text%3ASales%2CselectionType%3AINCLUDED)%2C(text%3ASolutions%2520Director%2CselectionType%3AINCLUDED)%2C(text%3ASolutions%2520VP%2CselectionType%3AINCLUDED)%2C(id%3A153%2Ctext%3AChief%2520Technology%2520Officer%2CselectionType%3AINCLUDED)))))&sessionId=Ju%2BQuthBRZ2hTKtHpJWbXA%3D%3D")
        sales_navigator_query_2 = st.text_input("Sales Navigator query 2", "https://www.linkedin.com/sales/search/people?query=(spellCorrectionEnabled%3Atrue%2Cfilters%3AList((type%3ACURRENT_COMPANY%2Cvalues%3AList((id%3Aurn%253Ali%253Aorganization%253A18875652%2CselectionType%3AINCLUDED%2Cparent%3A(id%3A0)))))%2Ckeywords%3A%2522Partner%2522%2520OR%2520%2522Partnership%2522%2520OR%2520%2522Alliance%2522)&sessionId=SUMDe%2FzUTOqstT30yZXQvA%3D%3D")
        sales_navigator_query_3 = st.text_input("Sales Navigator query 3", "")
    elif option == "Headlight Solutions":
        sales_navigator_query_1 = st.text_input("Sales Navigator query 1", "https://www.linkedin.com/sales/search/people?query=(recentSearchParam%3A(id%3A2744797746%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3AREGION%2Cvalues%3AList((id%3A102221843%2Ctext%3AAm%25C3%25A9rica%2520del%2520Norte%2CselectionType%3AINCLUDED)))%2C(type%3ACURRENT_COMPANY%2Cvalues%3AList((id%3Aurn%253Ali%253Aorganization%253A18875652%2Ctext%3AUPS%2CselectionType%3AINCLUDED%2Cparent%3A(id%3A0))))%2C(type%3ACURRENT_TITLE%2Cvalues%3AList((text%3A%2528%25E2%2580%259Cdirector%25E2%2580%259D%2520AND%2520%2528%25E2%2580%259Cdigital%2520transformation%25E2%2580%259D%2520OR%2520%25E2%2580%259CIT%25E2%2580%259D%2520OR%2520%25E2%2580%259Cinformation%2520technology%25E2%2580%259D%2520OR%2520%25E2%2580%259Coperations%25E2%2580%259D%2520OR%2520%25E2%2580%259Ctechnology%2520transformation%25E2%2580%259D%2520OR%2520%25E2%2580%259Csupply%2520chain%25E2%2580%259D%2520OR%2520%25E2%2580%259Clast%2520mile%25E2%2580%259D%2520OR%2520%25E2%2580%259Clogistics%25E2%2580%259D%2520OR%2520%25E2%2580%259CTransportation%25E2%2580%259D%2520OR%2520%25E2%2580%259CLast%2520mile%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CWhite%2520Glove%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CSystems%25E2%2580%259D%2520OR%2520%25E2%2580%259CIntegrations%25E2%2580%259D%2520OR%2520%25E2%2580%259CProject%2520Management%25E2%2580%259D%2520OR%2520%25E2%2580%259CFleet%25E2%2580%259D%2520OR%2520%25E2%2580%259CFulfillment%25E2%2580%259D%2520OR%2520%25E2%2580%259CPurchasing%25E2%2580%259D%2520OR%2520%25E2%2580%259CCommodity%25E2%2580%259D%2529%2529%2CselectionType%3AINCLUDED)%2C(text%3A%2528%25E2%2580%259CHead%25E2%2580%259D%2520AND%2520%2528%25E2%2580%259Cdigital%2520transformation%25E2%2580%259D%2520OR%2520%25E2%2580%259CIT%25E2%2580%259D%2520OR%2520%25E2%2580%259Cinformation%2520technology%25E2%2580%259D%2520OR%2520%25E2%2580%259Coperations%25E2%2580%259D%2520OR%2520%25E2%2580%259Ctechnology%2520transformation%25E2%2580%259D%2520OR%2520%25E2%2580%259Csupply%2520chain%25E2%2580%259D%2520OR%2520%25E2%2580%259Clast%2520mile%25E2%2580%259D%2520OR%2520%25E2%2580%259Clogistics%25E2%2580%259D%2520OR%2520%25E2%2580%259CTransportation%25E2%2580%259D%2520OR%2520%25E2%2580%259CLast%2520mile%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CWhite%2520Glove%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CSystems%25E2%2580%259D%2520OR%2520%25E2%2580%259CIntegrations%25E2%2580%259D%2520OR%2520%25E2%2580%259CProject%2520Management%25E2%2580%259D%2520OR%2520%25E2%2580%259CFleet%25E2%2580%259D%2520OR%2520%25E2%2580%259CFulfillment%25E2%2580%259D%2520OR%2520%25E2%2580%259CPurchasing%25E2%2580%259D%2520OR%2520%25E2%2580%259CCommodity%25E2%2580%259D%2529%2529%2CselectionType%3AINCLUDED)%2C(text%3A%2528%25E2%2580%259CLead%25E2%2580%259D%2520AND%2520%2528%25E2%2580%259Cdigital%2520transformation%25E2%2580%259D%2520OR%2520%25E2%2580%259CIT%25E2%2580%259D%2520OR%2520%25E2%2580%259Cinformation%2520technology%25E2%2580%259D%2520OR%2520%25E2%2580%259Coperations%25E2%2580%259D%2520OR%2520%25E2%2580%259Ctechnology%2520transformation%25E2%2580%259D%2520OR%2520%25E2%2580%259Csupply%2520chain%25E2%2580%259D%2520OR%2520%25E2%2580%259Clast%2520mile%25E2%2580%259D%2520OR%2520%25E2%2580%259Clogistics%25E2%2580%259D%2520OR%2520%25E2%2580%259CTransportation%25E2%2580%259D%2520OR%2520%25E2%2580%259CLast%2520mile%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CWhite%2520Glove%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CSystems%25E2%2580%259D%2520OR%2520%25E2%2580%259CIntegrations%25E2%2580%259D%2520OR%2520%25E2%2580%259CProject%2520Management%25E2%2580%259D%2520OR%2520%25E2%2580%259CFleet%25E2%2580%259D%2520OR%2520%25E2%2580%259CFulfillment%25E2%2580%259D%2520OR%2520%25E2%2580%259CDispatch%25E2%2580%259D%2529%2529%2CselectionType%3AINCLUDED)%2C(text%3A%2528%25E2%2580%259CManager%25E2%2580%259D%2520AND%2520%2528%25E2%2580%259Cdigital%2520transformation%25E2%2580%259D%2520OR%2520%25E2%2580%259CIT%25E2%2580%259D%2520OR%2520%25E2%2580%259Cinformation%2520technology%25E2%2580%259D%2520OR%2520%25E2%2580%259Coperations%25E2%2580%259D%2520OR%2520%25E2%2580%259Ctechnology%2520transformation%25E2%2580%259D%2520OR%2520%25E2%2580%259Csupply%2520chain%25E2%2580%259D%2520OR%2520%25E2%2580%259Clast%2520mile%25E2%2580%259D%2520OR%2520%25E2%2580%259Clogistics%25E2%2580%259D%2520OR%2520%25E2%2580%259CTransportation%25E2%2580%259D%2520OR%2520%25E2%2580%259CLast%2520mile%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CWhite%2520Glove%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CSystems%25E2%2580%259D%2520OR%2520%25E2%2580%259CIntegrations%25E2%2580%259D%2520OR%2520%25E2%2580%259CProject%2520Management%25E2%2580%259D%2520OR%2520%25E2%2580%259CFleet%25E2%2580%259D%2520OR%2520%25E2%2580%259CFulfillment%25E2%2580%259D%2520OR%2520%25E2%2580%259CDelivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CPurchasing%25E2%2580%259D%2520OR%2520%25E2%2580%259CCommodity%25E2%2580%259D%2529%2529%2CselectionType%3AINCLUDED)%2C(text%3A%2528%25E2%2580%259CVP%25E2%2580%259D%2520AND%2520%2528%25E2%2580%259CIT%25E2%2580%259D%2520OR%2520%25E2%2580%259Cinformation%2520technology%25E2%2580%259D%2520OR%2520%25E2%2580%259Coperations%25E2%2580%259D%2520OR%2520%25E2%2580%259Ctechnology%2520transformation%25E2%2580%259D%2520OR%2520%25E2%2580%259Csupply%2520chain%25E2%2580%259D%2520OR%2520%25E2%2580%259Clogistics%25E2%2580%259D%2520OR%2520%25E2%2580%259CTransportation%25E2%2580%259D%2520OR%2520%25E2%2580%259CLast%2520mile%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CWhite%2520Glove%2520Delivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CSystems%25E2%2580%259D%2520OR%2520%25E2%2580%259CIntegrations%25E2%2580%259D%2520OR%2520%25E2%2580%259CProject%2520Management%25E2%2580%259D%2520OR%2520%25E2%2580%259CFleet%25E2%2580%259D%2520OR%2520%25E2%2580%259CFulfillment%25E2%2580%259D%2520OR%2520%25E2%2580%259CFinance%25E2%2580%259D%2520OR%2520%25E2%2580%259CPurchasing%25E2%2580%259D%2520OR%2520%25E2%2580%259CCommodity%25E2%2580%259D%2529%2529%2CselectionType%3AINCLUDED)%2C(text%3A%2528%2522Founder%2522%2520OR%2520%2522Cofounder%2522%2520OR%2520%2522Co-Founder%2522%2520OR%2520%2522CEO%2522%2520OR%2520%2522Chief%2520Executive%2520Officer%2522%2520OR%2520%2522C.E.O%2522%2520OR%2520%2522CFO%2522%2520OR%2520%2522Chief%2520Finance%2520Officer%2522%2520OR%2520%2522Chief%2520of%2520Finance%2522%2520OR%2520%2522C.F.O%2522%2520OR%2520%2522COO%2522%2520OR%2520%2522Chief%2520Operations%2520Officer%2522%2520OR%2520%2522Chief%2520of%2520Operations%2522%2520OR%2520%2522Chief%2520Operating%2520Officer%2522%2520OR%2520%2522C.O.O%2522%2520OR%2520%2522Chief%2520Supply%2520Chain%2522%2520OR%2520%2522Chief%2520Customer%2522%2529%2529%2CselectionType%3AINCLUDED)))))&sessionId=Jw%2BJm9jCTDC8NeUOv2pBoA%3D%3D")
        sales_navigator_query_2 = st.text_input("Sales Navigator query 2", "https://www.linkedin.com/sales/search/people?query=(recentSearchParam%3A(id%3A2744797746%2CdoLogHistory%3Atrue)%2Cfilters%3AList((type%3AREGION%2Cvalues%3AList((id%3A102221843%2Ctext%3AAm%25C3%25A9rica%2520del%2520Norte%2CselectionType%3AINCLUDED)))%2C(type%3ACURRENT_COMPANY%2Cvalues%3AList((id%3Aurn%253Ali%253Aorganization%253A18875652%2Ctext%3AUPS%2CselectionType%3AINCLUDED%2Cparent%3A(id%3A0))))%2C(type%3ACURRENT_TITLE%2Cvalues%3AList((text%3A%2528%25E2%2580%259CSupervisor%25E2%2580%259D%2520AND%2520%2528%25E2%2580%259CDispatch%25E2%2580%259D%2520OR%2520%25E2%2580%259CDriver%25E2%2580%259D%2520OR%2520%25E2%2580%259CFulfillment%25E2%2580%259D%2520OR%2520%25E2%2580%259CLogistics%25E2%2580%259D%2520OR%2520%25E2%2580%259COperations%25E2%2580%259D%2520OR%2520%25E2%2580%259CPurchasing%25E2%2580%259D%2520OR%2520%25E2%2580%259CCommodity%25E2%2580%259D%2520OR%2520%25E2%2580%259CSupply%2520Chain%25E2%2580%259D%2520OR%2520%25E2%2580%259CTransportation%25E2%2580%259D%2529%2529%2CselectionType%3AINCLUDED)%2C(text%3A%2528%25E2%2580%259CSpecialist%25E2%2580%259D%2520AND%2520%2528%25E2%2580%259CFulfillment%25E2%2580%259D%2520OR%2520%25E2%2580%259CLogistics%25E2%2580%259D%2520OR%2520%25E2%2580%259COperations%25E2%2580%259D%2520OR%2520%25E2%2580%259CTransportation%25E2%2580%259D%2520OR%2520%25E2%2580%259CSupply%2520Chain%25E2%2580%259D%2529%2529%2CselectionType%3AINCLUDED)%2C(text%3A%2528%25E2%2580%259CCoordinator%25E2%2580%259D%2520AND%2520%2528%25E2%2580%259CDelivery%25E2%2580%259D%2520OR%2520%25E2%2580%259CDispatch%25E2%2580%259D%2520OR%2520%25E2%2580%259CDriver%25E2%2580%259D%2520OR%2520%25E2%2580%259CFleet%25E2%2580%259D%2520OR%2520%25E2%2580%259CFulfillment%25E2%2580%259D%2520OR%2520%25E2%2580%259CLogistics%25E2%2580%259D%2520OR%2520%25E2%2580%259COperations%25E2%2580%259D%2520OR%2520%25E2%2580%259CPurchasing%25E2%2580%259D%2520OR%2520%25E2%2580%259CCommodity%25E2%2580%259D%2520OR%2520%25E2%2580%259CSupply%2520Chain%25E2%2580%259D%2520OR%2520%25E2%2580%259CTransportation%25E2%2580%259D%2529%2529%2CselectionType%3AINCLUDED)%2C(text%3A%2528%25E2%2580%259CTransportation%2520Consultant%25E2%2580%259D%2520OR%2520%25E2%2580%259CDispatcher%25E2%2580%259D%2520OR%2520%25E2%2580%259COperations%25E2%2580%259D%2529%2CselectionType%3AINCLUDED)))))&sessionId=Jw%2BJm9jCTDC8NeUOv2pBoA%3D%3D")
        sales_navigator_query_3 = st.text_input("Sales Navigator query 3", "")
    else:
        sales_navigator_query_1 = st.text_input("Sales Navigator query 1", "")
        sales_navigator_query_2 = st.text_input("Sales Navigator query 2", "")
        sales_navigator_query_3 = st.text_input("Sales Navigator query 3", "")

if option != "Select Client ICP":
    if not spreadsheet_url:
            st.error("Please fill spreadsheet URL.")
    if not sheet_name:
            st.error("Please fill sheet name.")
    if not column_name:
            st.error("Please fill column name.")
    if not li_at:
            st.error("Please fill LinkedIn authentication cookie.")
    else:
        if st.button("First step"):
            try:
                task_id = generate_task_id()
                payload = {
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name,
                    "column_name": column_name,
                    "li_at": li_at,
                    "sales_navigator_query_1": sales_navigator_query_1,
                    "sales_navigator_query_2": sales_navigator_query_2,
                    "sales_navigator_query_3": sales_navigator_query_3,
                    "key_dict": key_dict,
                    "task_id": task_id,
                }
                response = requests.post(
                    f"{base_request_url}/linkedin_scripts/linkedin_workflow/first_workflow_part", json=payload)
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
                                time.sleep(15)
                                st.success("First step completed!")
                                break
                        else:
                            st.error(f"Invalid progress data: {msg.data}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.exception(e)
        if st.button("Second step"):
            try:
                task_id = generate_task_id()
                spreadsheet_url, sheet_name, key_dict, li_at
                payload = {
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name,
                    "li_at": li_at,
                    "key_dict": key_dict,
                    "task_id": task_id,
                }
                response = requests.post(
                    f"{base_request_url}/linkedin_scripts/linkedin_workflow/second_workflow_part", json=payload)             
                if response.status_code == 200:
                    st.success(f"Task started. Task ID: {task_id}")
                    first_sse_url = f"{base_request_url}/progress_stream/first_{task_id}"
                    second_sse_url = f"{base_request_url}/progress_stream/second_{task_id}"
                    third_sse_url = f"{base_request_url}/progress_stream/third_{task_id}"
                    if sales_navigator_query_1 != "":
                        first_sse_url = f"{base_request_url}/progress_stream/first_{task_id}"
                        first_progress_bar = st.progress(0)
                    if sales_navigator_query_2 != "":
                        second_sse_url = f"{base_request_url}/progress_stream/second_{task_id}"
                        second_progress_bar = st.progress(0)
                    if sales_navigator_query_3 != "":
                        third_sse_url = f"{base_request_url}/progress_stream/third_{task_id}"
                        third_progress_bar = st.progress(0)                    
                    search_messages = sseclient.SSEClient(search_sse_url)
                    if sales_navigator_query_1 != "":
                        for msg in search_messages:
                            if msg.data and msg.data.strip().isdigit():
                                progress = int(msg.data)
                                first_progress_bar.progress(progress)
                                if progress == 100:
                                    st.success("Query 1 completed!")
                                    break
                            else:
                                st.error(
                                    f"Invalid progress data received: {msg.data}")
                    if sales_navigator_query_2 != "":
                        for msg in search_messages:
                            if msg.data and msg.data.strip().isdigit():
                                progress = int(msg.data)
                                second_progress_bar.progress(progress)
                                if progress == 100:
                                    st.success("Query 2 completed!")
                                    break
                            else:
                                st.error(
                                    f"Invalid progress data received: {msg.data}")
                    if sales_navigator_query_3 != "":
                        for msg in search_messages:
                            if msg.data and msg.data.strip().isdigit():
                                progress = int(msg.data)
                                third_progress_bar.progress(progress)
                                if progress == 100:
                                    st.success("Query 3 completed!")
                                    break
                        else:
                            st.error(
                                f"Invalid progress data received: {msg.data}")
                else:
                    st.error(
                        f"Error starting task: {response.json().get('message')}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.exception(e)
        if st.button("Third step"):
            try:
                task_id = generate_task_id()
                payload = {
                    "spreadsheet_url": spreadsheet_url,
                    "sheet_name": sheet_name,
                    "li_at": li_at,
                    "key_dict": key_dict,
                    "task_id": task_id,
                }
                response = requests.post(
                    f"{base_request_url}/linkedin_scripts/linkedin_workflow/third_workflow_part", json=payload)
                if response.status_code == 200:
                    st.success(f"Task started. Task ID: {task_id}")
                    time.sleep(15)
                    st.success("Third step completed!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.exception(e)
