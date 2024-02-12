import pandas as pd

# generic filter function
# modify based on data characteristics (eg, if using our HE sensor with fucked voltages)
def filter(voltage, low, high):
    if (voltage <= low):
        return 0
    elif (voltage >= high):
        return 5

# import CSV, grab relevant cols, and clean unknown rows
# column names differ depending on port configuration and sampling rate
df = pd.read_csv("WITH-sway-bar-accel-right-wheels-2.csv") \
       .rename(columns={"Interval|\"ms\"|0|0|1" : "Interval (ms)",
                        "Analog5|\"Volts\"|0.0|5.0|200": "Voltage"})

df = df[["Interval (ms)", "Voltage"]]
df.dropna(
    axis=0,
    how='any',
    subset=None,
    inplace=True
)

# pull out relevant dataframes
voltages = df["Voltage"]
intervals = df["Interval (ms)"]

# initialize state for tracking pulses
periods = pd.DataFrame({"Period (ms)": []})
times = pd.DataFrame({"Interval (ms)": []})
past_state = 0
past_time = -1

# at each new pulse, record time since last pulse (period)
for i in range(0, len(voltages) - 1):
    curr = filter(voltages.iloc[i], 1, 4)

    if (curr == 5):
        if (past_time < 0):
            past_state = 5
            past_time = intervals.iloc[i]

        elif(past_state == 0):
            period = intervals.iloc[i] - past_time
            periods.loc[len(periods.index)] = period
            times.loc[len(times.index)] = intervals.iloc[i]
            past_state = 5
            past_time = intervals.iloc[i]
    else:
        if (past_state == 5):
            past_state = 0

# transform period into RPM
# apply 10-index rolling average (check what timeframe is reasonable for your data)
# join with time dataframe and plot
periods.transform(lambda el: 60 / (el / 1000) / 12) \
       .rename(columns={"Period (ms)": "RPM"}) \
       .rolling(window = 10).mean() \
       .join(times) \
       .plot(x='Interval (ms)', y='RPM') \
       .get_figure().savefig("RPM_graph.pdf")
