# Text Sentiment Analysis

A small web application, written in Python with **Flask** and **NLTK**, that tells you whether a comment is positive or negative. You type a comment into a web page. The app scores it with a **Naive Bayes classifier** trained on lists of positive, negative and neutral words, and shows the share of the comment that reads as negative and as positive.

This was built as a student project at Rajshahi University of Engineering & Technology (RUET). The full write-up is in [`A Web Application of Text Sentiment Analysis.pdf`](A%20Web%20Application%20of%20Text%20Sentiment%20Analysis.pdf).

---

## How it works

```
login.html  ──POST /login──▶  Flask (login.py)  ──redirect──▶  /success/<comment>
 (comment form)                                                  │
                                                                 ▼
                                    Train Naive Bayes on positive.txt,
                                    negative.txt + a built-in neutral list
                                                                 │
                                                                 ▼
                                    Lower-case the comment, split it into words,
                                    classify each word as pos / neg / neu
                                                                 │
                                                                 ▼
                                    Return the share of negative and positive words
```

1. **Input.** `login.html` is a simple form that posts the comment (field `nm`) to `http://localhost:5000/login`.
2. **Routing.** The `/login` route reads the comment and redirects to `/success/<comment>`.
3. **Training.** The `/success` route loads the vocabularies:
   - `positive.txt`: positive words (e.g. *awesome, outstanding, good*)
   - `negative.txt`: negative words (e.g. *bad, terrible, useless*)
   - a short neutral list in the code (*movie, the, sound, was, is, actors, ...*)

   Each entry becomes a feature set through a simple bag-of-words function (`word_feats`). The three sets are combined into one training set for NLTK's `NaiveBayesClassifier`.
4. **Prediction.** The comment is lower-cased and split on spaces. Each word is classified as `pos`, `neg` or `neu`.
5. **Output.** The page shows the fraction of words classified as negative and as positive:

   ```
   Negative: 0.0  .......Positive: 0.25
   ```

   Values range from `0` to `1`. Words classified as neutral count toward the total but are not shown, so the two numbers don't always add up to 1.

---

## Project structure

| File | Purpose |
|------|---------|
| `login.py` | The Flask app: routes, training the classifier and scoring the comment |
| `login.html` | The front-end form for typing a comment |
| `login.txt` | A plain-text copy of `login.html` |
| `positive.txt` | Positive word list, one word per line |
| `negative.txt` | Negative word list, one word per line |
| `A Web Application of Text Sentiment Analysis.pdf` | Project report: method, experiments and results |

---

## Requirements

- Python 3
- [Flask](https://flask.palletsprojects.com/)
- [NLTK](https://www.nltk.org/)

---

## Installation

```bash
git clone https://github.com/UtshaDas/Text-Sentiment-Analysis.git
cd Text-Sentiment-Analysis
pip install flask nltk
```

> **Note:** The app uses only NLTK's `NaiveBayesClassifier`, which needs no downloaded corpora, so you don't have to run `nltk.download()`. If NLTK ever asks for a missing resource, run `python -c "import nltk; nltk.download()"` and install the package it names.

---

## Usage

1. **Start the server** from inside the project folder. The app opens `positive.txt` and `negative.txt` by relative path, so it must be run from there:

   ```bash
   python login.py
   ```

   Flask starts on `http://localhost:5000`.

2. **Open `login.html`** in your web browser (double-click it, or drag it into a browser window).

3. **Type a comment** in the box and click **submit**. The result opens in the browser.

You can also skip the form and send a request directly:

```
http://localhost:5000/login?nm=the movie was awesome
```

---

## Results

In the project report, accuracy was measured by entering comments by hand and checking each prediction:

| No. of input comments | Accuracy (%) |
|:---------------------:|:------------:|
| 10 | 60 |
| 20 | 68 |
| 30 | 63 |
| 40 | 65 |

---

## Known limitations

- **Character-level features.** `word_feats` loops over each word, which in Python means looping over its *letters*. The classifier therefore learns from the letters in each word, not from whole words, which keeps accuracy modest. Changing `word_feats(word)` to `word_feats([word])` in training and prediction would make it work on whole words.
- **Retrained on every request.** The classifier is rebuilt each time a comment is submitted. Training it once at startup would make responses faster.
- **Comment travels in the URL.** The comment is passed as part of the `/success/<comment>` path, so comments containing `/` return a 404 error.
- **Blank lines in word lists.** `positive.txt` and `negative.txt` have blank lines between words. They become empty training examples and should be filtered out.
- **Simple tokenization.** Words are split on spaces only, so punctuation stays attached (e.g. `good!` is not matched as `good`). Negation (*not good*) is not handled.
- **Fixed address.** `login.html` posts to `http://localhost:5000`. If you change the host or port, update the form's `action` too.

---

## Possible improvements

- Fix the feature extraction and train once at startup.
- Pass the comment in the request body or a query string instead of the URL path.
- Serve the form from Flask (`render_template`) instead of opening a separate HTML file.
- Use NLTK's tokenizer and a labelled dataset (e.g. `movie_reviews`), or a lexicon-based analyzer such as VADER, for better accuracy.

---

## Author

**Utsha Das**, Department of Computer Science and Engineering, RUET (Roll: 143034)
Supervised by **Biprodip Pal**, Assistant Professor, Department of CSE, RUET

## Acknowledgements

- [Practical Flask Introduction, pythonprogramming.net](https://pythonprogramming.net/practical-flask-introduction/)
- [Tokenizing Words and Sentences with NLTK, pythonprogramming.net](https://pythonprogramming.net/tokenizing-words-sentences-nltk-tutorial/)
- [Bag of Words, pythonprogramminglanguage.com](https://pythonprogramminglanguage.com/bag-of-words/)
