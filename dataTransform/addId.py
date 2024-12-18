import json

def add_id_to_documents(documents):
    for i, doc in enumerate(documents):
        doc['id'] = i
    return documents

def flatten_comments(documents):
    for doc in documents:
        comments = []
        for comment in doc['comments']:
            if(comment['comment']):
                comments.append(comment['comment'])
            
            if 'replies' in comment:
                for reply in comment['replies']:
                    comments.append(reply)
        doc['comments'] = comments

    return documents


if __name__ == "__main__":
    ## read ../dataset/true_crime_semantics.json
    ## write ../dataset/true_crime_semantics_with_id.json

    json_path = '../dataset/true_crime_semantics.json'
    documents = None
    with open(json_path, 'r') as file:
        documents = json.load(file)

    add_id_to_documents(documents)

    with open('../dataset/true_crime_semantics_with_id.json', 'w') as file:
        json.dump(documents, file, indent=2)

    json_path = '../dataset/true_crime_semantics_with_id.json'
    documents = None
    with open(json_path, 'r') as file:
        documents = json.load(file)
    
    documents = flatten_comments(documents)

    with open('../dataset/true_crime_semantics_with_id.json', 'w') as file:
        json.dump(documents, file, indent=2)