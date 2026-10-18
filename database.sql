CREATE DATABASE attendance_system;

USE attendance_system;

CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    mail VARCHAR(100),
    ph_no VARCHAR(20)
);

CREATE TABLE teachers (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    mail VARCHAR(100),
    ph_no VARCHAR(20)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_code VARCHAR(20),
    course_name VARCHAR(100),
    teacher_id INT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

CREATE TABLE classes (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    class_date DATE,
    room_no VARCHAR(20),
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    teacher_id INT,
    class_id INT,
    status VARCHAR(20),
    remarks VARCHAR(200),

    FOREIGN KEY(student_id) REFERENCES students(student_id),
    FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY(class_id) REFERENCES classes(class_id)
);