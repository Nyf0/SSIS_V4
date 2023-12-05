USE SSISV3;

CREATE TABLE colleges (
    code varchar(99) NOT NULL,
	name varchar(99) NOT NULL,
    PRIMARY KEY  (code)
);

CREATE TABLE courses (
	code varchar(99) NOT NULL,
	name varchar(99) NOT NULL,
    college varchar(99) NOT NULL,
    PRIMARY KEY (code),
    FOREIGN KEY (college) REFERENCES colleges(code) ON UPDATE CASCADE ON DELETE CASCADE
);

create table students (
	student_id VARCHAR(9) PRIMARY KEY,
    pic varchar(255) NOT NULL,
    fname varchar(99) NOT NULL,
    lname varchar(99) NOT NULL,
    course varchar(99) NOT NULL,
    gender varchar(99) NOT NULL,
    level int NOT NULL,
    FOREIGN KEY (course) REFERENCES courses(code) ON UPDATE CASCADE ON DELETE CASCADE
);

DELIMITER //
CREATE TRIGGER before_student_insert
BEFORE INSERT ON students
FOR EACH ROW
BEGIN
    DECLARE current_year INT;
    DECLARE next_student_id INT;

    SET current_year = YEAR(NOW());

    SELECT IFNULL(MAX(CONVERT(SUBSTRING(student_id, 6), SIGNED)), 0) + 1 INTO next_student_id
    FROM students
    WHERE SUBSTRING(student_id, 1, 4) = current_year;

    SET NEW.student_id = CONCAT(current_year, '-', LPAD(next_student_id, 4, '0'));
END;
//
DELIMITER ;

