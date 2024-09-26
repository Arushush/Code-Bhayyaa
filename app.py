import streamlit as st
import mysql.connector as nasa
from mysql.connector import Error
import pandas as pd  # Import Pandas for DataFrame support

# Initialize session state for profile visibility and login status
if 'show_profile' not in st.session_state:
    st.session_state['show_profile'] = True
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Function to create a MySQL connection
def create_connection():
    try:
        connection = nasa.connect(
            host='localhost',
            database='streamlit_db',  # Your Database name
            user='root',  # MySQL username
            password='nega'  # MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return None

# Function to authenticate user login
def authenticate(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM login WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return True
    return False

# Function to insert data into 'entries' table
def insert_entry(name, age, medical_condition, medications, allergies, emergency_contact, emergency_contact_phone):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO entries (name, age, medical_condition, medications, allergies, emergency_contact, emergency_contact_phone) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, age, medical_condition, medications, allergies, emergency_contact, emergency_contact_phone))
            connection.commit()
            st.success("Data inserted successfully!")
        except Error as e:
            st.error(f"Error inserting data: {e}")
        finally:
            cursor.close()
            connection.close()

# Function to update data in 'entries' table
def update_entry(entry_id, name, age, medical_condition, medications, allergies, emergency_contact, emergency_contact_phone):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            query = """
                UPDATE entries 
                SET name = %s, age = %s, medical_condition = %s, medications = %s, allergies = %s, emergency_contact = %s, emergency_contact_phone = %s 
                WHERE id = %s
            """
            cursor.execute(query, (name, age, medical_condition, medications, allergies, emergency_contact, emergency_contact_phone, entry_id))
            connection.commit()
            if cursor.rowcount > 0:
                st.success("Entry updated successfully!")
            else:
                st.warning("No entry found with that ID.")
        except Error as e:
            st.error(f"Error updating data: {e}")
        finally:
            cursor.close()
            connection.close()

# Function to display all entries with column names
def display_entries():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM entries"
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            # Fetch column names
            column_names = [i[0] for i in cursor.description]
            st.write("### Displaying All Entries")
            # Use Pandas DataFrame for better display
            df = pd.DataFrame(rows, columns=column_names)
            st.table(df)
        else:
            st.warning("No entries found in the database.")
        cursor.close()
        connection.close()

# Function to display user profile information
def view_profile(username):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT username, facultyid, name, email, Number, designation FROM login WHERE username = %s"
        cursor.execute(query, (username,))
        profile = cursor.fetchone()
        cursor.close()
        connection.close()

        if profile:
            st.write("### Profile Information")
            st.write(f"**Username:** {profile[0]}")
            st.write(f"**Faculty ID:** {profile[1]}")
            st.write(f"**Name:** {profile[2]}")
            st.write(f"**Email:** {profile[3]}")
            st.write(f"**Number:** {profile[4]}")
            st.write(f"**Designation:** {profile[5]}")
        else:
            st.warning("No profile found.")

# Login Page
def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if authenticate(username, password):
            st.success("Login successful!")
            st.session_state['username'] = username  # Store username in session state
            st.session_state['logged_in'] = True  # Set logged in state
        else:
            st.error("Invalid username or password")

# Dashboard after login
def dashboard():
    if 'username' not in st.session_state:
        st.warning("Please log in first.")
        login_page()
        return

    st.title(f"Welcome, {st.session_state['username']}!")

    # Sidebar Profile Management
    if st.sidebar.button("Manage Profile"):
        st.session_state['show_profile'] = True  # Show profile when managing
        view_profile(st.session_state['username'])  # Show profile details

    # Sidebar Database Management
    st.sidebar.header("Manage Database")
    
    if st.sidebar.button("Add Entries"):
        st.session_state['show_profile'] = False  # Hide profile on button click
        st.write("### Add New Entry")
        with st.form("add_form", clear_on_submit=True):
            name = st.text_input("Enter name")
            age = st.number_input("Enter age", min_value=1, max_value=100)
            medical_condition = st.text_input("Medical Condition")
            medications = st.text_input("Medications")
            allergies = st.text_input("Allergies")
            emergency_contact = st.text_input("Emergency Contact Name")
            emergency_contact_phone = st.text_input("Emergency Contact Phone")
            submit = st.form_submit_button("Submit")
            if submit and name and age:
                insert_entry(name, age, medical_condition, medications, allergies, emergency_contact, emergency_contact_phone)

    if st.sidebar.button("Display Entries"):
        st.session_state['show_profile'] = False  # Hide profile on button click
        display_entries()

    if st.sidebar.button("Update Entry"):
        st.session_state['show_profile'] = False  # Hide profile on button click
        st.write("### Update Entry")
        with st.form("update_form"):
            entry_id = st.number_input("Enter Entry ID", min_value=1)
            new_name = st.text_input("Enter new name")
            new_age = st.number_input("Enter new age", min_value=1, max_value=100)
            new_medical_condition = st.text_input("New Medical Condition")
            new_medications = st.text_input("New Medications")
            new_allergies = st.text_input("New Allergies")
            new_emergency_contact = st.text_input("New Emergency Contact Name")
            new_emergency_contact_phone = st.text_input("New Emergency Contact Phone")
            update_submit = st.form_submit_button("Update")
            if update_submit and entry_id and new_name and new_age:
                update_entry(entry_id, new_name, new_age, new_medical_condition, new_medications, new_allergies, new_emergency_contact, new_emergency_contact_phone)

# Main app entry point
def main():
    if st.session_state['logged_in']:
        dashboard()  # Show dashboard if logged in
    else:
        login_page()  # Show login page if not logged in

if __name__ == "__main__":
    main()
