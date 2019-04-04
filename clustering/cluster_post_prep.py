import pandas as pd
import numpy as np


## Function converts inngredients to sudo categories to try and get better sense
## of the clusters. If convert function is not run then does on individual ingredients.
def convert(df):
	convert = pd.read_csv('data/ing_to_cat.csv')
	convert = convert.dropna()

	new_df = pd.DataFrame(columns=convert.category.unique())

	d = pd.Series(convert.category.values, convert.ing.values).to_dict()

	for col in df.columns:
		if col in d.keys():
			new_col = d[col]
			vals = df[col].values

			if len(new_df[new_col].values) < 1 or (new_df[new_col].isnull().values.sum() > 2):
				new_df[new_col] = vals
			else:
				vs = new_df[new_col].values
				new_df[new_col] = vs+vals

	return new_df


## Need to scale the features for clustering (distance metric)
def scale_df(df):
	for col in df.columns:
		if col != 'cust_id':
			df[col] = (df[col] - df[col].mean())/df[col].std()
	return df


def get_df():
	## Read in pickle data
	ing_freq = pd.read_pickle("clustering/user_f_df_tot.p")
	ing_freq.sample(3)
	customers = ing_freq.cust_id

	ing_freq = convert(ing_freq)

	return scale_df(ing_freq)


