# Tithe Tracker

A faith-based tithe tracking application that enables users to manage and calculate their tithes based on income inputs. The system provides comprehensive income management with support for both one-time and recurring transactions, automated tithe calculations, and data visualization components for financial insights.

## Features

- Income tracking with recurring transaction support
- Automated tithe calculations
- Interactive data visualizations
- Scripture notification system
- User verification system
- Faith-based UI theme implementation

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.11 or higher
- PostgreSQL database (version 12 or higher)
- Git

## Detailed Installation Guide

### 1. System Dependencies

#### For Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install python3.11 python3.11-dev
sudo apt-get install postgresql postgresql-contrib
```

#### For MacOS (using Homebrew):
```bash
brew install python@3.11
brew install postgresql
```

### 2. Clone the Repository
```bash
git clone https://github.com/manyinyire/tithe-tracker.git
cd tithe-tracker
```

### 3. Set Up Python Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 4. Install Required Packages
```bash
pip install -r requirements.txt
```

### 5. Database Setup

#### Create PostgreSQL Database
```bash
psql -U postgres
CREATE DATABASE tithe_tracker;
\q
```

### 6. Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/tithe_tracker

# Application Settings
STREAMLIT_SERVER_PORT=5000
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Security Settings (Generate using secure methods)
SECRET_KEY=your_secure_secret_key
```

## Running the Application

### 1. Start PostgreSQL Service
```bash
# On Ubuntu/Debian
sudo service postgresql start

# On MacOS
brew services start postgresql
```

### 2. Start the Application
```bash
streamlit run main.py
```

The application will be available at `http://localhost:5000`

## Development Setup

### Setting Up Development Environment

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Set up pre-commit hooks:
```bash
pre-commit install
```

### Running Tests
```bash
pytest tests/
```

### Code Style
This project follows PEP 8 style guide. Run the linter:
```bash
flake8 .
```

## Features Overview

### Income Management
- Add one-time or recurring income entries
- View and manage income history
- Categorize different income sources
- Bulk import/export functionality

### Tithe Calculations
- Automatic calculation of tithes based on income
- Support for different tithe calculation methods
- Historical tithe tracking
- Custom calculation rules

### Data Visualization
- Interactive charts showing income trends
- Tithe payment history visualization
- Financial insights dashboard
- Export reports in multiple formats

### User System
- Secure user authentication
- Personal profile management
- Individual tithe tracking
- Role-based access control

## Troubleshooting

### Common Issues

1. Database Connection Issues
```
Error: Could not connect to PostgreSQL database
Solution: Check if PostgreSQL service is running and credentials in .env are correct
```

2. Port Already in Use
```
Error: Port 5000 is already in use
Solution: Change the port in .env file or stop the process using that port
```

3. Package Installation Failures
```
Error: Failed to install requirements
Solution: Ensure you're using Python 3.11 and have proper system dependencies
```

## Database Schema

The application uses the following core tables:

- `users`: User authentication and profile data
- `income_entries`: Income transaction records
- `tithe_calculations`: Calculated tithe amounts
- `recurring_transactions`: Scheduled recurring income entries

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
