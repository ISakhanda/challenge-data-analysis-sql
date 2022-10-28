# %%
import sqlite3
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt



connexion = sqlite3.connect("data/bce.db")
cursor = connexion.cursor()

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
        enterprise.JuridicalForm IS NOT NULL AND
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

labels = df_juridicalform['CodeDescription']
sizes = df_juridicalform['CountByGroupBy']

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')
ax1.set_title("Question 1 : Which percentage of the companies are under which juridical form?")

st.pyplot(fig1)

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
        enterprise.Status IS NOT NULL AND
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

labels = df_status['CodeDescription']
sizes = df_status['CountByGroupBy']

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')

ax1.set_title("Question 2 : Which percentage of the companies are under which Status?")

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

labels = df_typeof['CodeDescription']
sizes = df_typeof['CountByGroupBy']

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')
ax1.set_title("Question 3 : Which percentage of the companies are which type of entreprise?")


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
df_NACE

# %%

source = pd.DataFrame({
    'Average age start': df_NACE['AverageStartDate'],
    'Sector subcategroy': df_NACE['DescriptionCode']
    })

# bar_chart = alt.Chart(source).mark_bar().encode(
#     y='Average age start',
#     x='Sector subcategroy',
# )

st.altair_chart(source, use_container_width=True)


