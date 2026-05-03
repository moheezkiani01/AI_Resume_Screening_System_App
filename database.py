import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='screening_results.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                score REAL,
                skills TEXT,
                classification TEXT,
                recommendation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check if recommendation column exists, if not add it
        cursor.execute("PRAGMA table_info(results)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'recommendation' not in columns:
            cursor.execute('ALTER TABLE results ADD COLUMN recommendation TEXT')
            print("Added recommendation column")
        
        if 'created_at' not in columns:
            cursor.execute('ALTER TABLE results ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            print("Added created_at column")
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    
    def save_result(self, result):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO results (filename, score, skills, classification, recommendation)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            result.get('original_filename', 'unknown'),
            result['score'],
            result['skills_text'],
            result['classification'],
            result['recommendation']
        ))
        
        conn.commit()
        conn.close()
    
    def get_all_results(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, score, skills, classification, recommendation, 
                   strftime('%Y-%m-%d %H:%M', created_at) as date
            FROM results
            ORDER BY created_at DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': r[0],
                'filename': r[1],
                'score': r[2],
                'skills': r[3],
                'classification': r[4],
                'recommendation': r[5] if len(r) > 5 else 'No recommendation',
                'date': r[6] if len(r) > 6 else ''
            }
            for r in results
        ]
    
    def get_result_by_id(self, result_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, score, skills, classification, recommendation, 
                   strftime('%Y-%m-%d %H:%M', created_at) as date
            FROM results
            WHERE id = ?
        ''', (result_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'filename': result[1],
                'score': result[2],
                'skills': result[3],
                'classification': result[4],
                'recommendation': result[5] if len(result) > 5 else 'No recommendation',
                'date': result[6] if len(result) > 6 else ''
            }
        return None