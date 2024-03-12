from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_2_nestorbird'
}

# Function to retrieve question text
def get_question_text(question_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT QuestionText FROM Questions WHERE QuestionID=%s", (question_id,))
    question_text = cursor.fetchone()[0]
    conn.close()
    return question_text

# Function to retrieve answers for a given question
def get_answers(question_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT AnswerID, AnswerText FROM Answers WHERE QuestionID=%s", (question_id,))
    answers = cursor.fetchall()
    conn.close()
    return answers

# Function to get the next question ID
def get_next_question_id(answer_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT NextQuestionID FROM Answers WHERE AnswerID=%s", (answer_id,))
    next_question_id = cursor.fetchone()[0]
    conn.close()
    return next_question_id

@app.route('/')
def index():
    return render_template('index.html', question_id=1, question_text=get_question_text(1), answers=get_answers(1))

@app.route('/answer', methods=['POST'])
def answer():
    answer_id = request.form['answer']
    next_question_id = get_next_question_id(answer_id)
    if next_question_id:
        return redirect(url_for('question', question_id=next_question_id))
    else:
        return render_template('result.html')

@app.route('/question/<int:question_id>')
def question(question_id):
    question_text = get_question_text(question_id)
    if not question_text:
        return render_template('result.html')
    answers = get_answers(question_id)
    return render_template('question.html', question_id=question_id, question_text=question_text, answers=answers)

if __name__ == '__main__':
    app.run(debug=True)
