import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# Function to categorize tasks based on keywords
def categorize_task(task):
    if 'work' in task.lower():
        return 'Work'
    elif 'personal' in task.lower():
        return 'Personal'
    else:
        return 'Other'

# Function to create database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

# Function to create tasks table
def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        due_date DATE,
        category TEXT,
        completed BOOLEAN
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Function to insert task into database
def insert_task(conn, task, due_date, category, completed=False):
    sql = """
    INSERT INTO tasks (task, due_date, category, completed)
    VALUES (?, ?, ?, ?)
    """
    cur = conn.cursor()
    cur.execute(sql, (task, due_date, category, completed))
    conn.commit()
    return cur.lastrowid

# Function to retrieve tasks from database
def fetch_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    return rows

# Function to mark task as complete
def complete_task(conn, task_id):
    sql = """
    UPDATE tasks
    SET completed = 1
    WHERE id = ?
    """
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()

# Function to delete task
def delete_task(conn, task_id):
    sql = """
    DELETE FROM tasks
    WHERE id = ?
    """
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()

# Main function to run the app
def main():
    # Database initialization
    conn = create_connection("todo.db")
    if conn is not None:
        create_table(conn)
    else:
        st.error("Error: Unable to create database connection.")

    # Customizing theme
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <style>
        .reportview-container {
            background: linear-gradient(90deg, #74ebd5, #9face6);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🚀 SuperTask - The Ultimate To-Do List App 📝")

    # Sidebar for task entry
    st.sidebar.header("➕ Add New Task")
    task = st.sidebar.text_input("Enter Task", key="task_input")
    due_date = st.sidebar.date_input("Due Date", key="due_date_input")
    add_button = st.sidebar.button("Add Task", key="add_button")

    # Add task to database
    if add_button:
        category = categorize_task(task)
        if conn is not None:
            task_id = insert_task(conn, task, due_date, category)
            st.sidebar.success("Task added successfully! 🎉")
        else:
            st.sidebar.error("Error: Unable to add task. 😞")

    # Display tasks
    st.header("📋 Your Tasks")
    if conn is not None:
        tasks = fetch_tasks(conn)
        if tasks:
            df = pd.DataFrame(tasks, columns=['ID', 'Task', 'Due Date', 'Category', 'Completed'])
            # Add checkbox column for marking tasks as complete
            df['Completed'] = df.apply(lambda row: st.checkbox("", value=row['Completed'], key=row['ID']), axis=1)
            st.dataframe(df)
            for index, row in df.iterrows():
                if row['Completed']:
                    delete_button = st.button(f"Delete Task {row['ID']}")
                    if delete_button:
                        delete_task(conn, row['ID'])
        else:
            st.info("No tasks available. Add some tasks to get started! 🚀")

    # Data visualization - Task Categories
    st.header("📊 Task Categories")
    if conn is not None:
        tasks = fetch_tasks(conn)
        if tasks:
            df = pd.DataFrame(tasks, columns=['ID', 'Task', 'Due Date', 'Category', 'Completed'])
            category_counts = df['Category'].value_counts()
            fig = px.pie(values=category_counts, names=category_counts.index, title='Task Categories')
            fig.update_traces(marker=dict(colors=['#ff9999', '#99ff99', '#9999ff']))
            st.plotly_chart(fig)
        else:
            st.info("No tasks available. Add some tasks to see the categories! 🚀")

    # Footer with social media links
    footer_html = """
    <footer style="text-align:center; margin-top: 50px;">
        <div style="margin-bottom: 20px;">
            <a href="https://www.linkedin.com/in/muhammad-ibrahim-qasmi-9876a1297/" target="_blank" style="margin-right: 20px;">
                <img src="https://img.icons8.com/fluent/48/000000/linkedin.png" alt="LinkedIn" style="width: 30px; height: 30px;"/>
            </a>
            <a href="https://github.com/muhammadibrahim313" target="_blank" style="margin-right: 20px;">
                <img src="https://img.icons8.com/material-outlined/48/000000/github.png" alt="GitHub" style="width: 30px; height: 30px;"/>
            </a>
            <a href="https://www.kaggle.com/muhammadibrahimqasmi" target="_blank">
                <img src="https://img.icons8.com/windows/32/000000/kaggle.png" alt="Kaggle" style="width: 30px; height: 30px;"/>
            </a>
        </div>
        <div>
            <span style="font-size: 15px;">Connect with me on LinkedIn, GitHub, and Kaggle!</span>
        </div>
    </footer>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
