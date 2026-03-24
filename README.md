# Analyzing-Attributes-of-AI-Generated-vs.-Human-Written-Text

This dataset contains ~500 rows of AI-generated vs. human-written text, as well as values like author type (AI vs. human), model source (human, ChatGPT, Claude, etc.):

https://www.kaggle.com/datasets/prince7489/ai-vs-human-comparison-dataset

In this project, we will set out to see if we can identify subtle statistical fingerprints (like word variety and sentence structure) that distinguish AI writing from human writing and further see if we can distinguish writing styles among different LLMs.

## Analytics Questions 

- On average, are AI or human written texts more complex? (e.g. rare vocabulary)
- Does the plagiarism score meaningfully separate AI from human written texts?
- Do humans show more irregularity when writing? (e.g. do the number of unique words and sentence length vary within the same text?)


## How to Run

First, you should probably be in a virtual environment. Make sure you are in the root directory. i.e., for dummies, that is the highest highest highest level folder (it contains the README.md) Then, set that up using
```
python3 -m venv .venv
```
or for windows
```
python -m venv .venv
```

then activate that with
```
source .venv/bin/activate
```
or for windows... (command prompt)
```
.venv\Scripts\activate
```
(for powershell instead)
```
.venv\Scripts\Activate.ps1
```

then do
```
pip install -r requirements.txt
```

finally, run 
```
python src/setup_pipeline.py
```

after that command finishes, you should be ready to do your analysis questions!!! :DDDD the mysql in docker should have the clean data. check the compose.yaml or load_to_mysql.py file for examples on how to access the database.

## Connecting PowerBI to MySQL Database

## Install MySQL Connector

Power BI requires a specific MySQL driver.

If you see **"Components not installed"**, do this:
1. **Uninstall** any existing *MySQL Connector/NET*
2. **Download version `8.0.28`**:
   [https://downloads.mysql.com/archives/c-net/](https://downloads.mysql.com/archives/c-net/)

   > Use **8.0.28 only**
   > Versions **9.x** or **8.0.33+** often cause *"Error State 18"*

3. Run installer:

   * Choose Complete setup (not Typical)

4. Restart your computer

5. Start the database (either in VS Code or Docker Desktop):

docker-compose up -d

## Connect Power BI to MySQL

1. Open Power BI Desktop
2. Click Get Data → MySQL database
3. Enter:

   * **Server:** `127.0.0.1:3367`
   * **Database:** `clean_data`

4. Authentication:

   * Select **Database**
   * **Username:** `root`
   * **Password:** `rootpassword`


