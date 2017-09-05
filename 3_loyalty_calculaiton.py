
# coding: utf-8

# In[1]:

# get_ipython().magic('reset')


# In[2]:

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import gc
import matplotlib.pyplot as plt
#import seaborn as sns
#get_ipython().magic('matplotlib inline')
import time


# In[3]:

class time_est():
    def __init__(self, total_len):
        self.t_start = time.time()
        self.total_len = total_len
        self.count = 0
        self.t_ref = time.time()
    
    def check(self,no_of_check=1,info=""):
        self.count += no_of_check
        if time.time() - self.t_ref > 1:
            t_used = time.time() - self.t_start
            t_total = t_used * self.total_len / self.count
            t_remain = t_total - t_used
            process_bar = "|"
            for i in range(40):
                if (i/40) < (self.count/self.total_len):
                    process_bar += "█"
                else:
                    process_bar += " "
            process_bar += "|"
            print("\r" + (str(info) + "  {:.2f}% ({}/{})\t".format(self.count * 100/self.total_len, self.count,self.total_len)) + str(process_bar).ljust(45) + "Used: {:02.0f}:{:02.0f}:{:02.0f}".format(int(t_used/3600), int(t_used/60)%60, t_used % 60).ljust(16) + "ETA: {:02.0f}:{:02.0f}:{:02.0f}".format(int(t_remain/3600), int(t_remain/60)%60, t_remain % 60),end="")
            self.t_ref = time.time()
        if self.count == self.total_len:
            t_used = time.time() - self.t_start
            print("\r" + str(info) + "  Finished in " +"{:02.0f}:{:02.0f}:{:02.0f}".format(int(t_used/3600), int(t_used/60)%60, t_used % 60).ljust(100))


# In[4]:

header = [
 'mobile',
 'isrc',
 'upc',
 'artist_name',
 'customer_id',
 'postal_code',
 'access',
 'gender',
 'birth_year',
 'region_code',
 'financial_product',
 'user_product_type',
 'stream_length',
 'stream_source_uri',
 'stream_device',
 'stream_os',
 'track_uri']


# In[5]:

import os
all_file = os.listdir('artist_jan/')


# In[6]:

len(all_file)


# In[7]:

# need to be split into batches
import math
batch = 100
batch_size = math.ceil(len(all_file)/batch)
# index = 0
# for i in range(batch):
#     files = all_file[index:index+batch_size]
batch_size


# In[8]:

all_file[:3]


# In[ ]:

warning_name = []
est_1 = time_est(batch)
index = 0
count = 0
for i in range(batch):
    files = all_file[i*batch_size:(i+1)*batch_size]
#     count+=(len(files))
    for f in files:
        count+=1
    #     print(f)
    #     try:
        df = pd.read_csv('artist_jan/'+f,names = header,low_memory=False)
        df = (df[df['stream_length']>=100])
        new_df = pd.DataFrame()

        new_df['customer_id'] = df['customer_id']
        new_df['postal_code'] = df['postal_code']
        new_df['region_code'] = df['region_code']

        df = 0

        location = new_df['region_code'].unique()
        est = time_est(len(location))
        counts = []
        customer = []
        for j in location:
        #     len(new[new[i]])
            if j != 'nan':
                counts.append(len(new_df[new_df['region_code']==j]['customer_id'].unique()))
                customer.append(list(new_df[new_df['region_code']==j]['customer_id'].unique()))
        #     break
        # for i in customer:
        #     new[new['customer_id']==i]['region_code']
        #     location.append(new[new['customer_id']==i]['region_code'].iloc[0])
    #             est.check()

        rank = pd.DataFrame()
        rank['region_code'] = location
        rank['loyalty'] = counts
        rank['customer'] = customer
        rank.to_csv('jan/'+f,index = False)
    #         print(f)
    #     except FileNotFoundError:
#             warning_name.append(f)
    est_1.check()
#     break


# In[ ]:

count


# In[ ]:

jan = os.listdir('jan/')


# In[ ]:

len(jan)


# In[ ]:

aaa = list(set(jan)^set(all_file))
aaa


# In[ ]:



