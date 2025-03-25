-- 创建进程表
CREATE TABLE processes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('running', 'paused', 'blocked')),
    priority TEXT NOT NULL CHECK(priority IN ('high', 'medium', 'low')),
    details TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime')) -- 使用 TEXT 存储时间戳
);

-- 创建日志表
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    process_id INTEGER NOT NULL,
    log_entry TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime')), -- 使用 TEXT 存储时间戳
    FOREIGN KEY (process_id) REFERENCES processes(id)
);

-- 插入测试数据
INSERT INTO processes (name, status, priority, details) VALUES
('Process 1', 'running', 'high', 'Initial process details'),
('Process 2', 'paused', 'medium', 'Details for process 2');

INSERT INTO logs (process_id, log_entry) VALUES
(1, 'Log entry for Process 1'),
(2, 'Log entry for Process 2');