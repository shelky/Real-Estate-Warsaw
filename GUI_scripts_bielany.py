#!/usr/bin/env python3

try:
    from tkinter import *
except ImportError:
    from Tkinter import *

import pandas as pd


def change_visibility(apartments_df, visible_apartments_df, v, filename):
    """
    The function checks which checkbuttons are ticked via v list variable and changes the visibility of those apartments
    in the GUI by swapping the visibility parameter in the database dataframe apartments_df. Then it exports updated
    database to a file.
    :param apartments_df: pandas dataframe, the imported database of the apartments
    :param visible_apartments_df: pandas dataframe with apartments which are visible in the GUI, used as a connector
    between full database apartments_df and the list of boolean variables v
    :param v: list of BooleanVar(), indicates which checkbuttons are ticked. The value True means that the apartment
    should be visible, the value False means that the apartment should disappear from the GUI.
    :return: The script does not return any information. Before finishing it refreshes GUI by the action of GUI_setup()
    function
    """
    list = [not v[i].get() for i in range(len(v))]
    rows = visible_apartments_df[list]
    for i in range(len(rows)):
        print('--------------')
        apartments_df.loc[apartments_df['url'] == rows.iloc[i,2], ['visible']] = 0
        print(apartments_df[(apartments_df['title'] == rows.iloc[i,0])&(apartments_df['url'] == rows.iloc[i,2])].values)
        print('...............')
        apartments_df.to_csv(filename, index = False, mode = 'w', header = False)
    GUI_setup(filename)
    return 0


def GUI_setup(filename):
    """
    Main script for setting up GUI with the new/visible apartments. It imports the database of apartments' ads and
    shows them in a tabular form. For clarity only apartments with True value of parameter "visible" are shown.
    Additionally one can erase the apartments from the list by using checkbuttons and the "Apply" button.
    :param filename: str, containing path and name of the database csv file
    :return:
    """
    columns = ['title', 'price', 'url', 'timestamp', 'visible']
    df = pd.read_csv(filename, names=columns)
    new_df = df[df.visible == 1]
    print(new_df)
    height = new_df.shape[0]
    width = new_df.shape[1]
    print('height: ', height)
    print('width: ', width)
    v = [BooleanVar() for i in range(height)]
    for i in range(len(v)):
        v[i].set(True)
    for i in range(height): #Rows
        for j in range(width): #Columns
            if j == 4:
                b = Checkbutton(root, text="", variable = v[i], onvalue = False, offvalue = True)
                b.config(width=1)
            if j == 0:
                b = Entry(root)
                b.insert(INSERT, str(new_df.iloc[i][j]))
                b.config(width=70, bg = 'old lace')
            if j == 1:
                b = Entry(root)
                b.insert(INSERT, str(new_df.iloc[i][j]))
                b.config(width=7, bg="papaya whip")
            if j == 2:
                b = Entry(root)
                b.insert(INSERT, str(new_df.iloc[i][j]))
                b.config(width=20, bg = 'lavender')
            if j == 3:
                b = Entry(root)
                b.insert(INSERT, str(new_df.iloc[i][j]))
                b.config(width=15, bg = 'old lace')

            b.grid(row=i+1, column=j)

    b = Button(root, text="Apply", command = lambda: change_visibility(df, new_df, v, filename))
    b.grid(row = 0,columns = 1)
    return 0

root = Tk()
GUI_setup('apartments_bielany.csv')
mainloop()