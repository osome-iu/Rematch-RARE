import pandas as pd
import os

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Complexity Plot")
    parser.add_argument('-dp','--datapath', metavar = 'data path', type = str,help = 'Data Path',default = 'data/processed/AMR3.0/')
    parser.add_argument('-m','--mode', metavar = 'mode', type = str, help = 'If smatch/sembleu/rematch etc', default = 'rematch')
    args = parser.parse_args()
    metric_data = pd.read_csv(os.path.join(args.datapath, f"all_unwiki_500k_1_{args.mode}_data.csv"))
    print(f"Total time taken to execute the testbed =  {sum(metric_data['time'])} seconds")