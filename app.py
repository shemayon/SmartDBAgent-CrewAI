import os
from crewai import Agent, Task, Crew, Process, tool
from crewai import LLM
import mysql.connector
from database import get_db_connection
from typing import Optional, List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache strategy for tools
def cache_strategy(*args, **kwargs):
    return f"{args}_{kwargs}"

# Tool Performing CRUD Operations
@tool("Create Student")
def create_student(ID: int, name: str, age: int, grade: str) -> str:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (Name, Grade, Age) VALUES (%s, %s, %s)", (name, grade, age))
        conn.commit()
        return "Student added successfully"
    except Exception as e:
        logger.error(f"Error creating student: {str(e)}")
        conn.rollback()
        return f"Error creating student: {str(e)}"
    finally:
        cursor.close()
        conn.close()

create_student.cache_function = cache_strategy

@tool("Read Students")
def read_students() -> List[Dict[str, Any]]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        return students
    except Exception as e:
        logger.error(f"Error reading students: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

@tool("Update Student")
def update_student(ID: int, name: Optional[str] = None, age: Optional[int] = None, grade: Optional[str] = None) -> str:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        update_fields = []
        values = []
        if name:
            update_fields.append("name = %s")
            values.append(name)
        if age:
            update_fields.append("age = %s")
            values.append(age)
        if grade:
            update_fields.append("grade = %s")
            values.append(grade)
        values.append(ID)
        query = f"UPDATE students SET {', '.join(update_fields)} WHERE ID = %s"
        cursor.execute(query, tuple(values))
        conn.commit()
        return "Student updated successfully"
    except Exception as e:
        logger.error(f"Error updating student: {str(e)}")
        conn.rollback()
        return f"Error updating student: {str(e)}"
    finally:
        cursor.close()
        conn.close()

@tool("Delete Student")
def delete_student(student_id: int) -> str:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE ID = %s", (student_id,))
        conn.commit()
        return "Student deleted successfully"
    except Exception as e:
        logger.error(f"Error deleting student: {str(e)}")
        conn.rollback()
        return f"Error deleting student: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# Defining Agent
crud_agent = Agent(
    role = "Student Manager",
    goal = "Manage students in the MySQL database efficiently",
    backstory = """
    You are an expert in MySQL database operations.
    You find the {action} and then as per action, you will be able to call a function to perform the action.
    Your responsibility is to create, read, update, and delete student records as per user {action}.
    Do not add any extra information, use only input data
    """,
    verbose = True,
    llm = LLM(
        model="gpt-4o-mini",
        temperature=0.5,
        base_url="https://api.openai.com/v1",
        api_key=os.getenv("OPENAI_API_KEY")
    ),
    tools = [create_student, read_students, update_student, delete_student]
)

# Define Tasks and Crews for each operation
def create_task(description: str, agent: Agent) -> Task:
    return Task(
        description=description,
        expected_output="Successfully managed student data.",
        agent=agent
    )

def create_crew(agent: Agent, task: Task) -> Crew:
    return Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

tasks = {
    'create': create_task("Create a new student record with the provided details", crud_agent),
    'read': create_task("Retrieve all student records from the database", crud_agent),
    'update': create_task("Update an existing student record with the provided details", crud_agent),
    'delete': create_task("Delete a student record with the specified ID", crud_agent),
}

def perform_action(action: str, id: Optional[int] = None, name: Optional[str] = None, 
                  age: Optional[int] = None, grade: Optional[str] = None) -> Any:
    try:
        inputs = {"action": action, "id": id, "name": name, "age": age, "grade": grade}
        crew = create_crew(crud_agent, tasks[action])
        response = crew.kickoff(inputs=inputs)
        return response.raw
    except Exception as e:
        logger.error(f"Error performing action {action}: {str(e)}")
        return f"Error performing action: {str(e)}"

if __name__ == "__main__":
    # Example usage
    print(perform_action("create", name="John Doe", age=20, grade="A"))
    print(perform_action("update", id=1, name="John Smith", age=21, grade="B"))
    print(perform_action("delete", id=1))
    print(perform_action("read"))
    
    