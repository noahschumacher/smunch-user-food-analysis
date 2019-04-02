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


-- Getting the number of times meals have been offered to customer
SELECT account_sfid_order, contact_sfid as user_id, delivery_timestamp as deliv_tmstmp
FROM bi.executed_order_employee
WHERE contact_sfid = '0030N00002LQqB9QAL' and order_type = 'single'

SELECT product_name, count(product_name), delivery_timestamp
FROM bi.executed_order_employee
WHERE account_sfid_order = '0010N00004IaGG6QAN' and 
	delivery_timestamp IN ('2017-12-12 10:30:00+00',
						   '2018-09-27 10:30:00+00',
						   '2019-01-09 11:30:00+00',
						   '2018-04-04 08:30:00+00',
						   '2017-12-12 10:30:00+00',
						   '2018-09-20 10:30:00+00')
GROUP BY product_name, delivery_timestamp


-- Above two querries combined into one.
WITH t1 AS(
	SELECT product_sfid
	FROM bi.executed_order_employee
	WHERE account_sfid_order = '0010N00004IaGG6QAN' and 
		delivery_timestamp IN (
			SELECT delivery_timestamp as deliv_tmstmp
			FROM bi.executed_order_employee
			WHERE contact_sfid = '0030N00002LQqB9QAL' and order_type = 'single')
	GROUP BY product_name, delivery_timestamp
)
SELECT t1.product_sfid, COUNT(t1.product_sfid)
FROM t1
GROUP BY t1.product_sfid


-- GENERALIZING THE ABOVE AND CREATING SEPERATE TABLE FOR SPEED --

-- contact_sfid, meal_id, meal_count, ingredient_ids
CREATE TABLE noah.user_order_ingredients AS
(
	WITH t1 as
		(SELECT contact_sfid, product_sfid as meal_id, COUNT(product_sfid) as meal_count
		FROM bi.executed_order_employee
		GROUP BY contact_sfid, product_sfid),
			
	t2 as
		(SELECT product__c as meal_id, ARRAY_AGG(ingredient__c) as ingredient_ids
		FROM salesforce.product_ingredient__c
		GROUP BY product__c)
	
	SELECT t1.contact_sfid, t1.meal_id, t1.meal_count, t2.ingredient_ids FROM t1
	LEFT JOIN t2
	ON t1.meal_id = t2.meal_id
	WHERE t2.ingredient_ids IS NOT NULL
)

select * from noah.user_order_ingredients
where contact_sfid = '0030N00002LQqB9QAL'



SELECT contact_sfid, delivery_timestamp as deliv_tmstmp
FROM bi.executed_order_employee
WHERE order_type = 'single'
GROUP BY contact_sfid


