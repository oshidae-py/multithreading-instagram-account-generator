import time
import undetected_chromedriver as uc
from RecaptchaSolver import RecaptchaSolver

# Initialize the undetected ChromeDriver
driver = uc.Chrome()

try:
    # Navigate to the demo reCAPTCHA page
    driver.get("https://www.google.com/recaptcha/api2/demo")

    # Initialize the reCAPTCHA solver
    recaptcha_solver = RecaptchaSolver(driver)

    # Attempt to solve the reCAPTCHA
    print("Attempting to solve reCAPTCHA...")
    recaptcha_solver.solveCaptcha()
    print("reCAPTCHA solved successfully!")

    # Submit the form
    submit_button = driver.find_element(By.ID, "recaptcha-demo-submit")
    submit_button.click()
    print("Form submitted successfully.")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Clean up and close the driver
    time.sleep(5)
    driver.quit()
