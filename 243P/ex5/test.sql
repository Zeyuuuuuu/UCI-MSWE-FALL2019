use sm;

SELECT *
FROM STUDENTS;

SELECT *
FROM COURSES;

SELECT *
FROM students_courses;


SELECT c.course_name, s.student_name
FROM courses c
  JOIN students_courses sc
    ON c.course_id = sc.course_id
  JOIN students s
    ON sc.student_id = s.student_id
WHERE c.course_id = '1'
ORDER BY s.student_name;

SELECT s.student_name,c.course_name 
FROM courses c JOIN students_courses sc 
ON c.course_id = sc.course_id 
JOIN students s ON sc.student_id = s.student_id 
WHERE s.student_id = 1 and c.course_schedule LIKE '%Mon%' ORDER BY c.course_name
