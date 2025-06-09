import sqlite3
import csv
from datetime import datetime

def initialize_database():
    conn = sqlite3.connect('flashcard.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,
            answer TEXT,
            wrong_count INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time DATETIME,
            end_time DATETIME,
            total_questions INTEGER,
            correct_count INTEGER,
            wrong_count INTEGER,
            accuracy REAL
        )
    ''')
    conn.commit()
    return conn

def insert_questions_from_input(conn):
    csv_file_path = input("请输入CSV文件路径: ").strip()
    if not csv_file_path:
        print("文件路径不能为空")
        return
    try:
        insert_questions_from_csv(conn, csv_file_path)
        print("题目已成功导入！")
    except FileNotFoundError:
        print("找不到指定的文件")
    except Exception as e:
        print(f"导入失败: {str(e)}")

    _
def insert_questions_from_csv(conn, csv_file_path):
    cursor = conn.cursor()
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        # 跳过表头
        next(reader)
        for row in reader:
            question = row[0] if len(row) > 0 else ''
            option_a = row[1] if len(row) > 1 else ''
            option_b = row[2] if len(row) > 2 else ''
            option_c = row[3] if len(row) > 3 else ''
            option_d = row[4] if len(row) > 4 else ''
            answer = row[5] if len(row) > 5 else ''
            cursor.execute('''
                INSERT INTO questions (question, option_a, option_b, option_c, option_d, answer)
                VALUES (?,?,?,?,?,?)
            ''', (question, option_a, option_b, option_c, option_d, answer))
    conn.commit()

def get_wrong_stats(conn):
    """获取错题统计信息"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) as wrong_questions_count, 
               SUM(wrong_count) as total_wrong_count
        FROM questions 
        WHERE wrong_count > 0
    ''')
    return cursor.fetchone()
def start_quiz(conn, question_filter='all', limit=None):
    cursor = conn.cursor()
    
    # 根据不同模式选择题目
    if question_filter == 'review':
        cursor.execute('SELECT * FROM questions WHERE wrong_count <= 0 order by wrong_count desc')
    elif question_filter == 'wrong':
        cursor.execute('SELECT * FROM questions WHERE wrong_count > 0 order by wrong_count desc ')
    else:
        cursor.execute('SELECT * FROM questions ORDER BY wrong_count DESC')
    
    questions = cursor.fetchall()
    if not questions:
        print("没有符合条件的题目!")
        return
    
    # 如果设置了数量限制
    if limit and limit < len(questions):
        questions = questions[:limit]
    
    total_questions = len(questions)
    correct_count = 0
    wrong_count = 0
    start_time = datetime.now()

    for i, question in enumerate(questions, 1):
        _, q_text, a, b, c, d, correct_answer, current_wrong_count = question
        print(f"\n[{i}/{total_questions}] 问题: {q_text}")
        print(f"A: {a}")
        print(f"B: {b}")
        print(f"C: {c}")
        print(f"D: {d}")
        print("输入9退出答题")
        
        user_choice = input("请输入你的选择 (1-4 对应 A-D): ").strip()
        
        if user_choice == '9':
            break
            
        choice_mapping = {'1': 'A', '2': 'B', '3': 'C', '4': 'D'}
        if user_choice in choice_mapping and choice_mapping[user_choice] == correct_answer:
            print("✓ 回答正确！")
            correct_count += 1
            if current_wrong_count > 0:
                cursor.execute('UPDATE questions SET wrong_count = wrong_count - 1 WHERE id =?', (question[0],))
        else:
            print(f"✗ 回答错误，正确答案是 {correct_answer}")
            wrong_count += 1
            cursor.execute('UPDATE questions SET wrong_count = wrong_count + 1 WHERE id =?', (question[0],))

        conn.commit()
        accuracy = correct_count / (correct_count + wrong_count) * 100 if (correct_count + wrong_count) > 0 else 0
        print(f"当前正确率: {accuracy:.2f}%")

    # 保存答题记录
    end_time = datetime.now()
    duration = end_time - start_time
    final_accuracy = correct_count / (correct_count + wrong_count) * 100 if (correct_count + wrong_count) > 0 else 0
    
    cursor.execute('''
        INSERT INTO quiz_records 
        (start_time, end_time, total_questions, correct_count, wrong_count, accuracy)
        VALUES (?,?,?,?,?,?)
    ''', (start_time, end_time, total_questions, correct_count, wrong_count, final_accuracy))
    conn.commit()
    
    # 显示答题摘要
    print("\n=== 答题摘要 ===")
    print(f"答题时间: {duration.total_seconds():.0f} 秒")
    print(f"题目数量: {correct_count + wrong_count}")
    print(f"正确数量: {correct_count}")
    print(f"错误数量: {wrong_count}")
    print(f"正确率: {final_accuracy:.2f}%")


def reset_wrong_count(conn):
    cursor = conn.cursor()
    cursor.execute('UPDATE questions SET wrong_count = 0')
    conn.commit()
    print("所有试题的答错计数器已重置为 0")

def get_wrong_stats(conn):
    """获取错题统计信息"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) as wrong_questions_count, 
               SUM(wrong_count) as total_wrong_count
        FROM questions 
        WHERE wrong_count > 0
    ''')
    return cursor.fetchone()

def delete_all_questions(conn):
    """删除所有试题"""
    if input("确定要删除所有试题吗? (y/N): ").lower() != 'y':
        print("已取消删除操作")
        return
        
    cursor = conn.cursor()
    cursor.execute('DELETE FROM questions')
    conn.commit()
    print("所有试题已删除")

if __name__ == "__main__":
    conn = initialize_database()
    #csv_file_path = 'ex.csv'
    #insert_questions_from_csv(conn, csv_file_path)

    while True:
        # 获取错题统计
        wrong_stats = get_wrong_stats(conn)
        wrong_count, total_wrong_times = wrong_stats if wrong_stats else (0, 0)
        
        print("\n=== 主菜单 ===")
        print(f"错题数量: {wrong_count}")
        print(f"答错次数: {total_wrong_times}")
        print("-" * 20)
        print("1. 对题重温")
        print("2. 错题清除")
        print("3. 所有题目")
        print("4. 重置答错计数")
        print("5. 导入试题")
        print("6. 删除所有试题")
        print("7. 退出程序")

        choice = input("输入你的选择: ").strip()
        
        if choice in ['1', '2', '3']:
            try:
                limit = int(input("请输入本次答题数量(直接回车则做所有题): ").strip() or 0)
            except ValueError:
                limit = 0
                
            if choice == '1':
                start_quiz(conn, 'review', limit)
            elif choice == '2':
                start_quiz(conn, 'wrong', limit)
            else:
                start_quiz(conn, 'all', limit)
                
        elif choice == '4':
            reset_wrong_count(conn)
        elif choice == '5':
            insert_questions_from_input(conn)
        elif choice == '6':
            delete_all_questions(conn)
        elif choice == '7':
            conn.close()
            break
        else:
            print("无效的选择，请重试。")