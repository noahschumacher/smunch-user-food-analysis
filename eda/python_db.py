import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import psycopg2


with open('private/db_info.txt') as f:
	content = f.readlines()
	content = [x.strip('\n') for x in content]
print(content)
