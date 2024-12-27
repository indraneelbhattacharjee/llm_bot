### Hospital Appointment Scheduler

#### Overview
The Hospital Appointment Scheduler is a web-based application designed to simplify the process of booking hospital appointments. It features a chatbot interface powered by OpenAI's GPT-3.5, allowing users to schedule appointments, get assistance, and view scheduled appointments. The system includes a Flask backend, Streamlit frontend, and SQLite database.

---

#### Features
- **Conversational Interface**: Users can interact with a chatbot for help with appointments.
- **Appointment Booking**: Book hospital appointments with details like specialty, date, time, and email confirmation.
- **View Scheduled Appointments**: View all your scheduled appointments in an organized list.
- **Email Notifications**: Users receive email confirmation upon successful appointment booking.
- **User-Friendly Interface**: Streamlit provides a clean and intuitive user experience.

---

#### Tech Stack
- **Frontend**: Streamlit
- **Backend**: Flask
- **Database**: SQLite
- **API**: OpenAI GPT-3.5

---

#### Installation and Setup

1. **Clone the Project**
   - Download the project files to your local system.

2. **Set Up Python Environment**
   - Ensure Python 3.10 is installed.
   - Create a virtual environment:
     ```bash
     python3.10 -m venv venv
     source venv/bin/activate
     ```
   - Upgrade `pip`:
     ```bash
     pip install --upgrade pip
     ```

3. **Install Dependencies**
   - Install the required Python libraries:
     ```bash
     pip install -r requirements.txt
     ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the project directory and add the following:
     ```
     OPENAI_API_KEY=your_openai_api_key
     EMAIL_HOST=your_email_host
     EMAIL_PORT=your_email_port
     EMAIL_USER=your_email_user
     EMAIL_PASSWORD=your_email_password
     ```

5. **Initialize the Database**
   - Run the following Python commands to set up the database:
     ```bash
     python
     >>> from database import init_db
     >>> init_db()
     >>> exit()
     ```

6. **Run the Application**
   - Start the Flask backend:
     ```bash
     flask run
     ```
   - Start the Streamlit frontend:
     ```bash
     streamlit run streamlit_app.py
     ```

---

#### Usage
1. Open the Streamlit app in your browser (default: `http://localhost:8501`).
2. Use the chatbot to get assistance or directly input details to book an appointment.
3. View scheduled appointments in the "Your Appointments" section.

---

#### Project Structure
```plaintext
Appointment-Scheduler/
├── app.py                 # Flask backend
├── bot.py                 # Chatbot integration with OpenAI API
├── database.py            # Database handling for appointments
├── streamlit_app.py       # Streamlit frontend
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables file
├── README.md              # Documentation
```

---

#### Future Enhancements
- Add voice input support for chatbot interactions.
- Implement user authentication and profile management.
- Allow users to reschedule or cancel appointments.
- Include appointment reminders via email.

---

#### License
This project is provided as-is for educational and demonstration purposes. Use it as a template for further development.