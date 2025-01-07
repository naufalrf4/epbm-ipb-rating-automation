import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from colorama import Fore, Style, init
import sys

init(autoreset=True)

# Load env
load_dotenv()
USERNAME = os.getenv("IPB_USERNAME")
PASSWORD = os.getenv("IPB_PASSWORD")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

# Routes
BASE_URL = "https://studentportal.ipb.ac.id"
LOGIN_ROUTE = "/Account/Login"
EPBM_HOME_ROUTE = "/Akademik/EPBM/"

# Configure Selenium 
options = Options()
options.add_argument("--start-maximized")
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title():
    title = """
=====================================
EPBM Score Automation
by: NaufalRF
=====================================|
    """
    try:
        terminal_size = os.get_terminal_size().columns
    except OSError:
        terminal_size = 80
    lines = title.strip().split("\n")
    for line in lines:
        print(Fore.CYAN + line.center(terminal_size) + Style.RESET_ALL)
    print()


def log_message(message, level="INFO"):
    colors = {
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "COURSE": Fore.CYAN
    }
    print(f"{colors.get(level, '')}[{level}] {message}{Style.RESET_ALL}")


def login():
    clear_console()
    print_title()
    try:
        log_message("Mengarahkan ke halaman login...")
        driver.get(BASE_URL + LOGIN_ROUTE)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Username")))

        log_message("Memasukkan kredensial...")
        driver.find_element(By.ID, "Username").send_keys(USERNAME)
        driver.find_element(By.ID, "Password").send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        WebDriverWait(driver, 10).until(EC.url_contains(BASE_URL))
        log_message("Berhasil login!")
    except TimeoutException:
        log_message("Gagal login. Waktu habis saat memuat halaman login.", "ERROR")
        driver.quit()
        sys.exit(1)
    except WebDriverException as e:
        log_message(f"Terjadi kesalahan saat login: {e}", "ERROR")
        driver.quit()
        sys.exit(1)


def navigate_to_epbm():
    try:
        clear_console()
        print_title()
        log_message("Mengarahkan ke halaman EPBM...")
        driver.get(BASE_URL + EPBM_HOME_ROUTE)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card.small-box")))

        courses = driver.find_elements(By.CLASS_NAME, "card.small-box")

        completed_courses = []
        not_completed_courses = []

        for course in courses:
            course_title = course.find_element(By.TAG_NAME, "h4").text
            course_desc = course.find_element(By.TAG_NAME, "p").text
            completed_icon = course.find_elements(By.CSS_SELECTOR, ".icon .fa-check-circle.text-success")

            if completed_icon:
                completed_courses.append((course, course_title, course_desc))
            else:
                not_completed_courses.append((course, course_title, course_desc))

        log_message("Daftar matakuliah yang tersedia:", "INFO")

        index = 1
        for c, title, desc in not_completed_courses:
            log_message(f"{index}. {title} - {desc}", "COURSE")  # Belum diisi = biru
            index += 1

        for c, title, desc in completed_courses:
            log_message(f"{index}. {title} - {desc} (Sudah Diisi)", "INFO")  # Sudah diisi = hijau
            index += 1

        if not not_completed_courses:
            log_message("Semua matakuliah sudah diisi.", "INFO")
            return None
        return not_completed_courses
    except TimeoutException:
        log_message("Gagal memuat halaman EPBM. Waktu habis.", "ERROR")
        driver.quit()
        sys.exit(1)
    except WebDriverException as e:
        log_message(f"Terjadi kesalahan saat mengarahkan ke EPBM: {e}", "ERROR")
        driver.quit()
        sys.exit(1)

def select_course(not_completed_courses):
    while True:
        try:
            choice = int(input("Pilih matakuliah berdasarkan nomor (masukkan angka): ")) - 1
            if 0 <= choice < len(not_completed_courses):
                course_url = not_completed_courses[choice][0].get_attribute("href")
                log_message(f"Mengarahkan ke matakuliah: {not_completed_courses[choice][1]} - {not_completed_courses[choice][2]}", "INFO")
                driver.get(course_url)
                return True
            else:
                log_message("Pilihan tidak valid. Silakan pilih nomor matakuliah yang benar.", "WARNING")
        except ValueError:
            log_message("Input tidak valid. Silakan masukkan angka.", "WARNING")

def select_star_rating():
    clear_console()
    print_title()
    while True:
        try:
            star_rating = int(input("Masukkan rating (1-4) untuk semua pertanyaan: "))
            if 1 <= star_rating <= 4:
                return star_rating
            else:
                log_message("Rating tidak valid. Masukkan nilai antara 1 dan 4.", "WARNING")
        except ValueError:
            log_message("Input tidak valid. Silakan masukkan angka antara 1 dan 4.", "WARNING")


def fill_course(star_rating):
    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "list-group-item"))
            )
            questions = driver.find_elements(By.CLASS_NAME, "list-group-item")

            if not questions:
                log_message("Tidak ada pertanyaan di halaman ini. Mungkin form sudah selesai atau tidak perlu rating.", "INFO")
                break

            for index, question in enumerate(questions, start=1):
                log_message(f"Memberikan rating {star_rating} bintang untuk Pertanyaan {index}.", "INFO")
                stars = question.find_elements(By.CLASS_NAME, "b-rating-star")

                if len(stars) < star_rating:
                    log_message(f"Jumlah bintang tidak mencukupi untuk Pertanyaan {index}. Melewati...", "WARNING")
                    continue

                driver.execute_script("arguments[0].scrollIntoView(true);", stars[star_rating - 1])
                time.sleep(0.2)
                try:
                    stars[star_rating - 1].click()
                    log_message(f"Berhasil memberikan rating untuk Pertanyaan {index}.", "INFO")
                except Exception as e:
                    log_message(f"Gagal memberikan rating untuk Pertanyaan {index}: {e}", "ERROR")

            try:
                next_button = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//button[text()='Selanjutnya']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", next_button)
                log_message("Berhasil klik tombol 'Selanjutnya' menggunakan JavaScript.", "INFO")
            except TimeoutException:
                log_message("Tidak ada tombol 'Selanjutnya'. Ini kemungkinan halaman terakhir.", "INFO")
                try:
                    agreement_checkbox = driver.find_element(
                        By.CSS_SELECTOR, ".alert.mt-4.alert-danger input[type='checkbox']"
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", agreement_checkbox)
                    time.sleep(0.2)
                    agreement_checkbox.click()
                    log_message("Kotak centang persetujuan telah dicentang.", "INFO")
                except NoSuchElementException:
                    log_message("Kotak centang persetujuan tidak ditemukan atau tidak diperlukan.", "INFO")

                try:
                    submit_button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Simpan EPBM')]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                    time.sleep(0.2)
                    driver.execute_script("arguments[0].click();", submit_button)
                    log_message("Formulir berhasil dikirim!", "INFO")
                except TimeoutException:
                    log_message("Gagal menemukan tombol 'Simpan EPBM'.", "ERROR")
                except WebDriverException as e:
                    log_message(f"Kesalahan saat mencoba mengirimkan formulir: {e}", "ERROR")
                break

        except TimeoutException:
            log_message("Timeout saat menunggu pertanyaan muncul. Mungkin form sudah selesai.", "INFO")
            break
        except Exception as e:
            log_message(f"Terjadi kesalahan tak terduga saat memproses form: {e}", "ERROR")
            break


def main():
    try:
        login()

        while True:
            not_completed_courses = navigate_to_epbm()
            if not not_completed_courses:
                break

            if not select_course(not_completed_courses):
                break

            star_rating = select_star_rating()
            fill_course(star_rating)

        log_message("Tidak ada matakuliah yang perlu diisi.", "INFO")

    except Exception as e:
        log_message(f"Terjadi kesalahan tidak terduga: {e}", "ERROR")
    finally:
        log_message("Menutup browser...", "INFO")
        driver.quit()


if __name__ == "__main__":
    main()
