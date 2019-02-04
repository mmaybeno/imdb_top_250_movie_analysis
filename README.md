# IMDB Top 250 Movie With Wikipedia Revisions Analysis
## Get started
* Requirements
    * python3.6
    * pipenv or pip
  
* Install python packages
    ```
    pipenv install --python 3.6 --skip-lock
    # or
    pip install -r requirements.txt
    ```
* Generate dataset (if you want latest data)
    ```
    pipenv run python generate_dataset.py
    # or if in pipenv shell or used only pip
    python generate_dataset.py
    ```
* Start jupyter notebook
    ```
    pipenv run jupyter notebook imdb_top_250_movies_wikipedia_revisions_analysis.ipynb
    # or if in pipenv shell or used only pip
    jupyter notebook imdb_top_250_movies_wikipedia_revisions_analysis.ipynb
    ```
* Backup notebook results as PDF
    ```
    ./files/imdb_top_250_movies_wikipedia_revisions_analysis.pdf
    ```