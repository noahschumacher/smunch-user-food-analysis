'''
File:
	- One run only.
	- Reads in user info from db and pickles it.
	- Pickled df used in creting user classes and models.
'''

import pandas as pd
import numpy as np
import pickle


## local run sql file
from db.python_db import connect, run_sql_query


conn = connect()

## Query gets cols (contact_sfid, contact_account_sfid, order_count)
q = '''
SELECT contact_sfid, contact_account_sfid, COUNT(contact_sfid) AS order_count
FROM bi.executed_order_employee
WHERE order_type = 'single'
GROUP BY contact_sfid, contact_account_sfid
ORDER BY order_count DESC'''

user_account_order = run_sql_query(q, conn)

pickle.dump(user_account_order, open('order_prediction/user_account_order.p', 'wb'))
