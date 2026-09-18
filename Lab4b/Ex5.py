# Ask the user for a sentence (using input()).
# Turn the sentence into a list of strings (using split()).
# Reverse the list. 
# Join the list back into a string (using join()).
# Name: Jorryn Orias
# Date: September 18, 2026

sentence = input("Enter a sentence: ")
words = sentence.split()
words.reverse()
reversed_sentence = " ".join(words)
print("Reversed sentence is:", reversed_sentence)

joined_sentence = sentence + " " + reversed_sentence
print("Joined sentence is:", joined_sentence)

