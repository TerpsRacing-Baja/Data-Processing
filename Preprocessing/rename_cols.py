import pandas as pd
import argparse
import os

def removeQuotes(col):
    return col.replace('\"', '')

# python3 rename_cols filename -q

parser = argparse.ArgumentParser(description="Rename data columns according to argument inputs")
parser.add_argument('filename')
parser.add_argument('-q', '--quotes', type=bool)
parser.add_argument('-1', '--an1', type=str)
parser.add_argument('-2', '--an2', type=str)
parser.add_argument('-3', '--an3', type=str)
parser.add_argument('-4', '--an4', type=str)
parser.add_argument('-5', '--an5', type=str)
parser.add_argument('-6', '--an6', type=str)
parser.add_argument('-7', '--an7', type=str)
parser.add_argument('-8', '--an8', type=str)
parser.add_argument('-s', '--sampling', type=str, default='200')
args = parser.parse_args()

df = pd.read_csv(args.filename) \
       .rename(columns={"Interval|\"ms\"|0|0|1" : "Interval (ms)",
                        "Analog1|\"Volts\"|0.0|5.0|" + args.sampling : args.an1 or "Analog1|\"Volts\"|0.0|5.0|" + args.sampling,
                        "Analog2|\"Volts\"|0.0|5.0|" + args.sampling : args.an2 or "Analog2|\"Volts\"|0.0|5.0|" + args.sampling,
                        "Analog3|\"Volts\"|0.0|5.0|" + args.sampling : args.an3 or "Analog3|\"Volts\"|0.0|5.0|" + args.sampling,
                        "Analog4|\"Volts\"|0.0|5.0|" + args.sampling : args.an4 or "Analog4|\"Volts\"|0.0|5.0|" + args.sampling,
                        "Analog5|\"Volts\"|0.0|5.0|" + args.sampling : args.an5 or "Analog5|\"Volts\"|0.0|5.0|" + args.sampling,
                        "Analog6|\"Volts\"|0.0|5.0|" + args.sampling : args.an6 or "Analog6|\"Volts\"|0.0|5.0|" + args.sampling,
                        "Analog7|\"Volts\"|0.0|5.0|" + args.sampling : args.an7 or "Analog7|\"Volts\"|0.0|5.0|" + args.sampling,
                        "Analog8|\"Volts\"|0.0|5.0|" + args.sampling : args.an8 or "Analog8|\"Volts\"|0.0|5.0|" + args.sampling
                        })

if(args.quotes):
    df_list = df.columns.to_list()
    for col in df_list:
       df.rename(columns = {col : removeQuotes(col)})


write_name = 'RENAMED_COLS_' + os.path.basename(args.filename)
df.to_csv(write_name)