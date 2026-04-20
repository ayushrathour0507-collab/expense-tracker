# Expense Tracker - Full Stack Application

A complete full-stack expense tracking application built with FastAPI (backend) and React + Vite (frontend), with Supabase PostgreSQL for data persistence.

## 🎯 Features

### Authentication
- ✅ User Registration
- ✅ User Login with JWT tokens
- ✅ Secure password hashing with bcrypt
- ✅ Token-based authorization

### Expense Management
- ✅ Add new expenses with amount, category, date, and note
- ✅ View all user expenses in a table
- ✅ Delete expenses
- ✅ View expense summary by category
- ✅ Responsive design with Tailwind CSS

## 📋 Project Structure

```
expense-tracker/
├── backend/
│   ├── main.py                 # FastAPI app setup
│   ├── database.py             # SQLAlchemy setup with Supabase
│   ├── models.py               # User and Expense models
│   ├── schemas.py              # Pydantic schemas
│   ├── auth.py                 # JWT auth & password functions
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables
│   └── routes/
│       ├── __init__.py
│       ├── auth_routes.py       # Register & Login endpoints
│       └── expense_routes.py    # Expense CRUD endpoints
│
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Login.jsx        # Login page
    │   │   ├── Register.jsx     # Registration page
    │   │   ├── Dashboard.jsx    # Main dashboard
    │   │   └── AddExpense.jsx   # Add expense form
    │   ├── services/
    │   │   └── api.js           # Axios API client
    │   ├── App.jsx              # Main app component
    │   ├── main.jsx             # React entry point
    │   └── index.css            # Global styles
    ├── index.html               # HTML template
    ├── package.json             # npm dependencies
    ├── vite.config.js           # Vite configuration
    ├── tailwind.config.js       # Tailwind CSS config
    └── postcss.config.js        # PostCSS config
```

## 🚀 Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Update `.env` file with your Supabase credentials:**
   ```
   DATABASE_URL=postgresql+psycopg://postgres.xxxxx:password@aws-region.pooler.supabase.com:6543/postgres?sslmode=require
   JWT_SECRET=your-long-random-secret-key-min-32-chars
   ```

4. **Start the backend server:**
   ```bash
   python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

   The API will be available at: `http://127.0.0.1:8000`
   API documentation: `http://127.0.0.1:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at: `http://127.0.0.1:5173`

## 📖 API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Expenses
- `GET /expenses` - Get all user expenses
- `POST /expenses` - Create a new expense
- `PUT /expenses/{id}` - Update an expense
- `DELETE /expenses/{id}` - Delete an expense
- `GET /expenses/summary` - Get expense summary by category

## 🔐 Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql+psycopg://user:password@host:port/database?sslmode=require
JWT_SECRET=your-secret-key-here
```

## 🛠️ Technology Stack

### Backend
- **Framework:** FastAPI
- **Database:** PostgreSQL (Supabase) with Connection Pooler
- **ORM:** SQLAlchemy
- **Authentication:** JWT (python-jose)
- **Password Hashing:** bcrypt (passlib)
- **Validation:** Pydantic

### Frontend
- **Framework:** React 18.2.0
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **Routing:** React Router DOM 6
- **State Management:** React Hooks

## 📝 Usage Guide

### Register & Login
1. Visit `http://127.0.0.1:5173`
2. Click "Register here" to create a new account
3. Enter your email and password (min 8 characters)
4. You'll be automatically logged in and redirected to dashboard

### Add Expenses
1. Click "+ Add New Expense" button on dashboard
2. Fill in the expense details:
   - **Amount:** The expense amount (required)
   - **Category:** Select from predefined categories (required)
   - **Date:** Pick a date (required)
   - **Note:** Optional description
3. Click "Add Expense"

### View & Manage Expenses
- Dashboard shows all your expenses in a table
- View category-wise summary on the left
- See total expenses at the top
- Click "Delete" to remove an expense

### Logout
- Click "Logout" button in the top-right corner

## 🔄 Data Flow

```
Frontend (React) 
  ↓ (HTTP Requests via Axios)
API Routes (FastAPI)
  ↓ (Query/Update via SQLAlchemy ORM)
PostgreSQL (Supabase)
  ↓ (JSON Response)
Frontend (Display/Update UI)
```

## 🔒 Security Features

- ✅ JWT token-based authentication
- ✅ Password hashing with bcrypt
- ✅ Protected API endpoints (require authentication)
- ✅ Token stored in localStorage (frontend)
- ✅ Token sent in Authorization header
- ✅ CORS enabled for frontend-backend communication
- ✅ Email validation and uniqueness checks

## 🐛 Troubleshooting

### Database Connection Issues
- Verify your Supabase pooler URL is correct
- Check that credentials are properly URL-encoded
- Ensure Connection Pooler is enabled in Supabase settings

### Frontend can't connect to backend
- Verify backend is running on `http://127.0.0.1:8000`
- Check CORS is enabled (should be in main.py)
- Check browser console for error messages

### JWT Token errors
- Clear localStorage: `localStorage.clear()` in browser console
- Log out and log back in
- Verify JWT_SECRET is set in `.env`

## 📞 Support

For issues or questions, refer to:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Supabase Documentation](https://supabase.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## 📄 License

This project is open source and available under the MIT License.
