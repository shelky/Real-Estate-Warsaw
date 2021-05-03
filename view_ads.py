import pandas as pd

columns = ['title', 'price', 'url', 'timestamp', 'seen']
df = pd.read_csv('apartments_praga_poludnie.csv', names=columns)
new_df = df[df.seen == 1]

htmlfile = open('table_praga_poludnie.html','w')
htmlfile.write(new_df.to_html())
htmlfile.close()


#print(new_df)
# Use the .to_html() to get your table in html
#print(new_df.to_html())