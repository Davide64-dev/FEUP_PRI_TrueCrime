import subprocess
import os

def query_solr(query_path, output_path):
    # python3 ./scripts/query_solr.py --query {query_path} --uri http://localhost:8983/solr --collection /
    # true_crime | python3 ./scripts/solr2trec.py > {output_path}

    query_solr_path = os.path.join(os.path.dirname(__file__), 'scripts/query_solr.py')
    solr2trec_path = os.path.join(os.path.dirname(__file__), 'scripts/solr2trec.py')

    # Check if solr2trec.py exists
    if not os.path.isfile(solr2trec_path):
        raise FileNotFoundError(f"{solr2trec_path} not found. Please check the path.")

    # Check if query_solr.py exists
    if not os.path.isfile(query_solr_path):
        raise FileNotFoundError(f"{query_solr_path} not found. Please check the path.")

    # Query Solr
    query = f"python3 {query_solr_path} --query {query_path} --uri http://localhost:8983/solr --collection true_crime"
    query_output = subprocess.check_output(query, shell=True).decode('utf-8')
    
    solr2trec = f"python3 {solr2trec_path}"

    # Convert Solr output to TREC format, passing query output via stdin
    trec_output = subprocess.check_output(solr2trec.split(), input=query_output.encode('utf-8')).decode('utf-8')

    # Save TREC output
    with open(output_path, 'w') as file:
        file.write(trec_output)

    return trec_output

def cleanup_results(results_path):
    ## results format
    # 0 Q0 ['lrO42okQeck'] 1 11.038336 run0
    # 0 Q0 ['EyR1BfzL36M'] 2 9.902887 run0
    # 0 Q0 ['iSOWYnG9QoQ'] 3 9.618229 run0

    ## desired format
    # 0 Q0 lrO42okQeck 1 11.038336 run0
    # 0 Q0 EyR1BfzL36M 2 9.902887 run0
    # 0 Q0 iSOWYnG9QoQ 3 9.618229 run0

    with open(results_path, 'r') as file:
        lines = file.readlines()

    cleaned_lines = []

    for line in lines:
        parts = line.split()
        video_id = parts[2].strip("[]")
        video_id = video_id.replace("'", "")
        cleaned_line = f"{parts[0]} {parts[1]} {video_id} {parts[3]} {parts[4]} {parts[5]}\n"
        cleaned_lines.append(cleaned_line)

    with open(results_path, 'w') as file:
        file.writelines(cleaned_lines)

    return cleaned_lines

def remove_duplicates(results_path):
    with open(results_path, 'r') as file:
        lines = file.readlines()

    seen_video_ids = set()
    unique_lines = []

    for line in lines:
        parts = line.split()
        video_id = parts[2]

        if video_id not in seen_video_ids:
            seen_video_ids.add(video_id)
            unique_lines.append(line)

    with open(results_path, 'w') as file:
        file.writelines(unique_lines)

    return unique_lines


def evaluate_results(qrels_path, results_path):
    # ../src/trec_eval/trec_eval {qrels_path} {results_path}

    trec_eval = f"../src/trec_eval/trec_eval {qrels_path} {results_path}"
    eval_output = subprocess.check_output(trec_eval, shell=True).decode('utf-8')

    return eval_output

def plot_results(results_path, qrels_path, output_path):
    # cat {results_path} | python3 ./scripts/plot_pr.py --qrels {qrels_path} --output {output_path}

    plot_pr_path = os.path.join(os.path.dirname(__file__), 'scripts/plot_pr.py')

    plot_pr = f"cat {results_path} | python3 {plot_pr_path} --qrels {qrels_path} --output {output_path}"
    plot_output = subprocess.check_output(plot_pr, shell=True).decode('utf-8')

    return plot_output

if __name__ == "__main__":
    ## paths to queries
    query_paths = ['queries/murder.json']

    ## paths to queries results
    query_results_paths = ['results/results_trec_murders.txt']

    ## path to qrels in trec format
    qrels_trec_paths = ['qrels_trec/qrels_trec_murders.txt']

    ## path to output of trec_eval
    eval_output_paths = ['eval_output/eval_output_murders.txt']

    ## path to output of graphs
    plot_output_paths = ['graphs/murders.png']

    for query_path, query_results_path, qrels_trec_path, eval_output_path, plot_output_path in zip(query_paths, query_results_paths, qrels_trec_paths, eval_output_paths, plot_output_paths):
        query_solr(query_path, query_results_path)
        cleanup_results(query_results_path)
        remove_duplicates(query_results_path)
        eval_output = evaluate_results(qrels_trec_path, query_results_path)

        with open(eval_output_path, 'w') as file:
            file.write(eval_output)
        
        plot_results(query_results_path, qrels_trec_path, plot_output_path)
    
        print(f"Saved evaluation output to {eval_output_path}")
        print(f"Saved plot output to {plot_output_path}")