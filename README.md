# Talk_to_SQL_in_English

Ask your database questions in plain English and get real answers back! This project connects OpenAI's LLM to MySQL, allowing you to query your database using natural language.

## 🚀 What it does

- Ask questions like "How many enterprise customers do we have?"
- LLM automatically generates SQL queries
- Executes queries on your MySQL database
- Returns results in a clean, readable format
- No SQL knowledge required!

## 📋 Prerequisites

- Python 3.7+
- MySQL Server
- OpenAI API key

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/AmuJoeAiday/Talk_to_SQL_in_English.git
cd Talk_to_SQL_in_English
python Talk_to_SQL_in_English.py
```

### 2. Install required packages
```bash
pip install mysql-connector-python openai python-dotenv
```

### 3. Set up MySQL Database

**Start MySQL and create database:**
```sql
CREATE DATABASE saas_analytics;
USE saas_analytics;
```

**Create tables:**
```sql
-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    company VARCHAR(100),
    signup_date DATE NOT NULL,
    plan_type ENUM('free', 'basic', 'pro', 'enterprise') DEFAULT 'free',
    monthly_revenue DECIMAL(8,2) DEFAULT 0,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Support tickets table
CREATE TABLE support_tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    subject VARCHAR(255) NOT NULL,
    status ENUM('open', 'in_progress', 'resolved', 'closed') DEFAULT 'open',
    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    category VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Feature usage table
CREATE TABLE feature_usage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    feature_name VARCHAR(100) NOT NULL,
    usage_count INT DEFAULT 1,
    usage_date DATE NOT NULL,
    session_duration_minutes INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Monthly metrics table
CREATE TABLE monthly_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    month_year VARCHAR(7),
    api_calls INT DEFAULT 0,
    storage_used_gb DECIMAL(8,2) DEFAULT 0,
    bandwidth_used_gb DECIMAL(8,2) DEFAULT 0,
    active_days INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 4. Add Sample Data (Optional)
```sql
-- Insert sample users
INSERT INTO users (name, email, company, signup_date, plan_type, monthly_revenue, country) VALUES
('John Smith', 'john@techcorp.com', 'TechCorp Inc', '2024-01-15', 'enterprise', 299.00, 'USA'),
('Sarah Johnson', 'sarah@startup.io', 'Startup.io', '2024-02-01', 'pro', 99.00, 'Canada'),
('Mike Wilson', 'mike@freelance.com', 'Freelance', '2024-01-20', 'basic', 29.00, 'UK'),
('Anna Davis', 'anna@bigcorp.com', 'BigCorp Ltd', '2024-01-10', 'enterprise', 299.00, 'Australia'),
('Tom Brown', 'tom@agency.com', 'Creative Agency', '2024-02-15', 'pro', 99.00, 'USA');

-- Insert sample monthly metrics
INSERT INTO monthly_metrics (user_id, month_year, api_calls, storage_used_gb, bandwidth_used_gb, active_days) VALUES
(1, '2025-01', 45000, 14.2, 25.5, 28),
(1, '2025-02', 41000, 12.5, 22.1, 25),
(2, '2025-01', 5200, 4.8, 8.2, 22),
(4, '2025-01', 43000, 20.1, 35.2, 30);

-- Insert sample feature usage
INSERT INTO feature_usage (user_id, feature_name, usage_count, usage_date, session_duration_minutes) VALUES
(1, 'Analytics View', 15, '2025-01-15', 45),
(2, 'Report Builder', 30, '2025-01-20', 30),
(4, 'Analytics View', 20, '2025-01-18', 60);
```

### 5. Environment Setup

Create a `.env` file in the project root:
```env
MYSQL_PASSWORD=your_mysql_password
OPENAI_API_KEY=your_openai_api_key
```

**Get your OpenAI API key:**
1. Go to https://platform.openai.com
2. Sign up/login
3. Go to API Keys section
4. Create new secret key
5. Copy and paste into `.env` file

## 🎯 Usage

Run the script:
```bash
python main.py
```

### Example Questions You Can Ask:
- "How many enterprise customers do we have?"
- "What's our total monthly recurring revenue?"
- "Which customers haven't logged in for more than a week?"
- "Show me all open support tickets with high priority"
- "Which features are used most by pro plan customers?"
- "What's the average API usage for enterprise customers?"

## 📁 Project Structure
```
nl-to-sql/
├── main.py              # Main script
├── .env                 # Environment variables (create this)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Requirements.txt
```txt
mysql-connector-python==8.0.33
openai==1.3.0
python-dotenv==1.0.0
```

## 🐛 Troubleshooting

**MySQL Connection Error:**
- Make sure MySQL server is running
- Check your password in `.env` file
- Verify database name is `saas_analytics`

**OpenAI API Error:**
- Verify your API key is correct
- Check you have credits in your OpenAI account
- Make sure API key has proper permissions

**No Results Found:**
- Check if your tables have data
- Try simpler questions first
- Look at the generated SQL to debug

## 🤝 Contributing

Feel free to open issues or submit pull requests! This is a learning project and I'm always open to improvements.

## 📜 License

MIT License - feel free to use this however you want!

## 🙋‍♂️ Questions?

DM me on LinkedIn or open an issue here. Always happy to help fellow developers!

---

*Built with ☕ and curiosity about how enterprise AI features actually work*
