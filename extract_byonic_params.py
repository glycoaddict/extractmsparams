"""
simply reads the byparms file and outputs a text file with the salient information.
"""


import os
import custom_tools
import pandas as pd

def byparms_into_df(test=False):
    if test:
        open_file = r'test.byparms'
    else:
        open_file = custom_tools.getfile('select the byonic parameter file', '.byparms')

    return pd.read_table(open_file, skiprows=range(9), delimiter='=')


def parse_multiline_string(s):
    """
    this converts a multiline string into a list of individual lines=entries, stripped of white spaces
    and \n newlines.
    :param s:
    :return:
    """
    return [x.strip() for x in s.strip().split('\n')]


def initialise_salient_dict():
    """
    df_index : human readable string
    :return:
    """
    s = dict()




def get_salient_rows(df, index_salient_list):
    pass


