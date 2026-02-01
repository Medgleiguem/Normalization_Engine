# Database Normalization Analysis Tool

A comprehensive web application that analyzes Excel files for database normalization compliance (1NF through 5NF), generates university-standard academic reports, produces MySQL scripts with best practices, and outputs normalized Excel files.

## Features

- **AI-Powered Dependency Detection**: Automatically detects functional dependencies, multi-valued dependencies, and candidate keys using statistical analysis
- **Comprehensive Normalization Analysis**: Analyzes tables for all normal forms (1NF, 2NF, 3NF, BCNF, 4NF, 5NF)
- **Academic-Standard Reports**: Generates detailed DOCX reports with theoretical background, step-by-step analysis, and references
- **MySQL Script Generation**: Creates production-ready SQL scripts with best practices, constraints, indexes, and comprehensive comments
- **Normalized Excel Output**: Produces normalized Excel files with metadata, data dictionary, and relationship diagrams
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS

## Tech Stack

### Backend

- **Flask**: Python web framework
- **pandas & openpyxl**: Excel file processing
- **scikit-learn**: AI-powered dependency detection
- **python-docx**: Report generation
- **Flask-CORS**: Cross-origin resource sharing

### Frontend

- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animations
- **Axios**: HTTP client
- **Lucide React**: Icon library

## Project Structure

```
normlawation/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── config.py            # Configuration
│   │   ├── routes/              # API endpoints
│   │   │   ├── upload_routes.py
│   │   │   ├── analysis_routes.py
│   │   │   └── download_routes.py
│   │   ├── services/            # Business logic
│   │   │   ├── excel_parser.py
│   │   │   ├── ai_dependency_detector.py
│   │   │   ├── normalization_engine.py
│   │   │   ├── report_generator.py
│   │   │   ├── sql_generator.py
│   │   │   └── excel_generator.py
│   │   ├── models/              # Data models
│   │   │   ├── table_model.py
│   │   │   └── analysis_result.py
│   │   └── utils/               # Utilities
│   │       └── file_handler.py
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── components/          # React components
    │   │   ├── FileUpload.jsx
    │   │   ├── AnalysisProgress.jsx
    │   │   └── ResultsPanel.jsx
    │   ├── pages/
    │   │   └── HomePage.jsx
    │   ├── services/
    │   │   └── api.js
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── .env.example
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create environment file:

```bash
cp .env.example .env
```

5. Run the Flask server:

```bash
python run.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Create environment file:

```bash
cp .env.example .env
```

4. Run the development server:

```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Upload an Excel file (.xlsx or .xls) containing your database table
3. Click "Start Analysis" to begin the normalization process
4. Wait for the AI-powered analysis to complete
5. Download your results:
   - **Academic Report** (DOCX): Comprehensive analysis with theoretical background
   - **MySQL Script** (SQL): Production-ready database schema
   - **Normalized Excel** (XLSX): Normalized data with metadata

## How It Works

### 1. Excel Parsing

- Extracts table structures and data from Excel files
- Infers SQL data types from column values
- Analyzes column properties (nullable, unique, etc.)

### 2. AI-Powered Dependency Detection

- Uses statistical analysis to detect functional dependencies
- Calculates determination coefficients for dependency confidence
- Identifies candidate keys through uniqueness analysis
- Detects multi-valued dependencies using mutual information

### 3. Normalization Analysis

- **1NF**: Checks for atomic values and repeating groups
- **2NF**: Detects partial dependencies
- **3NF**: Identifies transitive dependencies
- **BCNF**: Verifies determinant constraints
- **4NF**: Checks for multi-valued dependencies
- **5NF**: Analyzes join dependencies

### 4. Output Generation

- **Report**: Academic-standard DOCX with step-by-step analysis
- **SQL Script**: MySQL schema with constraints, indexes, and comments
- **Excel File**: Normalized tables with metadata and relationships

## Best Practices Implemented

### Backend

- ✅ Modular architecture with separation of concerns
- ✅ Service layer pattern for business logic
- ✅ Data models for type safety
- ✅ Comprehensive error handling
- ✅ Environment-based configuration
- ✅ CORS configuration for security
- ✅ File validation and cleanup

### Frontend

- ✅ Component-based architecture
- ✅ Custom hooks for reusability
- ✅ Responsive design with Tailwind CSS
- ✅ Smooth animations with Framer Motion
- ✅ Error boundaries and user feedback
- ✅ Accessibility considerations
- ✅ SEO optimization

### Code Quality

- ✅ Clean, readable code with comments
- ✅ Consistent naming conventions
- ✅ DRY (Don't Repeat Yourself) principles
- ✅ Single Responsibility Principle
- ✅ Proper file organization

## License

MIT

## Author

Created with ❤️ using AI-powered development
