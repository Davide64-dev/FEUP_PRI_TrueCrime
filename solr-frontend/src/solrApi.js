import axios from 'axios';

const solrBaseUrl = "http://localhost:8983/solr/true_crime/select";

export const fetchResults = async (query) => {
    try {
        const response = await axios.get(solrBaseUrl, {
            params: {
                q: query,        
                wt: 'json'
            },
        });
        console.log(response);
        return response.data.response.docs;
    } catch (error) {
        console.error("Error fetching results from Solr:", error);
        throw error;
    }
};