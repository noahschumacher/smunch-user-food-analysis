## Notes as I work through Capstone

### data:
   - Where local csv files will love for eda and model training.


### eda:
##### - initial-sql.sql:
- File contains all used SQL queries
- Should make queries handle more of the work than they do (In pandas two groupbys could be converted in sql)

##### - python_db.py:
- File contains a function for querying Smunch DB and three base queries to get save data to CSV file locally.

##### - eda1.ipyb:
- Inital exploration of users, meals, ingredients
  - Total Users = 9838
  - Total Meals = 980
  - Total Ingredients = 1414 (unique sf ids but some are the same)
  - Total Meal Count = 256886

- Large portion of users have ordered only few times:
  - 21% have ordered 2 or less times
  - Might be beneficial to only look at users who have ordered over x amount of times

- Some ingredients are duplicated (have two or more sfids which are account for minor changes to the name of the ingredient).
  - Ex: "fried onion" and "friend onions" have different ids and counts associated with them.
- Some ingredients are very similar and should maybe be grouped together.
  - Ex: "lime" and "lime juice" , "pepper" and "pepper sauce"

### model:
##### data-prep.py:
- Rudementary attempt to create ingredient frequency dataframe.
- File groups base tables customer_id and meal_id and then uses loops to go through every ingredient in every meal for each customer.
- Due to looping process ingredients with the same spelling and different capitalization are grouped together which is good.
- Runs very slowly (only using for a subset of data right now)
- Saves the dataframe as a pickle file