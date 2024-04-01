USE `nasa_judge`;

-- user Table
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    role VARCHAR(255)
);

-- problem Table
CREATE TABLE problem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    problem_name VARCHAR(255),
    created_time DATETIME,
    deadline DATETIME
);

-- submission Table
CREATE TABLE submission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    problem_id INT,
    submission_score INT,
    timestamp DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (problem_id) REFERENCES problem(id)
);

-- tasks Table
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(255),
    points_credit INT,
    user_id INT,
    problem_id INT,
    is_passed BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (problem_id) REFERENCES problem(id)
);

-- wireguard_profile Table
CREATE TABLE wireguard_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    is_valid BOOLEAN,
    creation_date_time DATETIME,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

