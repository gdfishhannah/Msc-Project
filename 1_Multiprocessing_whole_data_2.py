
# coding: utf-8

# In[30]:
from __future__ import print_function
from LaoGongLib import multiprocess_func
import time

import re
import requests
from requests.exceptions import ConnectionError
import os, sys, time
import time
import collections
import pandas as pd
import datetime
import numpy as np
from multiprocessing import Manager
import random

import pandas as pd
import gc
import h5py
# import hdfs
import numpy as np
import csv
# import feather
#path = '/media/hannah/UNTITLED/tour/data/'
file = '/media/hannah/UNTITLED/Warner_2015/201501 - part-m-001.gz'
data =file
# import warnings
# warnings.filterwarnings("ignore")
header = ['day',
 'log_time',
 'mobile',
 'track_id',
 'isrc',
 'upc',
 'artist_name',
 'track_name',
 'album_name',
 'customer_id',
 'postal_code',
 'access',
 'country_code',
 'gender',
 'birth_year',
 'filename',
 'region_code',
 'referral_code',
 'partner_name',
 'financial_product',
 'user_product_type',
 'offline_timestamp',
 'stream_length',
 'stream_cached',
 'stream_source',
 'stream_source_uri',
 'stream_device',
 'stream_os',
 'track_uri',
 'track_artists',
 'source']


def main():
    set_sleep_time = 5000000000
    max_sleep_time = 5000000000
    penalty = 1000000000
    max_restart = 10

    split = 512
    max_thread = 64
    process_start_duration = 0
    cpu_max = 105

    #     parameter_tuple = []
    #     for i in range(300):
    #         parameter_tuple.append((i,return_dict))

    raw_data = pd.read_csv(data, compression = 'gzip', sep = '\x01',error_bad_lines=False, chunksize = 10**6,names = header)
    two_artist = []
    #    artist_path = '/media/hannah/UNTITLED/artist/'
    chunk_no = 0
    for chunk in raw_data:
        t_ref = time.time()
        manager = Manager()
        return_dict = manager.dict()

        percentage_dict = manager.dict()
        def data_batch(i,return_dict):
            return_dict[i] = chunk.loc[chunk['artist_name']==i]
        parameter_tuple = []
        chunk = chunk.drop(['day','log_time','track_id','track_name','album_name','track_artists','country_code','filename', 'referral_code', 'partner_name', 'offline_timestamp', 'stream_cached', 'stream_source', 'source'], axis = 1)

        for i in list(chunk['artist_name'].unique()):
            parameter_tuple.append((i,return_dict))

        
        multiprocess_func(object_func=data_batch, name_list=parameter_tuple, set_sleep_time=set_sleep_time,
                          max_sleep_time=max_sleep_time, split=split, max_restart=max_restart, max_thread=max_thread,
                          penalty=penalty, process_start_duration=process_start_duration, percentage_dict=percentage_dict, 
                          cpu_max=cpu_max)
        np.save('./return_dict_2/return_dict_' + str(chunk_no) + '.npy', return_dict.copy())
        print(chunk_no, "{:.2f} seconds".format(time.time() - t_ref), 'saved retrun_dict to ./return_dict_2/return_dict_' + str(chunk_no) + '.npy')
        chunk_no+=1

        #for i in return_dict.keys():
        #    try:
        #        return_dict[i].to_csv(artist_path+str(i)+'.txt',mode = 'a',header=False,index=False)
        #    except (FileNotFoundError,OSError):
        #        return_dict[i].to_csv('two_artist'+'.txt',mode = 'a',header=False,index=False)


# In[33]:

if __name__ == "__main__":
    main()


# In[ ]:



