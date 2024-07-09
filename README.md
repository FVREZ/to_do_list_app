# To Do List App

## Features
- User Sign Up & Login
- Profile Editing & Password Reset
- Add Tasks and Create To Do Lists
- Categorize Tasks
- Change Task Status (To Do, Urgent, Done, etc.)

## Setup Instructions

### Prerequisites
- Python 3.x installed
- MongoDB installed and running

### Installation

1. Clone the repository:
   \\\ash
   git clone https://github.com/your-username/to_do_list_app.git
   cd to_do_list_app
   \\\

2. Create a virtual environment and activate it:
   \\\ash
   python -m venv venv
   source venv/bin/activate  # On Windows use \env\Scripts\activate\
   \\\

3. Install the dependencies:
   \\\ash
   pip install -r requirements.txt
   \\\

4. Set up your environment variables in a \.env\ file:
   \\\
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   MONGO_URI=mongodb://localhost:27017/iw_DATABASE
   \\\

5. Run the application:
   \\\ash
   flask run
   \\\

The app will be running at \http://localhost:5000\.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
