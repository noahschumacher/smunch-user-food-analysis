### Predicting the average rating of a meal based on the ingredients.

Initially the rating seemed to be the clearest indicator of how successful a meal was. However after creating several different models to predict the rating of a meal based on the ingredients it was clear there was little to no signal.

#### Data:
  - Features = Ingredients
  - Target = Avg Meal Rating
 
Ex:

| MealID | Ingredient 1 | Ingredient 2 | ... | Ingredient N | Avg Rating |
|--------|--------------|--------------|-----|--------------|------------|
| 1      |      1       |     0        |     |      1       |     3.5    |
| 2      |      0       |     1        |     |      1       |     4.7    |
| 3      |      1       |     1        |     |      0       |     4.2    |


#### Models and Performance:
- Several models attempted (listed in order of performance.)
  1. Random Forrest Regressor 1% lower MSE
  2. Gradient Boost Regressor 1% lower MSE
  3. Neural Network very slightly better than baseline.
  4. Baseline (Avg of all meal ratings)
  
#### Issue and Solution:
  - Not much signal in ingredients alone to make model get significant results.
  - Realized ratings do not always depend on the quality or taste of the meal. In fact most bad ratings tend to come other factors besides taste. For example, delivery was late, meal was incorrect, meal was cold, etc.
  - Need a better target value --> [cluster folder link](https://github.com/noahschumacher/smunch-user-food-analysis/tree/master/clustering "Clustering Folder")
