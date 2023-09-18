import pandas as pd
import plotly as px
import streamlit as st
# Import csv
vg_sales = pd.read_csv(r"vgsales.csv")

# Data Transforms
## Rename columns
vg_sales = vg_sales.rename(columns={
    "NA_Sales": "North America Sales", 
    "EU_Sales": "EU Sales", 
    "JP_Sales": "Japan Sales", 
    "Other_Sales": "Other Sales", 
    "Global_Sales": "Global Sales"
    })
## Change date to correct type
vg_sales["Year"] = pd.to_datetime(vg_sales.Year, format="%Y")
## 2017 and 2020 contain incomplete data for platforms and are therefore removed
vg_clean = vg_sales[~vg_sales.Year.isin([2017, 2020])].copy()
## Create column mapping platform to company that manafactured that platform
platforms_to_company = {
    "Wii": "Nintendo",
    "NES": "Nintendo",
    "GB": "Nintendo",
    "DS": "Nintendo",
    "X360": "Microsoft",
    "PS3": "Sony",
    "PS2": "Sony",
    "SNES": "Nintendo",
    "GBA": "Nintendo",
    "3DS": "Nintendo",
    "PS4": "Sony",
    "N64": "Nintendo",
    "PS": "Sony",
    "XB": "Microsoft",
    "PC": "All PCs",
    "2600": "Atari",
    "PSP": "Sony",
    "XOne": "Microsoft",
    "GC": "Nintendo",
    "WiiU": "Nintendo",
    "GEN": "Sega",
    "DC": "Sega",
    "PSV": "Sony",
    "SAT": "Sega",
    "SCD": "Sega",
    "WS": "Bandai",
    "NG": "SNK",
    "TG16": "NEC",
    "3DO": "Panasonic",
    "GG": "Sega",
    "PCFX": "NEC"
}
vg_clean["Company"] = vg_clean.Platform.map(platforms_to_company)

# Build app
st.title("Video Game Company Analysis")
st.markdown("""This dashboard plots data pertaining to video games sales in 
            North America, the EU and Japan between the years 1980 and 2016. 
            """)
st.markdown("""Data was sourced from the following kaggle dataset:
            https://www.kaggle.com/datasets/gregorut/videogamesales""")
st.markdown("""Please use the filters on the left pain of the page to filter 
            the data. Filter by both regional sales and games platform manufacturers""")

## Create region filter
region_select = st.sidebar.selectbox("Filter by region", ["North America Sales", "EU Sales", "Japan Sales", "Other Sales", "Global Sales"])

## Create company filter
st.sidebar.write("Filter by company:")
Nintendo = st.sidebar.checkbox("Nintendo")
Microsoft = st.sidebar.checkbox("Microsoft")
Sony = st.sidebar.checkbox("Sony")
All_PCs = st.sidebar.checkbox("All PCs")
Atari = st.sidebar.checkbox("Atari")
Sega = st.sidebar.checkbox("Sega")
Bandai = st.sidebar.checkbox("Bandai")
SNK = st.sidebar.checkbox("SNK")
NEC = st.sidebar.checkbox("NEC")
Panasonic = st.sidebar.checkbox("Panasonic")
company_filter_all = {
    "Nintendo":Nintendo,
    "Microsoft":Microsoft,
    "Sony": Sony,
    "All PCs": All_PCs,
    "Atari": Atari,
    "Sega":Sega,
    "Bandai":Bandai,
    "SNK":SNK,
    "NEC":NEC,
    "Panasonic":Panasonic
    }

## Filter vg_clean to include only user selected companies
company_selected = [comp for comp in company_filter_all if company_filter_all[comp]==True]
vg_company_filtered = vg_clean[vg_clean.Company.isin(company_selected)]

## Plot timeseries of sales
st.markdown("### Time Series of Video Game Sales (millions of units sold)")
vg_group_line = vg_company_filtered.groupby(["Company", "Year"], as_index=False).sum()
fig = px.express.line(vg_group_line, x="Year", y=region_select, color="Company")
st.plotly_chart(fig, use_container_width=True)

## Plot genre bar graph
st.markdown("### Game Sales by Genre (millions of units sold)")
vg_group_bar = vg_company_filtered.groupby(["Genre", "Company"], as_index=False).sum()[["Genre", region_select, "Company"]]
st.bar_chart(vg_group_bar, x="Genre", y=region_select, color="Company")

## Plot metircs of most sold video games by company
st.markdown("### Most Popular Games")
vg_group_metric = vg_company_filtered.groupby(["Company"], as_index=False).agg({"Name": "first", "Platform": "first", region_select: max})
company_subset = vg_group_metric.Company.unique()
col1, col2 = st.columns(2)
for n in range(len(company_subset)):
    company = company_subset[n]
    company_row = vg_group_metric[vg_group_metric.Company == company]
    if n%2 == 0:
        col1.metric(company, company_row["Name"].values[0])
    else:
        col2.metric(company, company_row["Name"].values[0])
