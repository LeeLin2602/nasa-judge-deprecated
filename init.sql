USE `nasa_judge`;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    role VARCHAR(255)
);

CREATE TABLE problems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    is_valid BOOLEAN DEFAULT TRUE,
    problem_name VARCHAR(255),
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_time DATETIME,
    deadline DATETIME
);

CREATE TABLE submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    problem_id INT,
    submission_score INT,
    submit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);

CREATE TABLE subtasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    problem_id INT,
    task_name VARCHAR(255),
    points INT,
    is_valid BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);

CREATE TABLE wireguard_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    is_valid BOOLEAN DEFAULT TRUE,
    creation_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE subtaskResult (
    id INT AUTO_INCREMENT PRIMARY KEY,
    submission_id INT,
    task_id INT,
    is_passed BOOLEAN,
    FOREIGN KEY (submission_id) REFERENCES submissions(id),
    FOREIGN KEY (task_id) REFERENCES subtasks(id)
);
