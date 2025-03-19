# 🌍 Sahel Dashboard

This is a web application that provides a **dashboard to visualize data about the expansion of the Sahel desert**.  
It is built using **Django (Backend) and React (Frontend)**.

---

##  Getting Started

### 1️ **Clone the Repository**
```bash
git clone https://github.com/MarcelNamyslo/sahel-dashboard.git
cd sahel-dashboard
```

---

##  **Backend Setup (Django)**

1. **Navigate to the `backend/` folder**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**
   - **Windows (cmd):**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     venv\Scripts\Activate.ps1
     ```
   - **Mac/Linux:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. *(Optional: Create a superuser for the Django admin panel)*
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Django backend**
   ```bash
   python manage.py runserver
   ```

---

## **Frontend Setup (React)**

1. **Navigate to the `frontend/` folder**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the React frontend**
   ```bash
   npm start
   ```

---

## **API Endpoints**
- **Backend is running at:** `http://127.0.0.1:8000/`
- **Frontend is running at:** `http://localhost:3000/`
- **Django API (example endpoint):** `http://127.0.0.1:8000/api/data/`





