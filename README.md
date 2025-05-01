# 🚀 FastAPI Blog API

A simple RESTful API built with **FastAPI**, **SQLAlchemy**, and **MySQL** to manage users and blog posts.

## 📦 Features

- Create, read, update delete users
- Create and read posts
- Simple MySQL database backend
- Automatically generated interactive API docs (Swagger UI)

---

## 🛠️ Setup Instructions


```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name 
```

```
On windows
python -m venv venv
.\venv\Scripts\activate

On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

```
Install dependencies
pip install -r requirements.txt
```

```
Run the fastAPI Server
uvicorn main:app --reload
```

Visit the API docs at:
Swagger UI: http://127.0.0.1:8000/docs