CREATE TABLE mood_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nickname VARCHAR(50) NOT NULL,
    age INT,
    mood_score INT NOT NULL,
    message TEXT,
    entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);