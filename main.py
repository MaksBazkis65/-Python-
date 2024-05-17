import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.worldometers.info/coronavirus/'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

def get_country_data(country_name):
    table = soup.find('table', id='main_table_countries_today')
    rows = table.tbody.find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        country = cols[1].text.strip()
        if country.lower() == country_name.lower():
            data = {
                'Country': country,
                'Total Cases': cols[2].text.strip().replace(',', ''),
                'New Cases': cols[3].text.strip().replace(',', '').replace('+', ''),
                'Total Deaths': cols[4].text.strip().replace(',', ''),
                'New Deaths': cols[5].text.strip().replace(',', '').replace('+', ''),
                'Total Recovered': cols[6].text.strip().replace(',', ''),
                'Active Cases': cols[8].text.strip().replace(',', ''),
                'Serious, Critical': cols[9].text.strip().replace(',', ''),
                'Total Cases/1M pop': cols[10].text.strip().replace(',', ''),
                'Deaths/1M pop': cols[11].text.strip().replace(',', ''),
                'Total Tests': cols[12].text.strip().replace(',', ''),
                'Tests/1M pop': cols[13].text.strip().replace(',', ''),
                'Population': cols[14].text.strip().replace(',', '')
            }
            return data
    return None

countries = ['USA', 'Japan']
data = []

for country in countries:
    country_data = get_country_data(country)
    if country_data:
        data.append(country_data)

df = pd.DataFrame(data)
print("Parsed Data:")
print(df)

df['Total Cases'] = pd.to_numeric(df['Total Cases'], errors='coerce')
df['New Cases'] = pd.to_numeric(df['New Cases'], errors='coerce')
df['Total Deaths'] = pd.to_numeric(df['Total Deaths'], errors='coerce')
df['New Deaths'] = pd.to_numeric(df['New Deaths'], errors='coerce')
df['Total Recovered'] = pd.to_numeric(df['Total Recovered'], errors='coerce')
df['Active Cases'] = pd.to_numeric(df['Active Cases'], errors='coerce')
df['Serious, Critical'] = pd.to_numeric(df['Serious, Critical'], errors='coerce')
df['Total Cases/1M pop'] = pd.to_numeric(df['Total Cases/1M pop'], errors='coerce')
df['Deaths/1M pop'] = pd.to_numeric(df['Deaths/1M pop'], errors='coerce')
df['Total Tests'] = pd.to_numeric(df['Total Tests'], errors='coerce')
df['Tests/1M pop'] = pd.to_numeric(df['Tests/1M pop'], errors='coerce')
df['Population'] = pd.to_numeric(df['Population'], errors='coerce')

print("\nQuantitative Characteristics:")
print(df.describe())

print("\nTable Headers:")
print(df.columns)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nData Types:")
print(df.dtypes)

# Видалення зайвих полів (для цього прикладу залишимо всі поля)
# df = df.drop(columns=['Column_to_remove'])

# Заповнення або видалення відсутніх даних
df = df.fillna(0)

# Переіменування стовпців (залишимо без змін у цьому прикладі)
# df.rename(columns={'Old_Name': 'New_Name'}, inplace=True)

# Вивід очищених даних
print("\nCleaned Data:")
print(df)

# Додавання розрахункових стовпчиків
df['Death Rate'] = (df['Total Deaths'] / df['Total Cases']) * 100
df['Recovery Rate'] = (df['Total Recovered'] / df['Total Cases']) * 100

# Групування та сортування (для цього прикладу не застосовується, оскільки всього 2 країни)
# df_grouped = df.groupby('Some_Column').sum()
df_sorted = df.sort_values(by='Total Cases', ascending=False)

# Вивід результатів розрахунків
print("\nCalculated Data:")
print(df_sorted)

import matplotlib.pyplot as plt
import seaborn as sns

# Візуалізація загальної кількості випадків
plt.figure(figsize=(10, 6))
sns.barplot(x='Country', y='Total Cases', data=df_sorted)
plt.title('Total Cases by Country')
plt.show()

# Візуалізація кількості смертей
plt.figure(figsize=(10, 6))
sns.barplot(x='Country', y='Total Deaths', data=df_sorted)
plt.title('Total Deaths by Country')
plt.show()

# Візуалізація рівня смертності
plt.figure(figsize=(10, 6))
sns.barplot(x='Country', y='Death Rate', data=df_sorted)
plt.title('Death Rate by Country')
plt.show()

# Візуалізація кількості тестів
plt.figure(figsize=(10, 6))
sns.barplot(x='Country', y='Total Tests', data=df_sorted)
plt.title('Total Tests by Country')
plt.show()

# Візуалізація активних випадків
plt.figure(figsize=(10, 6))
sns.barplot(x='Country', y='Active Cases', data=df_sorted)
plt.title('Active Cases by Country')
plt.show()

# Візуалізація серйозних/критичних випадків
plt.figure(figsize=(10, 6))
sns.barplot(x='Country', y='Serious, Critical', data=df_sorted)
plt.title('Serious, Critical Cases by Country')
plt.show()
