---- Round 2 SQL Querries -----

-- Get meal category table 
SELECT * FROM bi.dish_profiles_static


-- Prep for vegan, veg, protien clustering --
SELECT
	contact_sfid as user_id
	ARRAY_AGG(product_sfid) as meal_ids
FROM
	bi.executed_order_employee
GROUP BY
	contact_sfid
WHERE
	order_type = 'single'


-- Get particular user information
SELECT
	contact_sfid as user_id,
	account_sfid_order as account_id,
	product_sfid as meal_id,
	product_name as meal_name,
	delivery_timestamp as tm_stmp
FROM
	bi.executed_order_employee
WHERE
	contact_sfid = '0030N00002LQqB9QAL'

-- Get list of meals offered to a company on a particular day
-- Will join above table on account id
-- Get particular user information
WITH t1 as
	(
	SELECT product_sfid as meal_id, COUNT(product_sfid) as meal_count
	FROM bi.executed_order_employee
	WHERE contact_sfid = '0030N00002LQqB9QAL'
	GROUP BY product_sfid
	),
		
t2 as
	(
	SELECT product__c as meal_id, ARRAY_AGG(ingredient__c) as ingredient_ids
	FROM salesforce.product_ingredient__c
	GROUP BY product__c
	)

SELECT t1.meal_id, t1.meal_count, t2.ingredient_ids FROM t1
LEFT JOIN t2
ON t1.meal_id = t2.meal_id
WHERE t2.ingredient_ids IS NOT NULL

