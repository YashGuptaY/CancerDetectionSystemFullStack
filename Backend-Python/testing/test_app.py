from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the web app
driver.get("http://127.0.0.1:5000/")  # Update the URL if hosted elsewhere
driver.maximize_window()

# Explicit wait setup
wait = WebDriverWait(driver, 10)

# Sample test data
test_values = [
    14.2, 20.5, 90.2, 600.3, 0.1, 0.3, 0.4, 0.2, 0.2, 0.08,
    0.5, 1.2, 3.1, 20.0, 0.02, 0.03, 0.04, 0.03, 0.02, 0.001,
    16.2, 25.5, 110.2, 800.3, 0.15, 0.25, 0.35, 0.18, 0.25, 0.09
]

# Wait for input fields to be visible
input_fields = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))

for i, field in enumerate(input_fields):
    field.clear()
    field.send_keys(str(test_values[i]))

# Wait for the "Predict" button to be clickable
predict_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))

# Scroll to the button to ensure it's not hidden
driver.execute_script("arguments[0].scrollIntoView();", predict_button)
time.sleep(1)  # Short delay to avoid timing issues

# Click the button
predict_button.click()

# Wait for the result
time.sleep(3)

# Capture and print the result
result = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text  # Adjust if necessary
print("Prediction Result:", result)

# Close browser
driver.quit()
