## Smunch Customer Clustering and Meal Satisfaction Analysis
    
### Background:
Smunch is a rapidly growing B2B Food Delivery service based out of Germany, with their headquarters in Berlin. The general structure of Smunch consists of allowing employees of subscribing companies to choose an offered meal from local restaurants which Smuch packages and deliverers to the company. There are eight options per day (two restaurants with four options each). Each day the menu is changed and eight new meals are offered.

### Motivation:
As Smunch continues to expand and increase volume, it is extremely important to understand the trends and habits of their growing customer base. From a basic understanding of what meals are popular to an in-depth breakdown of what the key ingredients in meals, certain customers find most important, understanding what makes Smunch customers tick will allow Smunch to continuously improve their product and customer experience. More concretely having insights into key ingredients will allow Smunch to tailor meals to appeal to a wider customer base as well as increased order numbers. Understanding the factions or clusters of their customers and what they like will allow them to make sure each customer is presented with a good meal option every day. Other insights including identifying which customers are the most loyal and which customers churn or will allow for tailored efforts to increase customer retention and frequency of use. 

### Structure:
#### Clustering:
  - This folder attempts to clusters users based on their ingredient preferences.
  - Two types of clustering are used:
    1. K-Means
    2. Hierarchial
  - From inspection K-Means seems to reveal the most about the clusters.
  - The 3 significant clusters seem to be:
    1. Protien, Dairy heavy
    2. Vegan / Vegetarian
    3. Seafood / Asian ingredients
  - Other inspection is done on the hard labeled meals:
    1. Vegan
    2. Vegetarian
    3. Animal Protien

#### Average Meal Rating Prediction:
  - Predicting the average rating of meal by users based on the ingredients in the meal.
  - Several models attempted (listed in order of performance.)
    1. Random Forrest Regressor 1% lower MSE
    2. Gradient Boost Regressor 1% lower MSE
    3. Baseline (Avg of all meal ratings)
    4. Neural Network same as baseline.
  - Not much signal in ingredients alone to make model significant.
  - Realized ratings do not always depend on the quality or taste of the meal. In fact most bad ratings tend to come other factors besides taste. For example, delivery was late, meal was incorrect, meal was cold, etc.
  - Need a better target value.

#### Probabilty of Ordering Meal Prediction:
  - Solution to bias present in the ratings.
  - Target value is now $\frac{# of times ordered}{# of times offered}$
  - Feature matrix are the ingredients the user has encountered.
  - MSE is 8-12% lower than the guessing the average frequency of order.
  - Each user has their own model (each user has different preferences)

#### Recommender:
  - Simple recommender systems uses NMF.
  - Hidden user topics show insights into meal groups.


### Goals :
Bellow are the desired outcomes of the Smunch Customer and Meal Analysis:

- Clustering of customers based on meal preferences:
  - Motivation:
    - Customize menu so that each cluster of customers has a food option each day.
    - Understand what their largest customer base cares about and what features of meals are only liked by a small portion of the entire customer base.
- Clustering of customers based on the frequency of use:
  - Motivation:
    - Identify features that indicate a customer might churn.
    - Identify what features cause a customer to be loyal (high frequency)
    - Identify where in the user's timeline of Smunch a customer churns.
- Identification of key ingredients in customer meal satisfactions:
  - Motivation:
    - Allow Smunch to avoid negatively contributing ingredients to meals.
    - Work with restaurants to create other promising meals.
- Combine nutritional information with key ingredients to further understand customer ordering habits:
  - Motivation:
    - Allow for further meal customization to align with customer nutritional tendencies.
    - Give indication on how much emphasis Smunch should put on nutritional value of their meals.

### Execution / Pipeline:
Below is a rough description of how the above goals would be achieved sequentially. It is important to understand that some of the goals are related to one another other (3 and 4 are very related, 1 is also related) and might be completed as second iterations of the analysis. 
#### 1. Cluster users based on meal preference:
  - Query Smunch DB using SQL and the perform EDA in Python Notebook:
    - Use the number of frequency of a meal order to clusters users.
      - Explore different clusterig techniques, K-Means, Hierarchial.
    - Uncover insight as two what each cluster indicates
#### 2. Identify key ingredients in meal ratings:
  - Query Smuch DB using SQL and the perform EDA in Python Notebook:
    - Create a dataframe with ingredients as columns and meal as the row.
    - Explore prediction techniques using either rating of meal or % of orders per day as a target to get a meal prediction model
      - Regressor Model could use Linear Regression, Random Forrest, Gradient Boost etc.
    - Explore the feature importance (ie ingredient importance in prediction)
  - Redo above but separate analysis into the clustered user groups:
    - If a significant difference in key ingredients, might indicate different user groups value different ingredients differently
  - Complete model will allow for ingredients to be entered into a meal and meal rating would be predicted (both as a whole and for clustered user groups)
    - Would be ideal to wrap this up into a Web App so Smunch users could explore different meals (Smunch would probably build their own page on the backend site for this as well
#### 3. (After the first iteration) Scrape of use nutritional database tables on key ingredients to gain insights as to how customers value different meals.
#### 4. Final Report:
  - The final product of this project will be a comprehensive report outlining the insights, shortcoming, and documentation of the analysis done.
  - This report will give Smunch actionable insight and allow them for continued exploration of user groups. 

### Potential Areas of Concern / Difficulty:
#### 1. Lack of a strong signal in individual ingredient importance. Meals are complex and the interaction of ingredients is what really makes up the taste. Individual ingredients might not encompass these complex relations.
#### 2. Comparing users who have been using Smunch for a long time vs recently started using Smunch:
  - Handling meals that have never been offered to a user.
  - Handling situations where meals have not been offered at the same time as other meals.
#### 3. Data Wrangling:
  - Large database with lots of connected tables could mean lots of time getting queries correct and performing analysis on the data.
#### 4. Unsupervised Learning:
  - Clustering users into groups might be hard to correctly identify or label the clusters
  - What to set the limit on the number of clusters to etc.
