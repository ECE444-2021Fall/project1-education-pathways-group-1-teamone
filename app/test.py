import pandas as pd
import json
df = pd.read_pickle('resources/df_processed.pickle').set_index('Code')

dfbyCode = pd.read_pickle('resources/df_processed.pickle')
# course = df.loc['APS064H1']
# courseDict = json.loads(df.loc['APS064H1'].to_json())

results = df.loc[:, ["Course", "Division"]][:2]
print(results)

# tables = results.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False) 
# print(tables)
# tables = df.iloc[:2, :8].to_html(classes='data',index=False,na_rep='',render_links=True, escape=False)


