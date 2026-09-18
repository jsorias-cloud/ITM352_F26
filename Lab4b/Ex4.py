# Parse through the portions of an email address and print out the username and domain name. 
# Name: Jorryn Orias
# Date: September 18, 2026

#Method 1: Using split() method

email_address = input("Enter an email address: ")
parts= email_address.split("@")
username = parts[0]
domain_name = parts[1]

print("Parts of the email address are:", parts)
print("The username is:", username)
print("The domain name is:", domain_name)

# Method 2: Using index and slicing 
at_sign_index = email_address.index("@")
username2 = email_address[:at_sign_index]
domain_name2 = email_address[at_sign_index + 1:]

print("The username using slicing is:", username2)
print("The domain name using slicing is:", domain_name2)
