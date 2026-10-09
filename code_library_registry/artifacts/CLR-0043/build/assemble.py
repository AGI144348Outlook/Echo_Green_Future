"""Assemble the published page: inline starter.json and grammar.js into the template.
Run from this folder: python3 build/assemble.py  -> index.html
Data files published beside the page (regenerate with build/*.py, WordNet 3.0 via NLTK):
  data/wordnet-full.b64.txt  base64 of gzip(full dataset JSON)
  data/lexicon.b64.txt       base64 of gzip(word<TAB>pos-set lines)
  pyodide/*                  Pyodide 0.26.4 core from npm; python_stdlib.zip served as python_stdlib.b64.txt
"""
import json
t=open('lexicon_registry.template.html').read()
st=json.dumps(json.load(open('starter.json')),separators=(',',':')).replace('</','<\\/')
g=open('grammar.js').read().replace('</','<\\/')
open('index.html','w').write(t.replace('/*STARTER*/',st).replace('/*GRAMMAR*/',g))
print('index.html written')
