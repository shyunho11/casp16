import os
import glob
import numpy as np
import subprocess
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

def calculate_tmscore(pdb_file1, pdb_file2):
    result = subprocess.run(['TMscore', pdb_file1, pdb_file2, '-c', '-ter', '0'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if line.startswith('TM-score'):
            return float(line.split()[2])
    return None

def find_optimal_clusters(data, max_k):
    silhouettes = []
    for k in range(2, max_k + 1):
        kmeans = KMeans(n_clusters=k, n_init='auto').fit(data)
        labels = kmeans.labels_
        score = silhouette_score(data, labels)
        silhouettes.append((k, score))
    
    optimal_k = max(silhouettes, key=lambda x: x[1])[0]
    return optimal_k

def main(directory, output_directory, max_clusters=10):
    pdb_files = glob.glob(os.path.join(directory, '*.pdb'))
    for i, pdb_file in enumerate(pdb_files):
        print(f'PDB {i}\t{os.path.basename(pdb_file)}')
        
    n = len(pdb_files)
    if n == 0:
        print("No PDB files found in the directory.")
        return
    
    tmscore_matrix = np.zeros((n, n))
    
    progress = 0
    
    for i in range(n):
        for j in range(i+1, n):
            tmscore_matrix[i, j] = calculate_tmscore(pdb_files[i], pdb_files[j])
            tmscore_matrix[j, i] = tmscore_matrix[i, j]
            progress += 1
            
            if progress % 1000 == 0:
                print(f'Calculated {progress}th TMscore: {tmscore_matrix[i, j]}')
        tmscore_matrix[i, i] = 1.0  # TM-score with itself is always 1.0
    
    # Create output directory
    os.makedirs(output_directory, exist_ok=True)

    np.savetxt(os.path.join(output_directory, 'tmscore_matrix.csv'), tmscore_matrix, delimiter=',')
    
    tsne = TSNE(n_components=2, metric='precomputed', init='random')
    tsne_result = tsne.fit_transform(1 - tmscore_matrix)  # TM-score is a similarity metric
    
    optimal_clusters = find_optimal_clusters(tsne_result, max_clusters)
    print(f'Optimal number of clusters: {optimal_clusters}')
    
    kmeans = KMeans(n_clusters=optimal_clusters, n_init='auto')
    labels = kmeans.fit_predict(tsne_result)
    
    for cluster_num in range(optimal_clusters):
        cluster_pdb_files = [pdb_files[i] for i in range(n) if labels[i] == cluster_num]
        with open(os.path.join(output_directory, f'cluster_{cluster_num + 1}.txt'), 'w') as f:
            for pdb_file in cluster_pdb_files:
                f.write(f'{os.path.basename(pdb_file)}\n')
        print(f'Cluster {cluster_num + 1} saved as {os.path.join(output_directory, f"cluster_{cluster_num + 1}.txt")}')
    
    plt.scatter(tsne_result[:, 0], tsne_result[:, 1], c=labels)
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.title(f'PDB Structure Clustering using t-SNE (optimal clusters={optimal_clusters})')
    plt.savefig(os.path.join(output_directory, 'tsne_plot.png'))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cluster PDB files based on structural similarity.")
    parser.add_argument("directory", type=str, help="Directory containing PDB files")
    parser.add_argument("output_directory", type=str, help="Output directory for results")
    parser.add_argument("--max_clusters", type=int, default=10, help="Maximum number of clusters to test for optimal number (default: 10)")
    
    args = parser.parse_args()

    main(args.directory, args.output_directory, args.max_clusters)
