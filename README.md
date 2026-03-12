# Analyzing-Attributes-of-AI-Generated-vs.-Human-Written-Text

This dataset contains ~1000 of AI-generated vs. human-written text, as well as values like author type (AI vs. human), model source (human, ChatGPT, Claude, etc.).

https://www.kaggle.com/datasets/prince7489/ai-vs-human-comparison-datasetLinks to an external site.

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

