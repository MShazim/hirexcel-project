# HIREXCEL

## Overview
HIREXCEL is a pre-interview assessment platform designed to streamline the recruitment process by dynamically assessing candidates' cognitive skills, emotional intelligence, technical skills, and personality traits. The platform integrates OpenAI's ChatGPT API to provide automated assessments and is built using Python and Django.

## Features
- **Dynamic Assessments**: Evaluate candidates based on multiple dimensions such as personality traits, cognitive skills, and technical proficiency.
- **ChatGPT Integration**: Automate result evaluation using OpenAI's ChatGPT API.
- **Role-Based Functionality**: Supports job seekers, recruiters, and administrators.
- **Customizable Job Criteria**: Tailor assessments to specific job requirements.
- **Modern Design**: Built using the Vuexy theme for an intuitive and professional user interface.

## System Specifications
- **Language**: Python, HTML, CSS, JavaScript
- **Framework**: Django
- **Libraries**: OpenAI
- **Database**: SQLite3
- **Theme**: Vuexy


## Prerequisites
To run HIREXCEL locally, ensure you have the following installed:
1. Python 3.9 or later
2. Pip (Python package manager)
3. SQLite3

## Setup Instructions

### 1. Clone the Repository
```bash
# Clone the repository
git clone https://github.com/mshazim/hirexcel.git
cd hirexcel
```

### 2. Set Up Virtual Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
# Install required Python packages
pip install -r requirements.txt
```


### 4. Configure Environment Variables
Create a `.env` file in the project root directory and add the following:
```
SECRET_KEY=your_secret_key
DEBUG=True
OPENAI_API_KEY=your_openai_api_key
```

### 5. Run Database Migrations
```bash
# Apply database migrations
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser
```bash
# Create an admin user
python manage.py createsuperuser
```

### 7. Start the Development Server
```bash
# Run the server
python manage.py runserver

# Access the application at http://127.0.0.1:8000
```

## Usage
- Navigate to the admin panel at `http://127.0.0.1:8000/admin` to manage users, jobs, and assessments.
- Job seekers can create accounts, complete assessments, and apply for jobs.
- Recruiters can post jobs, define criteria, and review candidates' results.

## Testing
HIREXCEL includes a suite of tests to verify functionality. To run the tests, use:
```bash
python manage.py test
```

## **Project Status**

- **Branch Name:** `<!-- BRANCH_NAME -->`
- **Total Commits:** <!-- TOTAL_COMMITS -->
- **Last 3 Commits:**
  1. <!-- COMMIT_1 -->
  2. <!-- COMMIT_2 -->
  3. <!-- COMMIT_3 -->

## Contributing
We welcome contributions to improve HIREXCEL! Please follow these steps:
1. Fork the repository
2. Create a new branch for your feature/fix
3. Commit your changes
4. Push your branch and submit a pull request

## License
HIREXCEL is licensed under the MIT License. See `LICENSE` for details.

## Acknowledgments
- OpenAI for the ChatGPT API
- The Vuexy team for the frontend theme

For questions or support, please contact mehmoodsheikh312@gmail.com.



