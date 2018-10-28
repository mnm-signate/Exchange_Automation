Exchage_Automation
============================

仮想通貨取引自動化プログラム

Project Organization
------------

    â”œâ”€â”€ LICENSE
    â”œâ”€â”€ Makefile           <- Makefile with commands like `make data` or `make train`
    â”œâ”€â”€ README.md          <- The top-level README for developers using this project.
    â”œâ”€â”€ data
    â”‚Â Â  â”œâ”€â”€ external       <- Data from third party sources.
    â”‚Â Â  â”œâ”€â”€ interim        <- Intermediate data that has been transformed.
    â”‚Â Â  â”œâ”€â”€ processed      <- The final, canonical data sets for modeling.
    â”‚Â Â  â””â”€â”€ raw            <- The original, immutable data dump.
    â”‚
    â”œâ”€â”€ docs               <- A default Sphinx project; see sphinx-doc.org for details
    â”‚
    â”œâ”€â”€ models             <- Trained and serialized models, model predictions, or model summaries
    â”‚
    â”œâ”€â”€ notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    â”‚                         the creator's initials, and a short `-` delimited description, e.g.
    â”‚                         `1.0-jqp-initial-data-exploration`.
    â”‚
    â”œâ”€â”€ references         <- Data dictionaries, manuals, and all other explanatory materials.
    â”‚
    â”œâ”€â”€ reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    â”‚Â Â  â””â”€â”€ figures        <- Generated graphics and figures to be used in reporting
    â”‚
    â”œâ”€â”€ requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    â”‚                         generated with `pip freeze > requirements.txt`
    â”‚
    â”œâ”€â”€ setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    â”œâ”€â”€ src                <- Source code for use in this project.
    â”‚Â Â  â”œâ”€â”€ __init__.py    <- Makes src a Python module
    â”‚   â”‚
    â”‚Â Â  â”œâ”€â”€ data           <- Scripts to download or generate data
    â”‚Â Â  â”‚Â Â  â””â”€â”€ make_dataset.py
    â”‚   â”‚
    â”‚Â Â  â”œâ”€â”€ features       <- Scripts to turn raw data into features for modeling
    â”‚Â Â  â”‚Â Â  â””â”€â”€ build_features.py
    â”‚   â”‚
    â”‚Â Â  â”œâ”€â”€ models         <- Scripts to train models and then use trained models to make
    â”‚   â”‚   â”‚                 predictions
    â”‚Â Â  â”‚Â Â  â”œâ”€â”€ predict_model.py
    â”‚Â Â  â”‚Â Â  â””â”€â”€ train_model.py
    â”‚   â”‚
    â”‚Â Â  â””â”€â”€ visualization  <- Scripts to create exploratory and results oriented visualizations
    â”‚Â Â      â””â”€â”€ visualize.py
    â”‚
    â””â”€â”€ tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

# 用語
- 買い残高：信用取引によって買い付けた場合の、まだ決済（お金の返済）されずに残っている額。
- 売り残高：信用売りされたまま、まだ決済されずに残っている金額。
- ポジション：買い残高と売り残高の”どちらが多いのか（傾き）”を表す金融専門用語です。例えば自分が米ドル円を「買いで10万通貨」「売りで5万通貨」もっていた場合, 自分のドル円ポジションは『買いポジションorロングポジション』となる。

