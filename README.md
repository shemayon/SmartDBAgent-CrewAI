# SmartDBAgent-CrewAI

An intelligent CRUD (Create, Read, Update, Delete) system for managing student records in MySQL, automated by a GPT-4-powered agent using the CrewAI framework.

## 🚀 Agent Overview

This project demonstrates how to build an AI-driven database management system that can autonomously perform CRUD operations on a MySQL database. It uses:

- **CrewAI** to define tools, agents, tasks and crews  
- **GPT-4-powered agent** to interpret user intents and call the right database tool  
- **Custom caching strategy** to optimize repetitive operations  
- **Python** for orchestration  
- **MySQL** as the backend data store  

## 🔑 Key Features

- **Automated CRUD**: Create, read, update and delete student records without manual SQL  
- **Task & Crew Management**: Use CrewAI’s `Agent`, `Task` and `Crew` primitives for structured workflows  
- **Caching**: Speed up repeated calls with a custom cache strategy  
- **Extensible**: Easily add new database tables or tools  

## 📦 Tech Stack

- Python 3.8+  
- MySQL  
- [CrewAI](https://github.com/crewai/crewai)  
- OpenAI GPT-4 (via `gpt-4o-mini` model)  

## ⚙️ Prerequisites

- Python 3.8 or later  
- MySQL server (local or remote)  
- OpenAI API key  
- `pip install -r requirements.txt`  

## 🔧 Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/shemayon/SmartDBAgent-CrewAI.git
   cd ai-student-db-manager
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**  
   - export OPENAI_API_KEY="your_api_key" 
   - Fill in your MySQL connection URL and `OPENAI_API_KEY`


## 🚀 Usage

Run the main application to see example CRUD operations in action:

```bash
python app.py
```

You should see output similar to:

```
Student added successfully
Student updated successfully
Student deleted successfully
[{'ID': 2, 'Name': 'Alice', 'Age': 19, 'Grade': 'A'}]
```

### Integrating into your own app

Import and call `perform_action`:

```python
from app import perform_action

# Create
perform_action("create", name="Jane Doe", age=22, grade="B")

# Read
students = perform_action("read")

# Update
perform_action("update", id=2, grade="A+")

# Delete
perform_action("delete", id=2)
```


## 🤝 Contributing

1. Fork this repository  
2. Create a feature branch (`git checkout -b feature/new-tool`)  
3. Commit your changes (`git commit -m "Add new tool"`)  
4. Push to the branch (`git push origin feature/new-tool`)  
5. Open a Pull Request  

## 📄 License

This project is licensed under the MIT License.  
```
