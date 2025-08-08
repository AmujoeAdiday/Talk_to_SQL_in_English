import mysql.connector
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MySQL
try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.getenv('MYSQL_PASSWORD'),
        database='saas_analytics'
    )
    print("✅ MySQL connected")
except Exception as e:
    print(f"❌ MySQL connection error: {e}")
    db = None

# Initialize OpenAI client
try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    print("✅ OpenAI client initialized")
except Exception as e:
    print(f"❌ OpenAI client initialization error: {e}")
    client = None

# Database schema for better SQL generation
database_schema = """
Tables and their columns:
- users: id (INT), name (VARCHAR), email (VARCHAR), company (VARCHAR), signup_date (DATE), plan_type (ENUM: 'free','basic','pro','enterprise'), monthly_revenue (DECIMAL), last_login (TIMESTAMP), is_active (BOOLEAN), country (VARCHAR), created_at (TIMESTAMP)
- support_tickets: id (INT), user_id (INT), subject (VARCHAR), status (ENUM: 'open','in_progress','resolved','closed'), priority (ENUM: 'low','medium','high','urgent'), created_at (TIMESTAMP), resolved_at (TIMESTAMP), category (VARCHAR)
- feature_usage: id (INT), user_id (INT), feature_name (VARCHAR), usage_count (INT), usage_date (DATE), session_duration_minutes (INT)
- monthly_metrics: id (INT), user_id (INT), month_year (VARCHAR format 'YYYY-MM'), api_calls (INT), storage_used_gb (DECIMAL), bandwidth_used_gb (DECIMAL), active_days (INT)

Key relationships:
- support_tickets.user_id → users.id
- feature_usage.user_id → users.id
- monthly_metrics.user_id → users.id

Notes:
- month_year in monthly_metrics is stored as 'YYYY-MM' format (e.g., '2025-01', '2025-02')
- last_login is a TIMESTAMP column in the users table
- Users can have multiple monthly_metrics records (one per month)
"""

# List of questions to ask
questions = [
    "How many enterprise customers do we have?",
    "Which customers haven't logged in for more than a week?",
    "What's our total monthly recurring revenue?",
    "Show me all open support tickets with high priority",
    "Which features are used most by pro plan customers?",
    "What's the average API usage for enterprise customers in the most recent month?",
    "How many users signed up this month?",
    "What's the average monthly revenue per customer by plan type?",
    "Show me the top 5 customers with the highest storage usage",
    "Which countries have the most enterprise customers?",
    "Show me the most recent login times for enterprise customers who haven't logged in recently",
    "What's the total storage used by all customers this month?"
]

def process_question(question):
    """Process a single question and return results"""
    print(f"\n🤔 Question: {question}")
    print("-" * 50)
    
    if not client or not db:
        print("❌ Required connections not available")
        return
    
    # Create prompt for OpenAI
    prompt = f"""
Convert this question to SQL for a SaaS analytics database:

{database_schema}

Question: {question}

Important guidelines:
- Return ONLY the SQL query, no explanations
- last_login is a column in the users table, not a separate table
- For "most" or "highest" questions, use ORDER BY DESC and LIMIT 1 to show top results
- For date comparisons with "last week/month", use DATE_SUB(NOW(), INTERVAL X DAY/MONTH)
- When joining monthly_metrics with users and there are multiple months per user, consider using MAX() or GROUP BY to avoid duplicates
- For counting, use COUNT(*) or COUNT(column_name)
- For enterprise customers, use plan_type = 'enterprise'
- For revenue calculations, use SUM(monthly_revenue)
- For monthly_metrics date filtering, the month_year format is 'YYYY-MM'
- When checking for NULL results in aggregations, consider that there might be no matching data

SQL Query:"""

    try:
        # Get SQL from OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        sql = response.choices[0].message.content.strip()
        
        # Clean up the SQL (remove markdown formatting if present)
        if sql.startswith("```sql"):
            sql = sql.replace("```sql", "").replace("```", "")
        sql = sql.strip()
        
        print(f"🔍 Generated SQL:")
        print(sql)
        print()

        # Execute SQL query
        cursor = db.cursor()
        cursor.execute(sql)
        
        # Get results
        if sql.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            if results:
                print(f"📊 Results ({len(results)} rows):")
                
                # Check if all results are NULL for aggregation queries
                if len(results) == 1 and len(results[0]) == 1 and results[0][0] is None:
                    print("   No data found for this query (result is NULL)")
                    print("   This might mean no records match the criteria or date range")
                else:
                    # Print column headers
                    print("   " + " | ".join(columns))
                    print("   " + "-" * (len(" | ".join(columns))))
                    
                    # Print results (limit to first 10 rows)
                    for i, row in enumerate(results[:10]):
                        formatted_row = []
                        for value in row:
                            if value is None:
                                formatted_row.append("NULL")
                            else:
                                formatted_row.append(str(value))
                        print(f"   {' | '.join(formatted_row)}")
                    
                    if len(results) > 10:
                        print(f"   ... and {len(results) - 10} more rows")
            else:
                print("📊 No results found")
        else:
            # For non-SELECT queries
            db.commit()
            print(f"📊 Query executed successfully. {cursor.rowcount} rows affected.")
        
        cursor.close()

    except Exception as e:
        print(f"❌ Error: {e}")

# Main execution
if __name__ == "__main__":
    print("🚀 SaaS Analytics Query Tool")
    print("=" * 60)
    
    if client and db:
        successful_queries = 0
        failed_queries = 0
        
        for i, question in enumerate(questions, 1):
            print(f"\n[{i}/{len(questions)}]", end="")
            try:
                process_question(question)
                successful_queries += 1
            except Exception as e:
                print(f"❌ Failed to process question: {e}")
                failed_queries += 1
            
            print("=" * 60)
        
        # Summary
        print(f"\n📋 SUMMARY:")
        print(f"✅ Successful queries: {successful_queries}")
        print(f"❌ Failed queries: {failed_queries}")
        print(f"📊 Total questions processed: {len(questions)}")
        
        # Close database connection
        db.close()
        print("\n🔐 Database connection closed")
    else:
        print("❌ Cannot proceed without database and OpenAI connections")