from multiprocessing.pool import ThreadPool as Pool
import os
import polipy

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

import pandas as pd
import requests
import lxml
import cchardet
from bs4 import BeautifulSoup
import sys

from time import sleep

# don't forget to import
import pandas as pd
import multiprocessing

def func(d):
    # let's create a function that squares every value in the dataframe

    for index, row in d.iterrows():
        url = row['url']
        print(url)
        text = polipy.get_policy(url, screenshot=False)
        print(index)
        if text is not None:
            text.save(output_dir='data/textfiles_redone/' + url.split("/")[-1])

if __name__ == '__main__':

    # create as many processes as there are CPUs on your machine
    num_processes = multiprocessing.cpu_count()

    df = pd.read_csv('data/urls.csv')
    print(len(df))

    # calculate the chunk size as an integer
    chunk_size = int(df.shape[0]/num_processes)

    # this solution was reworked from the above link.
    # will work even if the length of the dataframe is not evenly divisible by num_processes
    chunks = [df.iloc[df.index[i:i + chunk_size]] for i in range(0, df.shape[0], chunk_size)]

    # create our pool with `num_processes` processes
    pool = multiprocessing.Pool(processes=num_processes)

    # apply our function to each chunk in the list
    result = pool.map(func, chunks)

    pool.close()
    pool.join()  # block at this line until all processes are done
    print("completed!")