-- 创建数据库
CREATE DATABASE IF NOT EXISTS realtime_voting;
USE realtime_voting;

-- 创建投票问卷表
CREATE TABLE IF NOT EXISTS polls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

-- 创建选项表
CREATE TABLE IF NOT EXISTS options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    poll_id INT NOT NULL,
    text VARCHAR(255) NOT NULL,
    votes INT DEFAULT 0,
    FOREIGN KEY (poll_id) REFERENCES polls(id)
);

-- 预置问卷数据
INSERT INTO polls (title) VALUES ('你最喜欢的编程语言是什么？');

-- 预置选项数据
INSERT INTO options (poll_id, text) VALUES
(1, 'Python'),
(1, 'JavaScript'),
(1, 'Go'),
(1, 'Java'),
(1, 'C++');