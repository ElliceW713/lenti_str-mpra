import pandas as pd

def replace_adaptor():
    input_csv = input("STR oligo design file: ")
    old_adapter = "ACTGGCCGCTTGACG"
    lenti_adapter = "AGGACCGGATCAACT"

    text = open(input_csv, "r")
    text = ''.join([i for i in text]) \
        .replace(old_adapter, lenti_adapter)
    x = open("output.csv","w")
    x.writelines(text)
    x.close()

def split_adaptor():
    old_adapter = "ACTGGCCGCTTGACG"

    df = pd.read_csv('/Users/user/Desktop/round1_probe_seq.tsv', sep='\t')
    df[['adapter', 'STR']] = df.short_tandem_repeat.str.split(old_adapter,
                                                                expand=True)
    df = df.assign(adapter = old_adapter)
    df[['STR', 'filler']] = df.STR.str.split("CACTGCGGCTCCTGCGATCGC", expand=True)
    df.insert(4, "AsiSI", 'CACTGCGGCTCCTGCGATCGC')

    df[['filler', 'BsaI_cut']] = df.filler.str.split("GGTCTC", expand = True)
    df.insert(6, "BsaI_recog", "GGTCTC")
    
    df['check'] = df['adapter'].str.cat(df.STR).str.cat(df.AsiSI).str.cat(df.filler).str.cat(df.BsaI_recog).str.cat(df.BsaI_cut)

    df['compare'] = (df['check'] == df['short_tandem_repeat'])

    df.to_csv("split.csv")

def main():
    replace_adaptor()
    split_adaptor()

if __name__=="__main__": 
    main() 
