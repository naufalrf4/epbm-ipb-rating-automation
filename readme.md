
---

# EPBM IPB Rating Automation

---

## **Title**
This project is designed to automate the process of filling out course evaluations (EPBM) on the IPB Student Portal. It eliminates the need for manual input by automating the login process, navigating to the EPBM section, selecting courses, and filling out evaluation forms with a predefined star rating.

---

## **Author**
- **Name**: Naufal Rizqullah F  
- **Contact**: [naufalrf4@gmail.com](mailto:naufalrf4@gmail.com)  

---

## **Requirements**
Before running the script, ensure you have the following installed:

1. **Python 3.9 or higher**: Download from [python.org](https://www.python.org/downloads/).
2. **Google Chrome**: Download from [google.com/chrome](https://www.google.com/chrome/).
3. **ChromeDriver**: Download the version matching your Chrome browser from [ChromeDriver](https://sites.google.com/chromium.org/driver/).
4. **Environment Variables**: Create a `.env` file to store your credentials and ChromeDriver path.

---

## **Download**
1. Clone the repository:
   ```bash
   git clone https://github.com/naufalrf4/epbm-ipb-rating-automation.git
   cd epbm-ipb-rating-automation
   ```

---

## **Environment Settings**
1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file and update the following variables:
   ```env
   IPB_USERNAME=your_student_username
   IPB_PASSWORD=your_student_password
   CHROMEDRIVER_PATH=/path/to/chromedriver
   ```
   Replace `your_student_username`, `your_student_password`, and `/path/to/chromedriver` with your actual credentials and ChromeDriver path.

---

## **Install Requirements**
1. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
---

## **Setup**
1. Ensure the `.env` file is correctly configured.
2. Verify that ChromeDriver is installed and the path is correct in the `.env` file.

---

## **Run the Script**
1. Activate the virtual environment (if not already activated):
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Run the script:
   ```bash
   python main.py
   ```

---

## **Tutorial: How to Use the Star Score**
1. **Login**: The script will automatically log in to the IPB Student Portal using your credentials.
2. **Navigate to EPBM**: The script will load the EPBM page and display a list of courses.
3. **Select a Course**:
   - Courses that have not been evaluated will be highlighted in **blue**.
   - Courses that have already been evaluated will be highlighted in **green**.
   - Enter the number corresponding to the course you want to evaluate.
4. **Enter Star Rating**:
   - You will be prompted to enter a star rating (1-4) for all questions in the selected course.
   - The script will automatically fill in the star ratings for each question.
5. **Submit the Form**:
   - The script will navigate through all pages of the evaluation form.
   - If a "Selanjutnya" (Next) button is present, it will click it automatically.
   - On the final page, it will check the agreement checkbox (if required) and submit the form.
6. **Repeat**: The script will return to the course list, allowing you to evaluate another course or exit if all courses are completed.

---

## **Example Workflow**
1. Run the script:
   ```bash
   python main.py
   ```
2. The script will log in and display the list of courses:
   ```
   [INFO] Daftar matakuliah yang tersedia:
   [COURSE] 1. Course Title 1 - Description
   [INFO] 2. Course Title 2 - Description (Sudah Diisi)
   ```
3. Enter the number of the course you want to evaluate:
   ```
   Pilih matakuliah berdasarkan nomor (masukkan angka): 1
   ```
4. Enter the star rating (1-4):
   ```
   Masukkan rating (1-4) untuk semua pertanyaan: 4
   ```
5. The script will automatically fill in the ratings and submit the form.

---

## **Troubleshooting**
- **WebDriver Issues**: Ensure the correct version of ChromeDriver is installed and matches your Chrome browser version.
- **Login Failures**: Double-check your `.env` file to ensure the username and password are correct.
- **Timeout Errors**: If the script times out, ensure your internet connection is stable and the IPB Student Portal is accessible.

---

## **Changelog**
- **v1.0.0** (2024-12-05): Initial release with basic functionality for automating EPBM evaluations.

---

## **Contact Information**
For questions or feedback, please contact:  
- Name: Naufal Rizqullah F  
- Email: [naufalrf4@gmail.com](mailto:naufalrf4@gmail.com)  
- GitHub: [naufalrf4](https://github.com/naufalrf4)  
