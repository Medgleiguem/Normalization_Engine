# Quick Start Guide

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- Terminal/Command line access

## Setup (5 minutes)

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment (if not already created)
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### 2. Frontend Setup

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python run.py
```

Backend will run on: **http://localhost:5000**

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will run on: **http://localhost:3000**

## Using the Application

1. Open your browser to **http://localhost:3000**
2. Drag and drop an Excel file (.xlsx or .xls) or click to browse
3. Click "Start Analysis"
4. Wait for the normalization analysis to complete
5. Download your results:
   - **Academic Report** (DOCX)
   - **MySQL Script** (SQL)
   - **Normalized Excel** (XLSX)

## Sample Excel File Format

Your Excel file should have:

- **Headers in the first row** (column names)
- **Data in subsequent rows**
- **One table per sheet** (or use the first sheet)

Example:

```
| student_id | student_name | course1 | course2 | instructor1 | instructor2 |
|------------|--------------|---------|---------|-------------|-------------|
| 1          | John Doe     | Math    | Physics | Dr. Smith   | Dr. Jones   |
| 2          | Jane Smith   | Math    | Chem    | Dr. Smith   | Dr. Brown   |
```

The tool will automatically:

- Detect this violates 1NF (repeating groups: course1/course2)
- Normalize it to proper tables
- Generate comprehensive documentation

## Troubleshooting

### Backend won't start

- Check Python version: `python --version` (should be 3.8+)
- Ensure all dependencies installed: `pip list`
- Check port 5000 is not in use

### Frontend won't start

- Check Node version: `node --version` (should be 16+)
- Delete `node_modules` and run `npm install` again
- Check port 3000 is not in use

### File upload fails

- Ensure file is .xlsx or .xls format
- File size must be under 16MB
- Check backend is running

## Next Steps

- Read the full [README.md](file:///home/med/Desktop/normlawation/README.md) for detailed information
- Check [walkthrough.md](file:///home/med/.gemini/antigravity/brain/68e92ebd-dfd6-4e0d-9401-abecb31e64f0/walkthrough.md) for implementation details
- Review [implementation_plan.md](file:///home/med/.gemini/antigravity/brain/68e92ebd-dfd6-4e0d-9401-abecb31e64f0/implementation_plan.md) for architecture overview
