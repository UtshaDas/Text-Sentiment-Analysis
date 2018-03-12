#import required tools and algorithms
from flask import Flask, redirect, url_for, request,abort
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names

# Construct an instance of Flask class for our webapp
app = Flask(__name__)

# URL '/' to be handled by main() route handler
@app.route('/success/<name>')
def success(name):
      
   #Input positive words from "positive.txt" file
   positive_vocab=[line.strip() for line in open("positive.txt", 'r')]
   #Input positive words from "positive.txt" file
   negative_vocab=[line.strip() for line in open("negative.txt", 'r')]
   #Input Neutral words
   neutral_vocab = [ 'movie','the','sound','was','is','actors','did','know','words','guy','person','man','boy','a' ]
   
   #Every word is converted into a feature using a simplified bag of words model
   def word_feats(words):
       return dict([(word, True) for word in words])
   positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
   negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
   neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]

   
   #Training set is then the sum of these three feature sets
   train_set = negative_features + positive_features + neutral_features

   #Train the classifier 
   classifier = NaiveBayesClassifier.train(train_set) 

   # Initialization of negitive and positive counter 
   neg = 0
   pos = 0

   #initialization
   index = 0
   found = 0

   #name contains the input comment , store it to sentence for analysis
   sentence=name

   #searching in positive_vocab
   for word in positive_vocab:
      if (sentence == positive_vocab[index]):
         found +=1
      index+=1
   #searching in negative_vocab
   index=0
   for word in negative_vocab:
      if (sentence == negative_vocab[index]):
         found+=1
      index+=1
   #for successful search  
   if (found >= 1):
      #make the sentence in lowercase
      sentence = sentence.lower()
      #split the words of sentence
      words = sentence.split(' ')
      #calculation using classifier algorithm
      for word in words:
         classResult = classifier.classify( word_feats(word))
         if classResult == 'neg':
            neg = neg + 1
         if classResult == 'pos':
            pos = pos + 1
      #ouput the result      
      return 'Negative: %s' % str(float(neg)/len(words)) + ' \r\n           .......Positive: %s' % str(float(pos)/len(words))
   
   #unsuccessful search
   if(found == 0):
      #make the sentence lowercase
      sentence = sentence.lower()
      #split the words of sentence
      words = sentence.split(' ')
      #calculation using classifier algorithm
      for word in words:
         classResult = classifier.classify( word_feats(word))
         if classResult == 'neg':
            neg = neg + 1
         if classResult == 'pos':
            pos = pos + 1
      #output the result     
      return 'Negative: %s' % str(float(neg)/len(words)) + ' \r\n           ........Positive: %s' % str(float(pos)/len(words))
      
#User input comment
# First request via POST, subsequent requests via GET
@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      # get(attr) returns None if attr is not present
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

# Script executed directly?
if __name__ == '__main__':
   # Launch built-in web server and run this Flask webapp
   app.run()
