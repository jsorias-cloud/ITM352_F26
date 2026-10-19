# Program to remove any scores from a list that are below 50.
 
scores = [60, 45, 30, 85, 10, 90]

#created a function to be able to remove the scores without skipping over any numbers

def removeScore (scores):
    scoresToReturn = scores.copy()
    for score in scores:
         if score < 60:
             scoresToReturn.remove(score)
    return scoresToReturn


print(removeScore(scores))
