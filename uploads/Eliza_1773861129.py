import re
##### globals#######

# Define substitution rules as a list of tuples (pattern, response)

# Welcome to the Mariah Carey Mix Tape --- Obsessed
'''
I had the orginal ELiza code but I just didn't like how sad it was. So, when I saw that it could be open ended on Piazza,
I thought I would make it into a song. Enjoy!

I found this method uses more of the operations we used barring capture groups

'''

#substitution for the lines I see the song as a conversation between two people.
substitution_rules = [
    (r'(.*)So, ?oh, ?oh, ?oh, ?oh(.*)', r'hey, hey, hey'),
    (r'(.*)W?hy are you obsessed(.*)', r'Girl all I wanna know'),
    (r'(.*)So, oh(.*)', r'oh oh oh ohhh'),
    (r'(.*)all up in the blogs(.*)', r'say we met at a bar'),
    (r"(.*)don'?t even know who you are(.*)", r'say we up in your house, sayin I am up in your car'),
    (r'(.*)L\.?A\.?(.*)', r"and I am out at Jermaine's"),
    (r'(.*)up in the a?A?(.*)', r"you're so,so lame"),
    (r'(.*)mentions your name(.*)', r"it must be the something not for class, it must be the E"),
    (r"(.*)poppin'?(.*)", r"heard you get poppin"),
    (r'(.*)o+hh+(.*)', r'oh woah oh ohhh'),
    (r'(.*)why you so obsessed with me(.*)', r'Boy, I wanna know, know, lying that you are into me'), #not the line but not diffrent from line 2. 
    (r'(.*)everybody knows(.*)', r"It is clear that you are upset with me "),
    (r'(.*)found(.*)', r"a girl that you couldn't impress"), 
    (r'(.*)[Ll]ast man(.*)', r"still couldn't get this"),
    (r'(.*)delusional(.*)', r'boy you are losing your mind'),
    (r'(.*)confusing(.*)', r'Why you wastin your time'),
    (r'(.*)fired(.*)', r'See right through you like you are bathing in windex'),
    (r'(.*)you on your job(.*)', r'This line hurts too much (in a job I dislike right now) so I am skipping it ha!'),
    (r'(.*)feed you(.*)', r"Grasping for air, I 'm ventilation"),
    (r'(.*)breath(.*)', r"Telling the world how you miss me"),
    (r'(.*)tripping(.*)', r"You a mom and pop, I am a corporation"),
    (r'(.*)press(.*)', r" you are a conversation"),
]


# Define a function that takes a user input and returns a response
def eliza_chat(user_input):
    # Iterate over the substitution rules
    for pattern, response in substitution_rules:
        # If the pattern matches the user input, return the response
        if re.match(pattern, user_input):
            return re.sub(pattern, response, user_input, flags = re.IGNORECASE)
    return "Ain't the lyrics (but I'm sorry if they are)"

if __name__ == '__main__':
    
    print("Press bye, QUIT, Q, or q to exit")
    print("Hello, I am Mariah Carey. How can I help you today?")
    
    while True:
        # Get user input
        user_input = input("YOU: ") 
        # Exit the loop if the user types 'bye' or 'quit'
        if user_input == 'QUIT' or user_input == 'Q' or user_input == 'q' or user_input == 'bye':
            print("Goodbye! Take care.")
            break
        # Print the response
        print("MC:", eliza_chat(user_input))