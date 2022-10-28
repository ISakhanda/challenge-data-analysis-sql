# %%
import sqlite3
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np



connexion = sqlite3.connect("data/bce.db")
cursor = connexion.cursor()

# %%
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Question 1", "Question 2", "Question 3", "Question 4", "Extra question"])






# %% [markdown]
# # Which percentage of the companies are under which juridical form?

# %% [markdown]
# ### First step : GROUP BY Juridical Form

# %%
query1 = f"""
    SELECT 
        enterprise.JuridicalForm, count(*)
    FROM 
        enterprise
    WHERE 
        enterprise.JuridicalForm IS NOT NULL
    GROUP BY
        enterprise.JuridicalForm

    LIMIT 10;   
"""        

cursor.execute(query1)
cursor.fetchall()

# %% [markdown]
# ### Second step : Find the SUM of all enterprises

# %%
query2 = f"""
    SELECT 
        count(enterprise.JuridicalForm)
    FROM 
        enterprise

"""        

cursor.execute(query2)
cursor.fetchall()

# %% [markdown]
# ### Third Step : Percentage

# %%
query3 = f"""
    SELECT
        enterprise.JuridicalForm,
        COUNT(enterprise.JuridicalForm) as 'Count by juridical form',
        COUNT(enterprise.JuridicalForm) / (SELECT COUNT(enterprise.JuridicalForm) FROM enterprise) * 100.0 as 'Percentage'
    FROM 
        enterprise
    WHERE 
        enterprise.JuridicalForm IS NOT NULL
    GROUP BY
        enterprise.JuridicalForm
    ;   
"""        

cursor.execute(query3)
cursor.fetchall()

# %% [markdown]
# ### Extract JuridicalForm Code and French Description string

# %%
query4 = f"""
    SELECT
        code.Code as 'Code',
        code.Description as 'Description'
    FROM 
        code
    WHERE
        code.Category is "JuridicalForm" AND
        code.Language is "FR"
        ;
     """
     
cursor.execute(query4)
cursor.fetchall()



# %% [markdown]
# ### Replace JuridicalForm code by the french Description of the Code

# %%
# SELECT 
# FROM 
# INNER JOIN 
# WHERE 
# GROUP BY

query6 = f"""
    SELECT
        enterprise.JuridicalForm as 'CodeOfJuridicalForm',
        code.Description as 'CodeDescription',
        COUNT(*) as 'CountByGroupBy'
          
    FROM
        enterprise
                        
    INNER JOIN
        code ON enterprise.JuridicalForm = code.Code

    WHERE
        code.Category = 'JuridicalForm' AND
        code.Language = 'FR'        
        
    GROUP BY
        enterprise.JuridicalForm
        
    ORDER BY
        CountByGroupBy DESC
                
    LIMIT 40
    ;  
        
        """
        
cursor.execute(query6)
cursor.fetchall()

# %% [markdown]
# ### Define the DataFrame

# %%
df_juridicalform = pd.read_sql_query(query6, connexion)

# %% [markdown]
# ### First Pie Chart

# %%
# st.write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame(df))
with tab1:
    st.header("Question 1 : Which percentage of the companies are under which juridical form?")

    labels = df_juridicalform['CodeDescription']
    sizes = df_juridicalform['CountByGroupBy']

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')

    st.pyplot(fig1)


    code_descrption = list(df_juridicalform['CodeDescription'])
    count = list(df_juridicalform['CountByGroupBy'])

    fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(code_descrption, count, color ='blue', width = 0.4)
    
    plt.xlabel("Juridical Form")
    plt.ylabel("Numbers of enterprises")
    plt.xticks(rotation=90)
    
  
    
    # arr = sizes
    # fig, ax = plt.subplots()
    # ax.hist2d(x = labels, y = arr, bins=20)

    st.pyplot(fig)
# %% [markdown]
# # Which percentage of the companies are under which Status?

# %%
# SELECT 
# FROM 
# INNER JOIN 
# WHERE 
# GROUP BY

query7 = f"""
    SELECT
        enterprise.Status as 'Status',
        code.Description as 'CodeDescription',
        COUNT(*) as 'CountByGroupBy'
          
    FROM
        enterprise
                        
    INNER JOIN
        code ON enterprise.Status = code.Code

    WHERE
        code.Category = 'Status' AND
        code.Language = 'FR'        
        
    GROUP BY
        enterprise.Status
        
    ORDER BY
        CountByGroupBy DESC
                
    LIMIT 40
    ;  
        
        """
        
cursor.execute(query7)
cursor.fetchall()

# %%
df_status = pd.read_sql_query(query7, connexion)

with tab2:
    st.header("Question 2 : Which percentage of the companies are under which Status?")

    labels = df_status['CodeDescription']
    sizes = df_status['CountByGroupBy']

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')


    st.pyplot(fig1)

# %% [markdown]
# # Which percentage of the companies are which type of entreprise?

# %%
# SELECT 
# FROM 
# INNER JOIN 
# WHERE 
# GROUP BY

query8 = f"""
    SELECT
        enterprise.TypeOfEnterprise as 'TypeOfEnterprise',
        code.Description as 'CodeDescription',
        COUNT(*) as 'CountByGroupBy'
          
    FROM
        enterprise
                        
    INNER JOIN
        code ON enterprise.TypeOfEnterprise = code.Code

    WHERE
        code.Category = 'TypeOfEnterprise' AND
        code.Language = 'FR'        
        
    GROUP BY
        enterprise.TypeOfEnterprise
        
    ORDER BY
        CountByGroupBy DESC
                
    LIMIT 40
    ;  
        
        """
        
cursor.execute(query8)
cursor.fetchall()

# %%
df_typeof = pd.read_sql_query(query8, connexion)


with tab3:
    st.header("Question 3 : Which percentage of the companies are which type of entreprise?")
    
    labels = df_typeof['CodeDescription']
    sizes = df_typeof['CountByGroupBy']

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')


    st.pyplot(fig1)

# %% [markdown]
# # What is the average company's age in each sector (hint: look what is the NACE code)?

# %%
import sqlite3
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt



connexion = sqlite3.connect("data/bce.db")
cursor = connexion.cursor()

# SELECT 
# FROM 
# INNER JOIN 
# WHERE 
# GROUP BY

# select code.Code, code.Category, code.Description  from code where code.Category = "Nace2008"
# select activity.EntityNumber, activity.NaceCode from activity
# select enterprise.Number, enterprise.StartDate from enterprise

# STRFTIME('%d/%m/%Y, %H:%M', sale_datetime)


query9 = f"""
    SELECT
        enterprise.EnterpriseNumber as 'EnterpriseNumber',
        SUBSTR(activity.NaceCode, 1, 2) as 'NaceCode',
        code.Description as 'DescriptionCode',
        ROUND(AVG(STRFTIME('%Y', enterprise.StartDate))) as 'AverageStartDate',
        COUNT(*) as 'CountByGroupBy'
          
    FROM
        enterprise
                        
    INNER JOIN
        code ON NaceCode = code.Code,
        activity ON enterprise.EnterpriseNumber = activity.EntityNumber

    WHERE
        code.Category = 'Nace2008' AND
        code.Language = 'FR' AND
        activity.NaceVersion = '2008'   

    GROUP BY
        SUBSTR(activity.NaceCode, 1, 2)
                
    ORDER BY
        CountByGroupBy DESC
    ;  
        
        """
        
cursor.execute(query9)
cursor.fetchall()

df_NACE = pd.read_sql_query(query9, connexion)

# %%
df_NACE = df_NACE.drop(['EnterpriseNumber'], axis=1)
df_NACE['AverageStartDate'] = df_NACE['AverageStartDate'].astype(int)
# df_NACE

# %%

with tab4:
    st.header("Question 4 : What is the average company's age in each sector (hint: look what is the NACE code)?")
    
    nacecode = list(df_NACE['NaceCode'].drop_duplicates())
    averagestratdate = list(df_NACE['AverageStartDate'].drop_duplicates())
    
    nacecode_choice = st.selectbox('Choose the NACE code:', nacecode)
    
    # df_NACE = df_NACE[df_NACE['NaceCode'].isin(nacecode_choice)]
    # df_NACE = df_NACE[df_NACE['AverageStartDate'].isin(averagestratdate_choice)]
    data = df_NACE[df_NACE['NaceCode'].isin([nacecode_choice])]
    st.dataframe(data)
    
    st.markdown("Complete dataframe")
    st.dataframe(df_NACE.sort_values('NaceCode', ascending=False).reset_index(drop=True))

    
    # chart = plt.bar(df_NACE['NaceCode'],df_NACE['AverageStartDate'],color = ['#F0F8FF','#E6E6FA','#B0E0E6']) 
    # #Adding the aesthetics
    # plt.title('Chart title')
    # plt.xlabel('NaceCode')
    # plt.ylabel('Average start date') 
    # #Show the plot
    # st.pyplot(chart)
    

with tab5:
    st.header("Extra question : From where come the enterprises ?")
    
    world_country = pd.read_csv('world_country_and_usa_states_latitude_and_longitude_values.csv')
    code_country_latitude =world_country[["country_code","latitude", "longitude"]]
    colnames = ["zero", "first", "codecountry","code", "country", "countryeng"]
    sql_pays = pd.read_csv('sql-pays.csv',names = colnames, header= None)
    code_country =sql_pays[["codecountry","country"]]
    

    cursor.execute('CREATE TABLE IF NOT EXISTS code_country (codecountry, country)')
    connexion.commit()
    code_country_sql = code_country.to_sql('code_country',connexion, if_exists='replace', index = False)
    code_country_sql
    cursor.execute('''
    SELECT * FROM code_country
                ''')
    for row in cursor.fetchall():
        print (row)


    # %%
    cursor.execute('CREATE TABLE IF NOT EXISTS coordinates (country_code, latitude, longitude)')
    connexion.commit()
    
    country_latitude_sql = code_country_latitude.to_sql('coordinates',connexion, if_exists='replace', index = False)
    
    cursor.execute('''
    SELECT * FROM coordinates
                ''')
    for row in cursor.fetchall():
        print (row) 
        

    querty10 = f"""
    SELECT 
        country, 
        latitude, 
        longitude
    FROM 
        code_country
    INNER JOIN 
        coordinates ON code_country.codecountry=coordinates.country_code
        ;
    """


    cursor.execute(querty10)
    cursor.fetchall()
    df_lonlat = pd.read_sql_query(querty10, connexion)

    df_lonlat = df_lonlat.rename(columns={"country":"CountryFR"})


    querty12 = f"""
        SELECT 
            address.CountryFR, count(*)
        FROM 
            address
        WHERE 
            address.CountryFR IS NOT NULL
        GROUP BY
            address.CountryFR;  
    """        


    cursor.execute(querty12)
    cursor.fetchall()
    df_company_by_country = pd.read_sql_query(querty12, connexion)
 


    df_map = pd.concat([df_lonlat.set_index('CountryFR'),df_company_by_country.set_index('CountryFR')], axis=1, join='inner')#sre.reset_index()
    st.map(df_map[['latitude', 'longitude']])



