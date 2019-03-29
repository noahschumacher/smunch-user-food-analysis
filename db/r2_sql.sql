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