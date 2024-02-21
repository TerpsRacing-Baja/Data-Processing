import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Carve up RaceCapture CSV files")
parser.add_argument('filename')
parser.add_argument('start_interval', type=int)
parser.add_argument('end_interval', type=int)
args = parser.parse_args()

df = pd.read_csv(args.filename)
df = df[df["Interval|\"ms\"|0|0|1"] >= args.start_interval]
df = df[df["Interval|\"ms\"|0|0|1"] <= args.end_interval]

write_name = str(args.start_interval) + "_" + str(args.end_interval) + "_" + args.filename

df.to_csv(write_name)