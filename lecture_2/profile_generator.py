def generate_profile(age:int) -> str:
    if 0 <= age <= 12:
        return 'Child'
    elif 13 <= age <= 19:
        return 'Teenager'
    else:
        return 'Adult'



user_name = input('Enter your full name: ')
birth_year_str = input('Enter your birth year: ')
birth_year = int(birth_year_str)
current_age = 2025 - birth_year
life_stage = generate_profile(current_age)



hobbies = []
hobby = input('Enter a favorite hobby or ' \
                        'type \'stop\' to finish: ')
while hobby != 'stop':
    hobbies.append(hobby)
    hobby = input('Enter a favorite hobby or ' \
                        'type \'stop\' to finish: ')



user_profile = {
    'name': user_name,
    'age': current_age,
    'stage': life_stage,
    'hobbies': hobbies
}



print()
print('---')
print('Profile Summary:')
print(f'Name: {user_name}')
print(f'Age: {current_age}')
print(f'Life Stage: {life_stage}')
if hobbies:
    print(f'Favorite Hobbies ({len(hobbies)}):')
    for hobby in hobbies:
        print(f'- {hobby}')
else:
    print('You didn\'t mention any hobbies.')
print('---')