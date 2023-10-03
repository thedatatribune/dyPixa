## import lib
from transformers import pipeline

## setting env
MODEL_NAME = "SamLowe/roberta-base-go_emotions" 
classifier = pipeline(task="text-classification", model=MODEL_NAME, top_k=None)

## prediction function | returns dict. that could be taken as JSON
def findEmotions(data_to_pred: str):
  gotEmotions = classifier(data_to_pred) 
  return gotEmotions