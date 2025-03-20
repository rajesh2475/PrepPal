CREATE TABLE job_openings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    position VARCHAR(255) NOT NULL,
    experience VARCHAR(50),
    vacancies INT,
    location VARCHAR(255),
    must_have TEXT, -- Store as a comma-separated string
    good_to_have TEXT, -- Store as a comma-separated string
    description TEXT,
    role VARCHAR(255),
    education VARCHAR(255),
    employment_type VARCHAR(50)
);

CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    resume VARCHAR(255),
    score FLOAT,
    job_id INT,
    FOREIGN KEY (job_id) REFERENCES job_openings(id) ON DELETE CASCADE
);