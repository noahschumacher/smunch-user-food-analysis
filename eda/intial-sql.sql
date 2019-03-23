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
)

-- Create meal ingredients table
CREATE TABLE noah.meal_ingredients AS
(
	SELECT
		product__c as meal_id,
		sfid as ingredient_id
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


