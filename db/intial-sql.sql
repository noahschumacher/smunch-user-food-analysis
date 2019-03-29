-- SQL Querries and Descriptions

----------------------------------------------------
--- Querries used to create tables in noah schema --


-- Create order table
CREATE TABLE noah.orders AS
(
	SELECT 
		contact_sfid as cust_id,
		product_sfid as meal_id,
		product_name as meal_name,
		rating_score as meal_rating
	FROM bi.executed_order_employee
	WHERE order_type = 'single'
)

-- Create meal ingredients table
CREATE TABLE noah.meal_ingredients AS
(
	SELECT
		product__c as meal_id,
		ingredient__c as ingredient_id
	FROM salesforce.product_ingredient__c
)

-- Create ingredient table
CREATE TABLE noah.ingredients AS
(
	SELECT
		sfid as ingredient_id,
		name
	FROM salesforce.ingredient__c
)


--------------------------------------------
--- Getting meal rating information -------

-- Customer rating table
SELECT 
	contact_sfid as cust_id,
	product_sfid as meal_id,
	product_name as meal_name,
	product_type as category,
	restaurant_name,
	delivery_timestamp as delivery_tm,
	rating_score as meal_rating
FROM 
	bi.executed_order_employee
WHERE
	order_type = 'single' and rating_score IS NOT NULL

-- Aggregated customer rating table on meal (avg meal rating)
SELECT
	product_sfid as meal_id,
	product_name as meal_name,
	product_type as category,
	AVG(rating_score) as avg_meal_rating,
	COUNT(rating_score) as rating_count
FROM 
	bi.executed_order_employee
WHERE
	order_type = 'single' and rating_score IS NOT NULL
GROUP BY
	product_name, product_sfid, product_type


-- Aggregated ingredient table meal --> ingredients list
SELECT
	product__c as meal_id,
	ARRAY_AGG(ingredient__c) as ingredient_id
FROM
	salesforce.product_ingredient__c
GROUP BY
	product__c

-- Putting customer rating avg and aggregated meal ingredients 
-- into one table
CREATE TABLE noah.meal_rating_ingredients AS
	(WITH t1 AS
		(SELECT
			product_sfid as meal_id,
			product_name as meal_name,
			product_type as category,
			AVG(rating_score) as avg_meal_rating,
			COUNT(rating_score) as rating_count
		FROM 
			bi.executed_order_employee
		WHERE
			order_type = 'single' and rating_score IS NOT NULL
		GROUP BY
			product_name, product_sfid, product_type),

	t2 AS
		(SELECT
			product__c as meal_id,
			ARRAY_AGG(ingredient__c) as ingredient_ids
		FROM
			salesforce.product_ingredient__c
		GROUP BY
			product__c)
			
	SELECT 
		t1.meal_id, t1.meal_name, t1. category, t1.avg_meal_rating, t1.rating_count, t2.ingredient_ids FROM t1
	LEFT JOIN
		t2
	ON 
		t1.meal_id = t2.meal_id
	WHERE
		t2.ingredient_ids IS NOT NULL and t1.rating_count > 5)









