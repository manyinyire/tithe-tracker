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
- PostgreSQL database
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/manyinyire/tithe-tracker.git
cd tithe-tracker
```

2. Install the required packages:
```bash
pip install plotly psycopg2-binary python-jose streamlit bcrypt jose pandas
```

## Environment Setup

Create a `.env` file in the root directory with the following variables:

```env
DATABASE_URL=your_postgresql_database_url
```

## Running the Application

1. Start the Streamlit application:
```bash
streamlit run main.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Database Setup

The application automatically handles database migrations and table creation on startup. No additional setup is required.

## Features Overview

### Income Management
- Add one-time or recurring income entries
- View and manage income history
- Categorize different income sources

### Tithe Calculations
- Automatic calculation of tithes based on income
- Support for different tithe calculation methods
- Historical tithe tracking

### Data Visualization
- Interactive charts showing income trends
- Tithe payment history visualization
- Financial insights dashboard

### User System
- Secure user authentication
- Personal profile management
- Individual tithe tracking

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
