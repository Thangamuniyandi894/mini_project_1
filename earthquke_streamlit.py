
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:gold90038%40@localhost:3306/global_seismic_trends')


queries = {
    "1.Top 10 strongest earthquakes (mag).": """select * from earthquakes 
order by mag desc 
limit 10;""",

    "2. Top 10 deepest earthquakes (depth_km)": """SELECT * FROM earthquakes 
ORDER BY depth_km DESC 
LIMIT 10;""",
    "3. Shallow earthquakes < 50 km and mag > 7.5.": """select * from earthquakes 
where depth_km < 50 and mag > 7.5;""",
   
    "4. Average magnitude per magnitude type (magType).": """select magType, avg(mag) as avg_magnitude 
from earthquakes 
group by magType;""",

    "5. Year with most earthquakes.": """select year,count(*) as total_counts
from earthquakes 
group by year 
order by total_counts desc
limit 1;""",

    "6. Month with highest number of earthquakes.": """select month,count(*) AS total_counts
from earthquakes 
group by month
order by total_counts DESC 
limit 1;""",

    "7. Day of week with most earthquakes.": """select day_of_week,count(*) as total_earthquakes 
from earthquakes 
group by day_of_week 
order by total_earthquakes desc
limit 1;""",

    "8. Count of earthquakes per hour of day.": """select hour,count(*) AS total_counts
from earthquakes 
group by hour 
order by total_counts;""",

    "9.   Most active reporting network (net).": """select net, count(*) as total_reports 
from earthquakes 
group by net 
order by total_reports desc
limit 1;""",

    "10.  Top 5 places with highest casualties.": """select place, max(sig) as max_impact
from earthquakes 
group by place 
order by max_impact desc
limit 5;""",
   
    "11.  Average economic loss by alert level.": """select alert,avg(sig) as  avg_impact
from earthquakes 
group by alert;""",

    "12.  Count of reviewed vs automatic earthquakes (status).": """select status, count(*) as total_count 
from earthquakes 
group by status;""",

    "13.  Count by earthquake type (type).": """select type, count(*) as total_count 
from earthquakes 
group by type;""",

    "14.  Number of earthquakes by data type (types).": """select types, count(*) as total_count 
from earthquakes 
group by types;""",
    
    "15.  Events with high station coverage (nst > threshold).": """select * from earthquakes 
where nst > 100 
order by nst desc 
limit 5;""",

    "16.  Number of tsunamis triggered per year.": """select year,count(*)  as tsunami_count 
from earthquakes 
where tsunami = 1
group by year;""",

    "17.  Count earthquakes by alert levels (red, orange, etc.).": """select alert, count(*) as total_count 
from earthquakes 
group by alert;""",

    "18.Find the top 5 countries with the highest average magnitude of earthquakes in thepast 5 years":"""select country, avg(mag) as avg_mag 
from earthquakes 
where year>=(select max(year)-5 from earthquakes)
group by country
order by avg_mag desc 
limit 5;""" ,

    "19.Find countries that have experienced both shallow and deep earthquakes within the same month.": 
    """select country, year,month 
from earthquakes 
group by country, year, month 
having sum(case when depth_km< 70 then 1 else 0 end) > 0 
and sum(case when depth_km > 300 then 1 else 0 end) > 0;""",

    "20.Compute the year-over-year growth rate in the total number of earthquakes globally.":
      """with yearlycounts as (
    select year as eq_year, count(*) as total_eq 
    from earthquakes 
    group by year
)
select eq_year, total_eq,
    lag(total_eq) over (order by eq_year) as prev_year_total,
    round(((total_eq - lag(total_eq) over (order by eq_year)) / lag(total_eq) over (order by eq_year)) * 100, 2) as yoy_growth_percent
from yearlyCounts;""",

    "	21. List the 3 most seismically active regions by combining both frequency and average magnitude.": """select place, count(*) as frequency, avg(mag) as avg_mag 
from earthquakes 
group by place 
order by (count(*) * avg(mag)) desc 
limit 3;""",

    "  22. For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator.": 
    """select country, avg(depth_km) as avg_depth 
from earthquakes 
where latitude between -5 and 5 
group by country;""",

    "23. Identify countries having the highest ratio of shallow to deep earthquakes.": """select country, 
    sum(case when depth_km < 70 then 1 else 0 end) / 
    nullif(sum(case when depth_km > 300 then 1 else 0 end), 0) as shallow_to_deep_ratio 
from earthquakes 
group by country 
order by shallow_to_deep_ratio desc;""",
        
    "  24. Find the average magnitude difference between earthquakes with tsunami alerts and those without.":
      """select (select avg(mag) from earthquakes where tsunami=1)-(
select avg(mag) from earthquakes where tsunami=0) as avg_magnitude_diff;""",

    "25. Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins).":
    """select *, (gap + rms) as total_error_margin 
from earthquakes 
order by total_error_margin desc 
limit 10;""",
   
    "26. Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km).":
      """select place, count(*) as deep_earthquake_count 
from earthquakes 
where depth_km > 300 
group by place 
order by deep_earthquake_count desc;"""
}


#  Sidebar Dropdown Filter
st.sidebar.header("QUESTIONS:")
selected_question = st.sidebar.selectbox("Select a question:", list(queries.keys()))

# quary excution and results
sql_query = queries[selected_question]

st.subheader(selected_question)

# sql code
with st.expander("Displaying SQL Code"):
    st.code(sql_query, language="sql")


# display the rresult
try:
    with engine.connect() as conn:
        df = pd.read_sql(sql_query, conn)
    st.write(f"*Total Rows (Rows):* {len(df)}")
    st.dataframe(df)

except Exception as e:
    st.error(f"Error Occured: {e}")