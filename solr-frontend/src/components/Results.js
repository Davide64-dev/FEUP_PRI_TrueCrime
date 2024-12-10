const Results = ({ results }) => {
    return (
        <div>
            {results.length > 0 ? (
                results.map((result, index) => (
                    <div key={index}>
                        <h3>{result.title || "No Title"}</h3>
                        <p>{result.description || "No Description"}</p>
                    </div>
                ))
            ) : (
                <p>No results found.</p>
            )}
        </div>
    );
};
export default Results;
