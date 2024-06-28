import pandas as pd
import argparse

# Function to read and process the log file
def process_log_file(file_path, rank_by_composite_file, rank_by_custom_file):
    data = {
        "id": [],
        "tm_io": [],
        "composite": [],
        "ptm": [],
        "i_ptm": [],
        "plddt": []
    }
    
    # Read the log file
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("tm_io"):
                parts = line.split()
                data["tm_io"].append(float(parts[1]))
                data["composite"].append(float(parts[3]))
                data["ptm"].append(float(parts[5]))
                data["i_ptm"].append(float(parts[7]))
                data["plddt"].append(float(parts[9]))
                data["id"].append(parts[11])
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Calculate the custom score
    def calculate_custom_score(row):
        if row["i_ptm"] == 0:
            return row["ptm"] * row["plddt"]
        else:
            return row["i_ptm"] * 0.8 + row["ptm"] * 0.2

    df["custom_score"] = df.apply(calculate_custom_score, axis=1).round(4)
    
    # Rank by composite score
    df_rank_composite = df.sort_values(by="composite", ascending=False).reset_index(drop=True)
    df_rank_composite.to_csv(rank_by_composite_file, index=False)
    print(f'Results saved as {rank_by_composite_file}')
    
    # Rank by custom score
    df_rank_custom = df.sort_values(by="custom_score", ascending=False).reset_index(drop=True)
    df_rank_custom.to_csv(rank_by_custom_file, index=False)
    print(f'Results saved as {rank_by_custom_file}')
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process log file and rank scores.")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument("--composite_output", default="RANK_BY_COMPOSITE.csv", help="Output file for ranking by composite score")
    parser.add_argument("--custom_output", default="RANK_BY_CUSTOM_SCORE.csv", help="Output file for ranking by custom score")
    
    args = parser.parse_args()
    
    process_log_file(args.log_file, args.composite_output, args.custom_output)