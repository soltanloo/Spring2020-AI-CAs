import pandas as pd

# pd1 = pd.read_csv('output.csv')
# pd2 = pd.read_csv('output (3).csv')

# joined = pd.merge(pd1,pd2,on='index')
# joined = joined[joined['category_x']!=joined['category_y']]
# joined.to_csv("my_test.csv",index=False)


# pd1 = pd.read_csv('test.csv')
# pd2 = pd.read_json('big.json',lines=True)

# joined = pd.merge(pd1,pd2,on='headline')[['index','category']]
# # joined = joined[joined['category_x']!=joined['category_y']]
# joined.to_csv("ans.csv",index=False)

pd1 = pd.read_csv('output.csv')
pd2 = pd.read_csv('ans.csv')
joined = pd.merge(pd1,pd2,on='index')

# joined = joined[joined['category_x']!=joined['category_y']]
joined.to_csv('dup.csv',index=False)
