# Step Challenge
# Three friends tracked their daily steps for one week.
# This program is supposed to:
#  1. Compute each person's average daily steps.
#  2. Award a badge based on that average:
#        Gold   - an average of 10,000 steps or more
#        Silver - an average of 7,500 steps or more
#        Bronze - anything less
#  3. Print a summary line for each person.


weekly_steps = {
   "Kai":     [8000, 9500, 7200, 11000, 6800, 12000, 9000],
   "Leilani": [12000, 9000, 10500, 8500, 11000, 9500, 9500],
   "Noa":     [4000, 5200, 3800, 6100, 4500, 5000, 4400],
}


#gold needed to have >= since it includes 10000
def choose_badge(average):
   if average >= 10000:
       return "Gold"
   elif average >= 7500:
       return "Silver"
   else:
       return "Bronze"


def average(steps):
    total = 0
    for name in weekly_steps:
       days = weekly_steps[name]
    for steps in days:
       total += steps


#total needed to be in the for loop to reset the total for each person
# to 0 or it would just keep adding to the previous total

for name in weekly_steps: 
    total = 0
    days = weekly_steps[name]
    for steps in days:
        total += steps
    avg = total / len(days)
    badge = choose_badge(avg)
    print(f"{name} averaged {avg:.2f} steps per day and earned a {badge} badge.")