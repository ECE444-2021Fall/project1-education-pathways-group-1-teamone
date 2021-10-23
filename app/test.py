import pandas as pd
import json
df = pd.read_pickle('resources/df_processed.pickle').set_index('Code')
course = df.loc['APS064H1'].to_json()

print(type(json.loads(course)))
