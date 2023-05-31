# Flask Backend
Using Flask to build a Restful API Server to serve Keras model for spam classification

## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Flask Application Structure 
```
.
├── README.md
├── __pycache__
│   └── app.cpython-310.pyc
├── app.py
├── image_classifier_model.h5
├── max_length.json
├── requirements.txt
├── text_classifier_model.h5
└── tokenizer.pickle
```

## Run Flask
### Run flask for develop
```
$ flask run
```
Default port is `5000`