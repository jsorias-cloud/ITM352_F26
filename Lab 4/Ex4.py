# Try to append to a tuple. It won't work. 
# Name: Jorryn Orias 
# Date: Sept. 16, 2026

survey_respondents = (1012, 1035, 1021, 1053)
#survey_respondents.append(1054)  # This will raise an AttributeError since tuples are immutable

survey_respondents = survey_respondents + (1054,)  # This creates a new tuple with the additional element
print("Updated survey respondents:", survey_respondents)

