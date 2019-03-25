import pandas as pd
import numpy as np

import psycopg2


## Function connects to Smunch DB and runs SQL querry returning a DataFrame
def run_sql_query(query):

	with open('private/db_info.txt') as f:
		content = f.readlines()
	content = [x.strip('\n') for x in content]
	
	conn = psycopg2.connect(dbname=content[0], user=content[1], host=content[2],
						   port=content[3], password=content[4])
	
	df = pd.io.sql.read_sql_query(query, conn)
	return df


## Reading in noah tables and saving them locally.
def get_data():
	orders = run_sql_query("Select * from noah.orders")
	meal_ingrds = run_sql_query("Select * from noah.meal_ingredients_f")
	ingrds = run_sql_query("Select * from noah.ingredients")

	orders.to_csv('data/orders.csv')
	meal_ingrds.to_csv('data/meal_ingrds.csv')
	ingrds.to_csv('data/ingrds.csv')

if __name__ == '__main__':
	get_data()




