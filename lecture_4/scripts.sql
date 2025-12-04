-- Create the 'students' table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_year INTEGER
);

-- Create the 'grades' table
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER REFERENCES students(id) NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER CHECK(grade > 0 AND grade < 100)
);

-- Insert data into the 'students' table
INSERT INTO students (full_name, birth_year) VALUES
    ("Alice Johnson", 2005),
    ("Brian Smith", 2004),
    ("Carla Reyes", 2006),
    ("Daniel Kim", 2005),
    ("Eva Thompson", 2003),
    ("Felix Nguyen", 2007),
    ("Grace Patel", 2005),
    ("Henry Lopez", 2004),
    ("Isabella Martinez", 2006);

INSERT INTO grades (student_id, subject, grade) VALUES
    (1, "Math", 88),
    (1, "English", 92),
    (1, "Science", 85),
    (2, "Math", 75),
    (2, "History", 83),
    (2, "English", 79),
    (3, "Science", 95),
    (3, "Math", 91),
    (3, "Art", 89),
    (4, "Math", 84),
    (4, "Science", 88),
    (4, "Physical Education", 93),
    (5, "English", 90),
    (5, "History", 85),
    (5, "Math", 88),
    (6, "Science", 72),
    (6, "Math", 78),
    (6, "English", 81),
    (7, "Art", 94),
    (7, "Science", 87),
    (7, "Math", 90),
    (8, "History", 77),
    (8, "Math", 83),
    (8, "Science", 80),
    (9, "English", 96),
    (9, "Math", 89),
    (9, "Art", 92);

 -- Рекомендация: Добавить индекс на столбец student_id в таблице grades
 CREATE INDEX grades_student_id_index ON grades(student_id);

-- 4.3 Find all grades for a specific student (Alice Johnson)
SELECT 'Alice Johnson' AS name, grade
FROM grades
WHERE student_id = (
    SELECT id FROM students
    WHERE full_name = 'Alice Johnson'
    );

-- 4.4 Calculate the average grade per student
SELECT full_name, round(avg(grade), 1) AS avg
FROM grades
JOIN students ON students.id = grades.student_id
GROUP BY student_id;

-- 4.5 List all students born after 2004
SELECT full_name, birth_year
FROM students
WHERE birth_year > 2004;

-- 4.6 Create a query that list all subjects and their average grades
SELECT subject, round(avg(grade), 1) AS avg
FROM grades
GROUP BY subject;

-- 4.7 Find the top 3 students with the highest average grades
SELECT full_name, round(avg(grade), 1) AS avg
FROM grades
JOIN students ON students.id = grades.student_id
GROUP BY student_id
ORDER BY avg DESC
LIMIT 3;

-- 4.8 Show all students who have scored below 80 in any subject
SELECT DISTINCT s.full_name
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade < 80;