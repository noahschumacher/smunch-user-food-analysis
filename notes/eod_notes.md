## End of Day Notes

### Day2:
- Essentialy closed the loop:
	- Clustered users with kmeans and hierarchial clustering
	- Got model to predict meal rating based on the ingredients
	- Inspected ingredient (aka feature) importances
- Looking forwards:
	- Edit hierachial clustering to show top three foods for each group in graph
	- Utilize clusters in prediction:
		- Starts from sql querry where rating are split into cluster groups.
		- Refit model for each cluster groups different targets.

### Day3:
- Re explored clustering but used mapped ingredients to more general categories.
	- Did this myself and has bias / some mistakes in mapping.
	- Some ingredients I did not know how to classify.
	- If this was to be used in the future someone with more culinary expertise should create the mappings.
	- With mapped ingredients the clustering shows meaningful clusters!
	- Hierarchial clustering still not proving to be as useful.
- Created basic ALS recommendation meal recommendation model:
	- Need to do train test split and validate its performance.
	- In future:
		- Compare using avg value with random forrest meal prediction
		- Write function to get top recommended meals.
- Looking ahead:
	- Need to re map out what I am going to do moving forwards with this project:
		- What am I going to deliver?
		- How am I going to deliver it?
		- Prioritize goals of accomplishment.

### Day3:
- Completed:
	- Validated NMF recommendation system:
		- MSE is about 1 (1 star off on avg)
		- Putting in avg value for meal is making the NMF overfit to the averages and ignore the real values
		- Sparsity of matrix is 99.1%
	- Innspecting in hidden topics in H matrix from NMF give some insights into meal groups.
	- Created neural network to predict meal ratinng based on meal predictions
		- Initially though neural net would learn ingredient combinations to more accuretly predict a meal rating.
		- Was not able to get model score better than baseline of avg meal rating.
		- Classifier neural net as well predicts probability a meal will be certain rating (0,1,2,3,4) but seems to be overfitting to predict 3 (the most common meal rating)
- Looking ahead:
	- Might be time to focus more on clustering user and discovering trends within user groups.
	- Maybe break out from ingredient and meal preferences and look into things like:
		- When certain users order their meal.
		- User churning indicators.
