# Backend for Gutenberg-Search

## Available Scripts

### `python3 manage.py fetch_data --n 1664` 

set up the DataBase with books and keywords but super long, you should stop at 100 to test (approx. 2h).


### `python3 manage.py get_graph`

sets up the Jaccard's graph.

### `python3 manage.py centrality`

calculate for each book its centrality in the graph.
