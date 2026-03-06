#Asking for input from the user about a ski pass purchase
skipass=input("Enter the ski pass you wish to purchase this year (Epic, Ikon, Backountry, or none)")
# The if statements below evalutes the ski pass inputted based on if text and runs until one of the conditions is true
# if none of the conditions are true it assumes that the user did not buy a ski pass. (premise set in input question)
if "pic" in skipass:
    print ("Great choice, Epic is the best in CO") #If the ski pass has "pic" in it, it signifies "Epic" and not case sensitive
elif "kon" in skipass:
    print("I would suggested looking into Epic") #If the ski pass has "kon" in it, it signifies "Ikon" and not case sensitive
    print (" Here is the link for you: https://www.epicpass.com/region/region-overview.aspx")
elif "ackcountry" in skipass:
    print(" That is the most fun option, see you out there!") #If the ski pass has "ackcountry" in it, it signifies "Backcountry" and not case sensitive
else: 
    print ("You sure you don't want to ski this year?") # This assumes no other ski passes from the premise of the question

# This chain of events calculates the number of powder days the user had
# the input requires an input from the user on how much snow they had on their snow days. 
Snow_fall_vail_in = input("Enter the amount of snow that fell on your snow days in inches (integers seperated by comas)")
# This splits the user intput from a string to a list
snow_lst=(Snow_fall_vail_in.split(","))
# This this is an empty list to store the results of the loop below
num_snowy_days_lst=[]
# the loop below uses converts the numbers in the list from strings to integers, and stores them in a list if the number is greater than or equal to 6
for inches in snow_lst:
    if int(inches) >= 6.0:
        num_snowy_days_lst.append(int(inches))
#this counts the number of items in the list to give to the user
num_snowy_days=len(num_snowy_days_lst)
# This line prints a statement to show the number of powder days they had this year
print( "You had ", num_snowy_days, "powder days this year!")
