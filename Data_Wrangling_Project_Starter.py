#!/usr/bin/env python
# coding: utf-8

# # Real-world Data Wrangling

# In[1]:


# !python -m pip install kaggle==1.6.14


# In[2]:


# !pip install --target=/workspace ucimlrepo


# In[3]:


#imports
import pandas as pd
import numpy as np
import zipfile
import os
import json
import matplotlib.pyplot as plt


# ## 1. Gather data
# 
# 

# ### **1.1.** Problem Statement
# 

# 
# 
# ⁤The Movies Database dataset contains two datasets: one has titles and related details of nearly 5,000 different movies, and another lists the credits for each movie for the same set. ⁤⁤The goal of this project is to **identify trends in movie production over the years** and **Identify the film team members who have received 100 rating and above**. ⁤⁤We will use data-wrangling techniques to leverage the data to answer these questions in detail. The reason for the selection of this particular dataset is that it contains many unique variables to analyze the movie industry.

# ### **1.2.** Gather at least two datasets using two different data gathering methods
# 

# #### **tmdb_5000_credits**
# 
# Type: CSV File
# 
# 
# Method: Data was gathered using the "Download data manually" method from Kaggle.
# 
# Dataset variables:
# 
# *   **movie_id**: Unique identfier for movie.
# *   **title**: Movie name.
# *   **cast**: Individual cast member's details.
# *   **crew**: Crew member associated with a particular film.

# In[4]:


#Download data manually
Credits= pd.read_csv("tmdb_5000_credits.csv")


# #### tmdb_5000_movies
# 
# Type: CSV File
# 
# Method: Programmatically downloading files from Kaggle.
# 
# Dataset variables:
# 
# *   **budget**: Budget of the movie.
# *   **genres**: Genres that the movie contains.
# *   **homepage**: Movie's webpage.
# *   **id**: Unique identifier for the movie.
# *   **keywords**: Search terms regarding the movie.
# *   **original_language**: The movie's original language was officially released.
# *   **original_title**: The movie's name was officially published. 
# *   **overview**: A reflection of the film's story. 
# *   **popularity**: Popularity scale.
# *   **production_companies**: Company that had produced the movie.
# *   **production_countries**: Country where the movie was produced.
# *   **release_date**: Date of release of the movie.
# *   **revenue**: Revenue earned from the movie.
# *   **runtime**:  length of the movie in minutes.
# *   **spoken_languages**: Language spoken in the movie.
# *   **status**: Stages in a film's production lifecycle.
# *   **tagline**: A memorable phrase used to capture the tone and idea of the film.
# *   **title**: The movie's title.
# *   **vote_average**: Average number of votes for the film.
# *   **vote_counte**: The total number of votes cast for the movie.
# 
# 
# 
# 
# 
# 
#  

# In[5]:


#Download data from kaggle
get_ipython().system('kaggle datasets download -d tmdb/tmdb-movie-metadata --file tmdb_5000_movies.csv --force')

# # extract files
with zipfile.ZipFile('tmdb_5000_movies.csv.zip', 'r') as zip_ref:
    
    #  extracts all
    
    zip_ref.extractall()

# Load csv file
movies = pd.read_csv('tmdb_5000_movies.csv')


#  ### Data storing step  

# In[6]:


#store the raw data in local data store
#Already read the credits dataframe so no need to read again

#Making backup dataframe before cleaning
movies.to_csv('local_tmdb_5000_movies.csv', index=False)
Credits.to_csv('local_tmdb_5000_credits.csv', index=False)




# ## 2. Assess data
# 
# 

# ### Quality Issue 1:

# In[7]:


#  Inspecting the dataframe visually
movies.sample(55)


# In[8]:


#Inspecting the dataframe programmatically
# Check for NaN, None, or empty strings
missing_or_empty_budget = movies['budget'].apply(lambda x: x == 0)
missing_or_empty_revenue = movies['revenue'].apply(lambda x: x == 0)

#print number of missing budget,revenue values 
missing_or_empty_budget.sum(),missing_or_empty_revenue.sum()


# ### Completeness issues: We observe that not all movies have "budget" and "revenue" information for confirmation, we apply the lambda function to the total number of missing values.

# ### Quality Issue 2:

# In[9]:


#Inspecting the dataframe visually
#sample columns 
movies.sample(55)


# In[10]:


#Inspecting the dataframe programmatically
#get information about the datatype of each column
movies.info()


# ### Validity issue:"release_date" is not in the correct data type "Date", we used the .info to get the datatype for each column.

# ### Tidiness Issue 1:

# In[11]:


#Inspecting the dataframe visually
Credits["crew"]


# In[12]:


#Inspecting the dataframe programmatically
Credits['crew'] = Credits['crew'].apply(json.loads)

# Inspect the first few rows again to see the changes

# # Inspect the JSON data in the 'crew' column
for index, row in Credits.iterrows():
    print(f"\nRow {index + 1} crew data:")
    for member in row['crew']:
        for key, value in member.items():
            print(f"  {key}: {value}")
            
# print("\nFirst row crew data:", first_row_crew)

first_member_name = Credits.loc[0, 'crew'][0]['name']
print("First member's name in the first row crew:", first_member_name)


# ### Completeness issue: It is challenging to identify the crew members for each movie individually. We plan to create a list for each film that includes all of its crew members.

# ### Tidiness Issue 2: 

# In[13]:


#Inspecting the dataframe visually
Credits["crew"]


# In[14]:


#Inspecting the dataframe programmatically

Credits['cast'] = Credits['cast'].apply(json.loads)


# # Inspect the JSON data in the 'crew' column
for index, row in Credits.iterrows():
    print(f"\nRow {index + 1} crew data:")
    for member in row['cast']:
        for key, value in member.items():
            print(f"  {key}: {value}")
first_member_name = Credits.loc[0, 'cast'][0]['character']
print("First member's name in the first row crew:", first_member_name)            


# ### Consistency issue:Finding the number of departments for each movie in the dataset is difficult. hence, we plan to create a clearer list that contains the number of different departments in each film.

# ## 3. Clean data
# Clean the data to solve the 4 issues corresponding to data quality and tidiness found in the assessing step. **Make sure you include justifications for your cleaning decisions.**
# 
# After the cleaning for each issue, please use **either** the visually or programatical method to validate the cleaning was succesful.
# 
# At this stage, you are also expected to remove variables that are unnecessary for your analysis and combine your datasets. Depending on your datasets, you may choose to perform variable combination and elimination before or after the cleaning stage. Your dataset must have **at least** 4 variables after combining the data.

# In[15]:


# Make copies of the datasets to ensure the raw dataframes are not impacted


##Already done it above

# I would not create another copy since we've already converted the "cast" and "crew" columns to JSON format.## movies.to_csv('local_tmdb_5000_movies.csv', index=False)

## movies.to_csv('local_tmdb_5000_movies.csv', index=False)
## Credits.to_csv('local_tmdb_5000_credits.csv', index=False)


# ### Quality Issue 1:Missing values in "budget" and "revenue" columns.

# In[16]:


#Apply the cleaning strategy



movies['revenue'] = movies['revenue'].replace(["nan", "None"], np.nan)
movies['budget'] = movies['budget'].replace(["nan", "None"], np.nan)

# Step 2: Replace zeros with NaN
movies['budget'].replace(0, np.nan,inplace=True)
movies['revenue'].replace(0, np.nan,inplace=True)

# Step 3: Convert to float, removing commas
movies['revenue'] = movies['revenue'].apply(lambda x: float(str(x).replace(',', '')) if pd.notnull(x) else np.nan)
movies['budget'] = movies['budget'].apply(lambda x: float(str(x).replace(',', '')) if pd.notnull(x) else np.nan)


# In[17]:


#Validate the cleaning was successful
movies.sample(5)


# In[18]:


# Calculate mean for budget and mode for revenue
budget_mean = int(movies['budget'].mean())
revenue_mean = movies['revenue'].mean()

#print the values for mean and mode 
print("Budget meane value is equal to",budget_mean)
print("mean value for revenue column is equal to",revenue_mean)

# Replace NaN values
movies['budget'].fillna(budget_mean, inplace=True)
movies['revenue'].fillna(revenue_mean, inplace=True)

# Convert scientific notation to regular float format for "revenue" 
movies['revenue'] = movies['revenue'].apply(lambda x: f"{x:,.2f}")


movies.head(55)


# ### The budget and revenue columns initially contained values of zero, which have since been replaced with the mean and mode values, respectively.
# 

# ### Quality Issue 2: Dtype for "release_date " column. 

# In[19]:


#Apply the cleaning strategy

movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')


# In[20]:


#Validate the cleaning was successful
movies.info()


# ### The release_date column, which was previously of type object, is now of type datetime64[ns].

# ### Tidiness Issue 1: Identify crew members for each movie.

# In[21]:


# Apply the cleaning strategy

##Apply json load 
# Credits['crew'] = Credits['crew'].apply(json.loads)

# Extract crew names and add them to a new column
Credits['crew_names'] = Credits['crew'].apply(lambda crew_list: [member['name'] for member in crew_list if 'name' in member])



# In[22]:


#  Validate the cleaning was successful
Credits


# ### we read json data and create a list that iterates through each movie to gather the crew members for each one.

# ### Tidiness Issue 2: Calculate number of departments for each movie. 

# In[23]:


#Apply the cleaning strategy


# Apply the json.loads function directly to the 'crew' column
# Credits['crew'] = Credits['crew'].apply(json.loads)

# Extract crew names and add them to a new column
Credits['crew_names'] = Credits['crew'].apply(lambda crew_list: [member['name'] for member in crew_list if 'name' in member])

# Count the number of unique departments in the 'crew' column for each row
Credits['num_departments'] = Credits['crew'].apply(lambda crew_list: len(set(member['department'] for member in crew_list if 'department' in member)) if isinstance(crew_list, list) else 0)



# In[24]:


#Validate the cleaning was successful
Credits.head()


# ### To identify the number of departments for each movie we read the "crew " column and used "json.loads" to phrase the json data by extracting department information for each row.

# ### **Remove unnecessary variables and combine datasets**
# 
# 

# ### Droping data in "Credits" dataframe.

# In[25]:


# Remove unnecessary variables and combine datasets
# Drop the 'crew', 'cast', , 'title' and "movie_id" columns
Credits.drop(columns=['crew', 'cast', 'title'], inplace=True)
Credits


# ### Droping data in "movies" dataframe.

# In[26]:


movies.drop(columns=["overview",'genres', 'homepage', 'keywords',"original_language","original_title","production_companies","production_countries","runtime","status","tagline","spoken_languages"], inplace=True)


# In[27]:


movies


# In[28]:


movies.rename(columns={'id': 'movie_id'}, inplace=True)


# In[29]:


cleaned_df = pd.merge(movies, Credits, on='movie_id')


# ### Display merged dataframe

# In[30]:


cleaned_df


# ### Reordering the dataFrame

# In[31]:


#new column order
new_order = ['movie_id', 'title', 'budget', 'revenue', 'release_date','popularity','vote_count','vote_average','crew_names','num_departments']

# Reorder the DataFrame columns
cleaned_df = cleaned_df[new_order]
cleaned_df.head()


# ## 4. Update your data store
# 

# In[32]:


#saving the cleaned dataset
cleaned_df.to_csv('cleaned_movies_Credits.csv', index=False)
cleaned_df.info()


# ## 5. Answer the research question
# 
# ### **5.1:** Define and answer the research question 
# 

# *Identify trends in movie production over the years :* We would mainly depend on movie rating in our analysis so we would observe the behavoir of movie overtime with different varibles.

# In[37]:


#Visual 1, histograme of release Year with Popularity 

# Drop rows where 'release_date' could not be converted to datetime
cleaned_df = cleaned_df.dropna(subset=['release_date'])

cleaned_df.loc[:, 'year'] = cleaned_df['release_date'].dt.year

# Group by year and calculate the average popularity
popularity_by_year = cleaned_df.groupby('year')['popularity'].mean()

# Plot the histogram
plt.figure(figsize=(8, 6))
plt.bar(popularity_by_year.index, popularity_by_year.values)
plt.xlabel('Year')
plt.ylabel('Average Popularity')
plt.title('Average Popularity of Movies by Release Year')
plt.show()


# In[34]:


#Visual 2, barplot of release Year with number of departments 

popularity_by_departments = cleaned_df.groupby('num_departments')['popularity'].mean()

# Plot the bar plot
plt.figure(figsize=(10, 6))
popularity_by_departments.plot(kind='bar')
plt.xlabel('Number of Departments')
plt.ylabel('Average Popularity')
plt.title('Average Popularity by Number of Departments')
plt.xticks(rotation=360)
plt.show()


# ### Movies that have release dates from 2000 and above have an up-trend in movie popularity. Also, it is evident that the movie's popularity rises relative to the number of departments

# *Identify the film team members who have received 100 rating and above in movie rating*

# In[35]:


# Filter for movies with popularity of 100 and above
high_popularity_movies = cleaned_df.loc[cleaned_df['popularity'] >= 100].copy()



# Show the results
high_popularity_movies[['title', 'crew_names', 'popularity']]


# ### The  above table displays name of crew members that earned a rating of 100 and more in movie rating.

# ### **5.2:** Reflection
# 

# 
# #### ْْْRmove movies without a website to ensure all entries have accessible and verifiable information.
#     
# #### Create a dictionary containing the cast IDs from the "cast" column, making it easier to display complete cast information.
#     
# #### Remove any films that have an empty list of "keywords" as it make a qulity issue.

# In[36]:


cleaned_df

