'''
File:

Creates:
	- cust_ratingDF.p:
		- rows = A meal experience
		- cols = cust_id, meal_id, meal_name, rating given
	- avg_meal_ratingDF.p:
		- Aggregated rating for meals
			- Avg meal rating, count of ratings for meal.
'''

import pandas as pd
import numpy as np
import pickle

from db.python_db import run_sql_query

## Get customer ratings table
cust_rs = run_sql_query("SELECT * from noah.cust_ratings")


## Querry to get the avg meal rating for each meal
querry = '''
SELECT
	product_name as meal_name,
	AVG(rating_score) as avg_meal_rating,
	COUNT(rating_score) as rating_count
FROM 
	bi.executed_order_employee
WHERE
	order_type = 'single' and rating_score IS NOT NULL
GROUP BY
	product_name'''

avg_rs = run_sql_query(querry)

pickle.dump(cust_rs, open('recommender/cust_ratingsDF.p', 'wb'))
pickle.dump(avg_rs, open('recommender/avg_meal_ratingDF.p', 'wb'))