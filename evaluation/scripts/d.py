def read_results(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def remove_duplicates(lines):
    seen_video_ids = set()
    unique_lines = []
    
    for line in lines:
        parts = line.split()
        video_id = parts[2]
        
        if video_id not in seen_video_ids:
            seen_video_ids.add(video_id)
            unique_lines.append(line)
    
    return unique_lines

def save_results(lines, file_path):
    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    file_paths = ['results_trec_murders.txt']
    
    for file_path in file_paths:
        lines = read_results(file_path)
        unique_lines = remove_duplicates(lines)
        save_results(unique_lines, file_path)
        
        print(f"Removed duplicates and saved {len(unique_lines)} unique lines back to {file_path}")