name = input('What is your name? ')
print(f"Type of name variable is: {type(name)}. It should be <class 'str'>")

age = int(input('What is your age? '))
print(f"Type of age variable is: {type(age)}. It should be <class 'int'>")

height = float(input('What is your height in meters? '))
print(f"Type of height variable is: {type(height)}. It should be <class 'float'>")

loyalty = input('Are you part of our loyalty program? ').lower() == 'yes'
print(f"Type of loyalty variable is: {type(loyalty)}. It should be <class 'bool'>")