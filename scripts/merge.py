"""The purpose of this simple script is to use pandas to merge the two partial csv files into one based on id
"""
import pandas

tarot_csv = pandas.read_csv('tarot-cards.csv')
description_csv = pandas.read_csv('descriptions.csv')
merged = tarot_csv.merge(description_csv, on='id')
merged.to_csv("generators.csv", index=False)


