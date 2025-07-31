import os
from ehrql.codes import codelist_from_csv

# Tuple inputs
# [0] Cluster Name
# [1] Substring present in CSV filename (if different to cluster name)
# [2] Column containing the codes

cl_tups = [
    ("ast_cod", None, "code"),
    ("astres_cod", None, "code"),
    ("copd_cod", None, "code"),
    ("copdres_cod", None, "code"),
    ("asttrt_cod", "drug-treatment", "code"),
    ("all_saba", "saba-inhalers", "code")
]

cl_dict = {}

codelist_filenames = [file for file in os.listdir("codelists/") if file[-3:] == "csv"]

for name, substr, colstr in cl_tups:
    substr = name if substr == None else substr
    csv = list(filter(lambda file: substr in file, codelist_filenames))[0]
    cl_dict[name] = codelist_from_csv("codelists/"+csv, column=colstr)