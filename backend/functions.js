async function serpApiSearch(query, apiKey, options = {}) {
    const { getJson } = require('serpapi');
    
    const defaultOptions = {
        region: 'us-en',
        maxResults: 5
    };

    const searchOptions = { ...defaultOptions, ...options };

    return new Promise((resolve, reject) => {
        getJson({
            engine: 'duckduckgo',
            q: query,
            kl: searchOptions.region,
            api_key: apiKey
        }, (json) => {
            if (json.error) {
                reject(new Error(json.error));
                return;
            }

            try {
                // Extract organic results
                const results = (json.organic_results || [])
                    .slice(0, searchOptions.maxResults)
                    .map(result => ({
                        title: result.title || '',
                        url: result.link || '',
                        snippet: result.snippet || ''
                    }));

                if (results.length === 0) {
                    resolve([{
                        title: 'No results found',
                        url: '',
                        snippet: ''
                    }]);
                    return;
                }

                resolve(results);
            } catch (error) {
                reject(new Error(`Failed to process results: ${error.message}`));
            }
        });
    });
}

// Example usage
async function main() {
        try {
        // Replace 'YOUR_API_KEY' with your actual SerpApi key
        const apiKey = '11273a8046c26dedf404c4fc02c3fc0ecc0fd50a3f25373ac344c4ab2044a176';
        
        const results = await serpApiSearch('anthropic claude', apiKey, {
            maxResults: 3,
            region: 'us-en'
        });
        
        console.log(JSON.stringify(results, null, 2));
    } catch (error) {
        console.error('Search error:', error.message);
    }
}

// Only run if this is the main module
if (require.main === module) {
    main();
}

module.exports = { serpApiSearch };