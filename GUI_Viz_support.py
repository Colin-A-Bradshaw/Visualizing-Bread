#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 6.1
#  in conjunction with Tcl version 8.6
#    Apr 25, 2021 05:39:13 PM EDT  platform: Windows

import numpy as np
import pandas as pd
import io
import plotly.express as px
from PIL import Image, ImageTk

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def set_Tk_var():
    global che56
    che56 = tk.IntVar()
    global che57
    che57 = tk.IntVar()
    global che45
    che45 = tk.IntVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def save_flour(p1):
    global sel_flour_tuple
    sel_flour_tuple = p1
    print(sel_flour_tuple)

def save_leavening(p1):
    global sel_leavening_tuple
    sel_leavening_tuple = p1
    print(sel_leavening_tuple)


def group(df_data, min, max, interval):
    # break reg-green spectrum over number of groupings
    delta = max - min
    groupings = delta // interval
    groupings = int(groupings)
    ranges = []
    for i in range(groupings):
        ranges.append(min + interval * i)
    ranges.append(max)

    df_ratings = pd.DataFrame(columns=['grouping'])
    for i in range(len(df_data)):
        this_rating = float(df_data._get_value(i, 2, takeable=True))
        if this_rating >= min:
            has_happened = True
            for i in range(len(ranges) - 1):
                if this_rating >= ranges[i] and this_rating < ranges[i + 1]:
                    range_string = str(ranges[i]) + '-' + str(ranges[i + 1])
                    super_norm = (ranges[i] + ranges[i + 1]) / 2
                    #print(super_norm)
                    df_ratings.loc[len(df_ratings)] = [super_norm]
                    has_happened = False
            # take care of issue with floating point comparisons
            if(has_happened):
                range_string = str(ranges[len(ranges) - 2]) + '-' + str(ranges[len(ranges) - 1])
                super_norm = (ranges[i] + ranges[i + 1]) / 2
                #print((super_norm))
                df_ratings.loc[len(df_ratings)] = [super_norm]
    return df_ratings

def viz_button_clicked(p1):
    print('GUI_Viz_support.viz_button_clicked')
    sel_flour = []
    for i in range(len(sel_flour_tuple)):
        sel_flour.append(p1.flour_types[sel_flour_tuple[i]])
    print(sel_flour)
    sel_leavening = []
    for i in range(len(sel_leavening_tuple)):
        sel_leavening.append(p1.leaven_types[sel_leavening_tuple[i]])
    print(sel_leavening)
    min_rating = 0
    max_rating = 5
    group_by = 0.01
    if not p1.from_entry.get() == '':
        min_rating = float(p1.from_entry.get())
    if not p1.to_entry.get() == '':
        max_rating = float(p1.to_entry.get())
    if not p1.group_by_entry.get() == '':
        group_by = float(p1.group_by_entry.get())
    flour_exclusive = che56.get()
    leavening_exclusive = che57.get()
    narrow_results = che45.get()
    # now we have all the needed data to filter the dataframe all_data to get the desired results.
    df_working = None
    if narrow_results == 0:
        df_working = p1.df_all_data
    else:
        df_working = p1.df_last_query

    # to_drop will contain the row of every item to be dropped from df_working
    to_drop = []
    if flour_exclusive == 0 and leavening_exclusive == 0:
        # check if the selected flour(s) and leavener(s) are in a particular row of the dataframe
        for i in range(len(df_working)):
            flour_item = df_working['type of flour'].iloc[i]
            leaven_item = df_working['leavening agent'].iloc[i]
            if type(leaven_item) is float:
                # for undetermined leavening - '', type appears as float
                # set to empty list
                leaven_item = []
            item_has_flour = False
            item_has_leavener = False
            for type_of_flour in sel_flour:
                if type_of_flour in flour_item:
                    item_has_flour = True
            for leavener in sel_leavening:
                if leavener in leaven_item:
                    item_has_leavener = True
            if not item_has_flour or not item_has_leavener:
                to_drop.append(i)
        # we know now all items to be dropped from df_working on the basis of flour. drop them.
        df_working = df_working.drop(to_drop)
    elif flour_exclusive == 1 and leavening_exclusive == 0:
        # check if the selected leavener(s) are in this row of the dataframe
        # check if the flour(s) in this row of the dataframe are in the selected flour(s)
        for i in range(len(df_working)):
            flour_item = df_working['type of flour'].iloc[i]
            leaven_item = df_working['leavening agent'].iloc[i]
            if flour_item.find(',') != -1:
                flour_item = flour_item.split(',')
            else:
                flour_item = [flour_item]
            if type(leaven_item) is float:
                # for undetermined leavening - '', type appears as float
                # set to empty list
                leaven_item = []
            flour_good = True
            leavener_good = False
            for item in flour_item:
                if item not in sel_flour:
                    flour_good = False
            for leavener in sel_leavening:
                if leavener in leaven_item:
                    leavener_good = True
            if not leavener_good or not flour_good:
                to_drop.append(i)
        df_working = df_working.drop(to_drop)
    elif flour_exclusive == 0 and leavening_exclusive == 1:
        # check if all of the leavener(s) in this row of the dataframe are in the selected leavener(s)
        # check if the selected flour(s) are in this row of the dataframe
        for i in range(len(df_working)):
            flour_item = df_working['type of flour'].iloc[i]
            leaven_item = df_working['leavening agent'].iloc[i]
            if type(leaven_item) is float:
                # for undetermined leavening - '', type appears as float
                # set to empty list
                leaven_item = []
            else:
                if leaven_item.find(',') != -1:
                    leaven_item = leaven_item.split(',')
                else:
                    leaven_item = [leaven_item]
            flour_good = False
            leavener_good = True
            for type_of_flour in sel_flour:
                if type_of_flour in flour_item:
                    item_has_flour = True
            for item in leaven_item:
                if item not in sel_leavening:
                    leavener_good = False
            if not leavener_good or not flour_good:
                to_drop.append(i)
        df_working = df_working.drop(to_drop)
    elif flour_exclusive == 1 and leavening_exclusive == 1:
        # check if all of the leavener(s) in this row of the dataframe are in the selected leavener(s)
        # check if the flour(s) in this row of the dataframe are in the selected flour(s)
        for i in range(len(df_working)):
            flour_item = df_working['type of flour'].iloc[i]
            leaven_item = df_working['leavening agent'].iloc[i]
            if flour_item.find(',') != -1:
                flour_item = flour_item.split(',')
            else:
                flour_item = [flour_item]
            if type(leaven_item) is float:
                # for undetermined leavening - '', type appears as float
                # set to empty list
                leaven_item = []
            else:
                if leaven_item.find(',') != -1:
                    leaven_item = leaven_item.split(',')
                else:
                    leaven_item = [leaven_item]
            flour_good = True
            leavener_good = True
            for item in flour_item:
                if item not in sel_flour:
                    flour_good = False
            for item in leaven_item:
                if item not in sel_leavening:
                    leavener_good = False
            if not leavener_good or not flour_good:
                to_drop.append(i)
        df_working = df_working.drop(to_drop)

    # use user input to create groupings by rating
    df_groupings = group(df_working, min_rating, max_rating, group_by)
    df_working.reset_index(inplace=True, drop=True)
    # now create a new visualization based off of this dataframe
    frames_list = [df_working['type of flour'], df_working['leavening agent'], df_working['rating'], df_groupings]
    headings = ['type of flour', 'leavening agent', 'ratings', 'grouped ratings']
    df_for_query = pd.concat(frames_list, axis=1, keys=headings, ignore_index=True)
    fig = px.parallel_categories(df_for_query, dimensions=[0, 1, 3],
                                 dimensions_max_cardinality=100,
                                 color=3, color_continuous_scale=px.colors.diverging.RdYlGn,
                                 color_continuous_midpoint=6 / 2,
                                 labels={'type of flour': 'type of flour', 'leavening agent': 'leavening agent',
                                         'grouped ratings': 'ratings'})
    fig.show()
    datastring = ''
    size = p1.datapointBox.size()
    p1.datapointBox.delete(0, size)
    datapoints_list = []
    for i in range(len(df_working)):
        recipe_name = str(df_working.loc[i][1])
        recipe_rating = str(df_working.loc[i][2])
        recipe_url = str(df_working.loc[i][3])
        index = recipe_name.find('|')
        recipe_name = recipe_name[0:index]
        while len(recipe_name) < 55:
            recipe_name += ' '
        while len(recipe_rating) < 7:
            recipe_rating += ' '
        datastring = recipe_name + recipe_rating + recipe_url
        datapoints_list.append(datastring)
        datastring = ''

    data_counter = 0
    while data_counter < len(datapoints_list) -1:
        p1.datapointBox.insert(data_counter, datapoints_list[data_counter])
        data_counter += 1

    to_drop = []
    # enable narrowing of results
    p1.narrow_results_checkbutton.configure(state='active')
    p1.df_last_query = df_working
    sys.stdout.flush()

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import GUI_Viz
    GUI_Viz.vp_start_gui()




