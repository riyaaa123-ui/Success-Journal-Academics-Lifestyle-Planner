from flask import Flask, render_template, request, redirect,jsonify
from datetime import datetime, timedelta
import mysql.connector
from db_connection import get_db_connection
import google.generativeai as ai
from db_connection import get_db_connection  # Your existing database connection logic

# Initialize the Flask app
app = Flask(__name__)

# Configure the API key for Google Generative AI
API_KEY = 'AIzaSyCaXlaXnIXZPOwSIbi6d7dWneZDF4-CvGo'  # Replace with your actual API key
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-1.5-flash-latest")
chat = model.start_chat()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Academic Section

# Assignment Tracker
@app.route('/academic/assignments', methods=['GET', 'POST'])
def assignment_tracker():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM assignments")
    assignments = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('academic.html', assignments=assignments)

@app.route('/academic/add_assignment', methods=['GET', 'POST'])
def add_assignment():
    if request.method == 'POST':
        print("Adding new assignment")  # Add this line to check
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO assignments (title, description, due_date) VALUES (%s, %s, %s)",
                       (title, description, due_date))
        db.commit()
        cursor.close()
        db.close()
        return redirect('/academic/assignments')
    return render_template('add_assignment.html')

@app.route('/academic/edit_assignment/<int:id>', methods=['GET', 'POST'])
def edit_assignment(id):
    db = get_db_connection()
    cursor = db.cursor()

    if request.method == 'POST':
        # Get the updated data from the form
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        
        # Execute the update query
        cursor.execute("""
            UPDATE assignments 
            SET title = %s, description = %s, due_date = %s 
            WHERE id = %s
        """, (title, description, due_date, id))
        db.commit()

        cursor.close()
        db.close()
        return redirect('/academic/assignments')  # Redirect to the assignments page

    # If GET request, fetch the current assignment data to prefill the form
    cursor.execute("SELECT * FROM assignments WHERE id = %s", (id,))
    assignment = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template('edit_assignment.html', assignment=assignment)

@app.route('/academic/delete_assignment/<int:id>', methods=['GET'])
def delete_assignment(id):
    db = get_db_connection()
    cursor = db.cursor()

    # Execute the delete query
    cursor.execute("DELETE FROM assignments WHERE id = %s", (id,))
    db.commit()

    cursor.close()
    db.close()
    
    return redirect('/academic/assignments')  # Redirect back to the assignments page



# Notes
@app.route('/academic/notes')
def notes():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
        notes = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('notes.html', notes=notes)
    except Exception as e:
        print(f"Error fetching notes: {e}")
        return "An error occurred while fetching notes.", 500

# Add Note
@app.route('/academic/notes/add', methods=['GET'])
def show_add_note_form():
    return render_template('add_note.html')

@app.route('/academic/notes/add', methods=['POST'])
def add_note():
    # Get the form data
    title = request.form.get('title')
    content = request.form.get('content')

    # Check for empty values
    if not title or not content:
        return "Error: Title and content cannot be empty."

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
        db.commit()
        cursor.close()
        db.close()

        return redirect('/academic/notes')
    except Exception as e:
        print(f"Error occurred while adding the note: {e}")
        return "Error occurred while adding the note."


# Edit Note
@app.route('/academic/notes/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            return "Title and Content are required!", 400

        try:
            cursor.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s",
                           (title, content, note_id))
            db.commit()
            cursor.close()
            db.close()
            return redirect('/academic/notes')
        except Exception as e:
            print(f"Error updating note: {e}")
            return "An error occurred while updating the note.", 500

    cursor.execute("SELECT * FROM notes WHERE id = %s", (note_id,))
    note = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('edit_note.html', note=note)

# Delete Note
@app.route('/academic/notes/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        db.commit()
        cursor.close()
        db.close()
        return redirect('/academic/notes')
    except Exception as e:
        print(f"Error deleting note: {e}")
        return "An error occurred while deleting the note.", 500
#if main=true

# To-Do List
@app.route('/academic/daily_todo', methods=['GET', 'POST'])
def daily_todo():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM daily_todo")
    todos = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('daily_todo_list.html', todos=todos)

@app.route('/academic/add_todo', methods=['POST'])
def add_todo():
    task = request.form['task']
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO daily_todo (task) VALUES (%s)", (task,))
    db.commit()
    cursor.close()
    db.close()
    return redirect('/academic/daily_todo')
@app.route('/academic/delete_todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM daily_todo WHERE id = %s", (todo_id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect('/academic/daily_todo')


# Weekly Planner


# Weekly Planner (View All and Add Tasks)
@app.route('/academic/weekly_planner', methods=['GET', 'POST'])
def weekly_planner():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Get the current date and the start of the current week
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())  # Get Monday of the current week
    days_of_week = [start_of_week + timedelta(days=i) for i in range(7)]  # Generate the full week

    # Fetch tasks for each day of the week
    cursor.execute("SELECT * FROM weekly_planner WHERE date IN (%s, %s, %s, %s, %s, %s, %s)",
                   (days_of_week[0], days_of_week[1], days_of_week[2], days_of_week[3],
                    days_of_week[4], days_of_week[5], days_of_week[6]))
    tasks = cursor.fetchall()
    
    cursor.close()
    db.close()

    # If the form is submitted, add a task
    if request.method == 'POST':
        task = request.form['task']
        task_date = request.form['date']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO weekly_planner (date, task) VALUES (%s, %s)", (task_date, task))
        db.commit()
        cursor.close()
        db.close()

        return redirect('/academic/weekly_planner')

    return render_template('weekly_planner.html', days_of_week=days_of_week, tasks=tasks)
from datetime import datetime, timedelta

@app.route('/academic/show_calendar', methods=['GET'])
def show_calendar():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Fetch all tasks
    cursor.execute("SELECT * FROM weekly_planner ORDER BY date ASC")
    tasks = cursor.fetchall()
    cursor.close()
    db.close()

    # Group tasks by date
    tasks_by_date = {}
    for task in tasks:
        task_date = task['date'].strftime('%Y-%m-%d')
        if task_date not in tasks_by_date:
            tasks_by_date[task_date] = []
        tasks_by_date[task_date].append(task['task'])

    # Get the current month and year
    today = datetime.today()
    first_day_of_month = datetime(today.year, today.month, 1)
    first_weekday = first_day_of_month.weekday()  # Monday is 0

    # Build calendar structure
    calendar_data = []
    current_date = first_day_of_month - timedelta(days=first_weekday)

    for _ in range(6):  # Up to 6 weeks
        week = []
        for _ in range(7):  # 7 days per week
            if current_date.strftime('%Y-%m-%d') in tasks_by_date:
                week.append({
                    'date': current_date.day,
                    'tasks': tasks_by_date[current_date.strftime('%Y-%m-%d')]
                })
            else:
                week.append({'date': current_date.day if current_date.month == today.month else None, 'tasks': []})
            current_date += timedelta(days=1)
        calendar_data.append(week)

    return render_template('show_calendar.html', calendar_data=calendar_data)


# Lifestyle Section
# Sleep Tracker


@app.route('/apiapcheck/')
def apiapcheck():
    return render_template('apiindex.html')  # The chatbot page

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form.get('message', '')  # Get the user message
    if not user_message:
        return jsonify({'response': 'No message provided!'})

    if user_message.lower() == 'bye':
        return jsonify({'response': 'Goodbye! Have a nice day!!'})

    try:
        response = chat.send_message(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f"Error generating response: {str(e)}"})

@app.route('/lifestyle/sleep_tracker', methods=['GET', 'POST'])
def sleep_tracker():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sleep_tracker")
    sleep_data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('lifestyle.html', sleep_data=sleep_data)


@app.route('/lifestyle/add_sleep', methods=['GET', 'POST'])
def add_sleep():
    if request.method == 'POST':
        # Get data from the form
        date = request.form['date']
        sleep_hours = request.form['sleep_hours']
        sleep_quality = request.form['sleep_quality']

        # Insert new record into the database
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO sleep_tracker (date, sleep_hours, sleep_quality) VALUES (%s, %s, %s)",
            (date, sleep_hours, sleep_quality)
        )
        db.commit()
        cursor.close()
        db.close()
        
        return redirect('/lifestyle/sleep_tracker')

    return render_template('add_sleep.html')

@app.route('/lifestyle/edit_sleep/<int:id>', methods=['GET', 'POST'])
def edit_sleep(id):
    db = get_db_connection()  # Connect to the database
    cursor = db.cursor(dictionary=True)

    try:
        # Handle POST request: update the record in the database
        if request.method == 'POST':
            date = request.form['date']
            sleep_hours = request.form['sleep_hours']
            sleep_quality = request.form['sleep_quality']

            # Update the record in the database
            cursor.execute("""
                UPDATE sleep_tracker
                SET date = %s, sleep_hours = %s, sleep_quality = %s
                WHERE id = %s
            """, (date, sleep_hours, sleep_quality, id))
            db.commit()

            cursor.close()
            db.close()

            return redirect('/lifestyle/sleep_tracker')

        # Handle GET request: fetch the current record for pre-filling the form
        cursor.execute("SELECT * FROM sleep_tracker WHERE id = %s", (id,))
        sleep = cursor.fetchone()

        if not sleep:
            return "Error: Sleep record not found.", 404

        cursor.close()
        db.close()
        return render_template('edit_sleep.html', sleep=sleep)

    except Exception as e:
        print(f"Error editing sleep record: {e}")
        cursor.close()
        db.close()
        return "An error occurred while editing the sleep record.", 500

@app.route('/lifestyle/delete_sleep/<int:id>', methods=['POST'])
def delete_sleep(id):
    try:
        db = get_db_connection()  # Connect to the database
        cursor = db.cursor()

        # Delete the record from the sleep_tracker table
        cursor.execute("DELETE FROM sleep_tracker WHERE id = %s", (id,))
        db.commit()

        cursor.close()
        db.close()

        return redirect('/lifestyle/sleep_tracker')  # Redirect to the sleep tracker page
    except Exception as e:
        print(f"Error deleting sleep record: {e}")
        return "An error occurred while deleting the sleep record.", 500





# Route to display water intake tracker


@app.route('/lifestyle/water_tracker', methods=['GET', 'POST'])
def water_tracker():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM water_tracker ORDER BY date DESC")
    water_data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('water_tracker.html', water_data=water_data)
# add water
@app.route('/lifestyle/add_water', methods=['GET', 'POST'])
def add_water():
    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO water_tracker (date, amount) VALUES (%s, %s)", (date, amount))
        db.commit()
        cursor.close()
        db.close()

        return redirect('/lifestyle/water_tracker')
    
    return render_template('add_water.html')

#edit water
@app.route('/lifestyle/edit_water/<int:id>', methods=['GET', 'POST'])
def edit_water(id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']

        try:
            cursor.execute(
                "UPDATE water_tracker SET date = %s, amount = %s WHERE id = %s",
                (date, amount, id)
            )
            db.commit()
            cursor.close()
            db.close()
            return redirect('/lifestyle/water_tracker')
        except Exception as e:
            print(f"Error updating water intake: {e}")
            return "An error occurred while updating the water intake.", 500

    cursor.execute("SELECT * FROM water_tracker WHERE id = %s", (id,))
    water_entry = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('edit_water.html', water_entry=water_entry)

#delete water
@app.route('/lifestyle/delete_water/<int:id>', methods=['GET', 'POST'])
def delete_water(id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        try:
            cursor.execute("DELETE FROM water_tracker WHERE id = %s", (id,))
            db.commit()
            cursor.close()
            db.close()
            return redirect('/lifestyle/water_tracker')
        except Exception as e:
            print(f"Error deleting water intake record: {e}")
            return "An error occurred while deleting the record.", 500

    cursor.execute("SELECT * FROM water_tracker WHERE id = %s", (id,))
    water_record = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('delete_water.html', water_record=water_record)


# Exercise Tracker
# Exercise Tracker (View All)
@app.route('/lifestyle/exercise_tracker', methods=['GET'])
def exercise_tracker():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM exercise_tracker ORDER BY date DESC")
    exercises = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('exercise_tracker.html', exercises=exercises)

# Add Exercise (Form and Processing)
'''@app.route('/lifestyle/add_workout', methods=['GET', 'POST'])
def add_workout():
    if request.method == 'POST':
        date = request.form['date']
        workout = request.form['workout']
        duration = request.form['duration']
        notes = request.form['notes']

        # Input validation
        if not date or not workout or not duration:
            return "Error: Date, workout, and duration are required fields.", 400

        db = get_db_connection()
        cursor = db.cursor()

        try:
            # Insert the new exercise record
            cursor.execute("""
                INSERT INTO exercise_tracker (date, workout, duration, notes)
                VALUES (%s, %s, %s, %s)
            """, (date, workout, duration, notes))
            db.commit()
            return redirect('/lifestyle/exercise_tracker')

        except Exception as e:
            print(f"Error adding exercise: {e}")
            return "An error occurred while adding the exercise record.", 500

        finally:
            cursor.close()
            db.close()'''
@app.route('/lifestyle/add_workout', methods=['GET', 'POST'])
def add_workout():
    if request.method == 'POST':
        # Fetch form data
        date = request.form.get('date')
        workout = request.form.get('workout')
        duration = request.form.get('duration')
        notes = request.form.get('notes')

        # Ensure all required fields are present
        if not date or not workout or not duration:
            return "Error: All fields are required.", 400

        try:
            # Connect to the database
            db = get_db_connection()
            cursor = db.cursor()

            # Insert data into the database
            cursor.execute("""
                INSERT INTO exercise_tracker (date, workout, duration, notes)
                VALUES (%s, %s, %s, %s)
            """, (date, workout, duration, notes))
            db.commit()

        except Exception as e:
            print(f"Error: {e}")
            return f"An error occurred: {e}", 500

        finally:
            cursor.close()
            db.close()

        # Redirect to the exercise tracker page after adding the workout
        return redirect('/lifestyle/exercise_tracker')

    # If GET method, render the 'add_workout.html' template
    return render_template('add_workout.html')


# Edit Exercise
@app.route('/lifestyle/edit_workout/<int:exercise_id>', methods=['GET', 'POST'])
def edit_workout(exercise_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        if request.method == 'POST':
            date = request.form.get('date')
            workout = request.form.get('workout')
            duration = request.form.get('duration')
            notes = request.form.get('notes')

            # Log the form data to ensure it's being sent
            print(f"Form data: date={date}, workout={workout}, duration={duration}, notes={notes}")

            # Input validation
            if not date or not workout or not duration:
                return "Error: All fields are required.", 400

            cursor.execute("""
                UPDATE exercise_tracker
                SET date = %s, workout = %s, duration = %s, notes = %s
                WHERE id = %s
            """, (date, workout, duration, notes, exercise_id))
            db.commit()
            return redirect('/lifestyle/exercise_tracker')

        # Fetch the existing record for editing
        cursor.execute("SELECT * FROM exercise_tracker WHERE id = %s", (exercise_id,))
        exercise = cursor.fetchone()
        if not exercise:
            return "Error: Exercise record not found.", 404

        return render_template('edit_workout.html', exercise=exercise)

    except Exception as e:
        print(f"Error while editing exercise record: {e}")
        return f"An error occurred while editing the exercise record: {e}", 500

    finally:
        cursor.close()
        db.close()


# Delete Exercise
@app.route('/lifestyle/delete_exercise/<int:exercise_id>', methods=['GET', 'POST'])
def delete_exercise(exercise_id):
    print(f"Accessing delete route for exercise_id: {exercise_id}")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Try fetching the record to confirm it exists
    try:
        cursor.execute("SELECT * FROM exercise_tracker WHERE id = %s", (exercise_id,))
        exercise_record = cursor.fetchone()
        print(f"Fetched record: {exercise_record}")

        if not exercise_record:
            print("Record not found in the database.")
            return "Error: Exercise record not found.", 404

        if request.method == 'POST':
            cursor.execute("DELETE FROM exercise_tracker WHERE id = %s", (exercise_id,))
            db.commit()
            print("Record deleted successfully.")
            return redirect('/lifestyle/exercise_tracker')

        return render_template('delete_exercise.html', exercise_record=exercise_record)
    
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {e}", 500

    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.run(debug=True)


