'''Lecture 3. The Student Grade Analyzer.
A single program that manages and annalyzes student grades.
'''

def get_user_choice() -> int:
    '''Display menu and get validated user choice (1-5).
    '''

    print('\n--- Student Grade Analyzer ---')
    print('1. Add a new student')
    print('2. Add grades for a student')
    print('3. Generate a full report')
    print('4. Find the top student')
    print('5. Exit program')
    while True:
        try:
            n = int(input('Enter your choice: '))
            if 0 < n < 6:
                return n
            print('Invalid input. Please enter a number from 1 to 5.')
            continue
        except ValueError:
            print('Invalid input. Please enter a number.')
        except KeyboardInterrupt:
            print('Invalid combination. Ctrl + C.')
        except EOFError:
            print('Invalid combination. Ctrl + Z.')

def get_name(message: str) -> str | None:
    '''Get and validate name
    Return name or 'exit'.
    '''
    while True:
        try:
            name = input(message).strip().title()
            if name.lower()=='exit':
                return None
            if sum(1 for ch in name if ch.isalpha()) < 2:
                print('There are too few letters for a name.')
                name = ''
            if name.isalpha():
                return name
            # We check the name for extra characters.
            for symb in name:
                if not symb.isalpha() and not symb in (' ', '-'):
                    print(f'The name must not contain this character: {symb}')
                    print('Enter name or \'Exit\' to exit.')
                    name = ''
                    break
            # We clean from unnecessary ' ' and '-'.
            p = 0
            while p <= len(name)-2 and name:
                if name[0] in (' ', '-'):
                    name = name[1:]
                    continue
                if name[len(name)-1] in (' ', '-'):
                    name = name[:len(name)-1]
                    continue
                if name[p] in (' ', '-') and name[p+1] in (' ', '-'):
                    name = name[:p] + name[p+1:]
                else:
                    p += 1
            if name:
                return name
        except KeyboardInterrupt:
            print('Invalid combination. Ctrl + C.')
        except EOFError:
            print('Invalid combination. Ctrl + Z.')

def add_student(students_list: list) -> None:
    '''Add a new student if they don't already exist.
    Modifies the list.
    '''
    name = get_name('Enter name: ')
    for item in students_list:
        if item['name'] == name:
            print('This student already exists.')
            return None
    students_list.append({'name':name, 'grades':[]})
    return None

def add_grades(students_list: list) -> None:
    '''Add grades for an existing student.'''
    name = get_name('Enter student name: ')
    for item in students_list:
        if item['name'] == name:
            while True:
                n = input('Enter a grade (or \'done\' to finish): ')
                if n.lower() == 'done':
                    return None
                try:
                    n = int(n)
                    if 0 <= n <= 100:
                        item['grades'].append(n)
                    else:
                        print('Invalid input. Please enter a number from 0 to 100.')
                except ValueError:
                    print('Invalid input. Please enter an integer number.')
    print('The student is not found.')
    return None

def generate_report(students_list: list):
    '''Generate a sorted report with averages, min/max, and overall stats.'''
    print('--- Student Report ---')
    min_avg = float('inf')
    max_avg = float('-inf')
    sum_avg = 0
    count = 0
    for item in students_list:
        name = item['name']
        try:
            avg = round(sum(item['grades']) / len(item['grades']), 2)
            print(f'{name}\'s average grade is {avg}.')
            count += 1
            sum_avg += avg
            max_avg = max(avg, max_avg)
            min_avg = min(avg, min_avg)
        except ZeroDivisionError:
            print(f'{name}\'s average grade is N/A.')
    print('--------------------------')
    if count:
        print(f'Max Average: {max_avg:.2f}')
        print(f'Min Average: {min_avg:.2f}')
        print(f'Overall Average: {(sum_avg / count):.2f}')
    elif not students_list:
        print('There are no students.')
    else:
        print('There are no grades.')

def top_student(students_list: list) -> None:
    '''Find and display the student with the highest average grade.'''
    if not students_list:
        print('There is no student added.')
        return

    students_graded = [stud for stud in students if stud["grades"]]
    if not students_graded:
        print('There is no grades added.')
        return

    best_stud = max(students_graded, key=lambda stud: sum(stud["grades"]) / len(stud["grades"]))
    stud_avg = round(sum(best_stud["grades"]) / len(best_stud["grades"]), 2)
    print(f'The student with highest average is {best_stud["name"]} with a grade of {stud_avg}.')


students = []
while True:
    CHOISE = get_user_choice()
    if CHOISE == 1:
        add_student(students)
    elif CHOISE == 2:
        add_grades(students)
    elif CHOISE == 3:
        generate_report(students)
    elif CHOISE == 4:
        top_student(students)
    else:
        print('Exiting program.')
        break
