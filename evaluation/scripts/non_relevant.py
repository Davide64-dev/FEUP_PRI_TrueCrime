def add_non_relevant(result_trec_path, qrels_trec_path):
    result_trec_lines = []
    with open(result_trec_path, 'r') as file:
        result_trec_lines = file.readlines()

    qrels_trec_lines = []
    with open(qrels_trec_path, 'r') as file:
        qrels_trec_lines = file.readlines()

    qrels_trec_videos = []
    for line in qrels_trec_lines:
        parts = line.split()
        qrels_trec_videos.append(parts[2])

    non_relevant_lines = []
    for line in result_trec_lines:
        parts = line.split()
        video_id = parts[2]
        if video_id not in qrels_trec_videos:
            non_relevant_lines.append(line)
    
    ## truncate non relevant lines at 20
    non_relevant_lines = non_relevant_lines[:20]
    with open(qrels_trec_path, 'a') as file:
        for line in non_relevant_lines:
            file.write(f"0 0 {line.split()[2]} 0\n")
    
    return

if __name__ == "__main__":
    ## paths to queries results
    query_results_paths = ['results/results_trec_murders.txt',
                           'results/results_trec_nineties.txt',
                           'results/results_trec_serial.txt',
                           'results/results_trec_unsolved.txt']
    
    ## path to qrels in trec format
    qrels_trec_paths = ['qrels_trec/qrels_trec_murders.txt',
                        'qrels_trec/qrels_trec_nineties.txt',
                        'qrels_trec/qrels_trec_serial.txt',
                        'qrels_trec/qrels_trec_unsolved.txt']
    
    for query_results_path, qrels_trec_path in zip(query_results_paths, qrels_trec_paths):
        add_non_relevant(query_results_path, qrels_trec_path)

    print("Done")