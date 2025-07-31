import pandas as pd

data = pd.read_csv("output/dataset.csv.gz")

# Rule 1 Denom (reversed)
data = data[
    (data.eunrescopd_dat.isnull()) &
    (data.ast_dat.isnull()) &
    (data.astres_dat.notnull()) &
    (data.asttrt_dat.isnull())
]

# Rule 2 Denom
data = data[
    (data.ast_dat.notnull()) &
    (data.astres_dat.isnull()) &
    (data.asttrt_dat.notnull())
]

# Rule 1 Numer

data["RESP-02"] = [True if x >= 6 else False for x in data["saba_count"]]


measure_numer = len(data[data["RESP-02"] == True])
measure_denom = len(data[data["RESP-02"] == False])

summary = pd.DataFrame({
    "Measure": ["RESP02"],
    "Numer": [measure_numer],
    "Denom": [measure_denom]
})

summary.to_csv("output/resp02_summary.csv", index=False)