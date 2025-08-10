import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def human_like_typing(element, text):
    """Type text with random delays to mimic human behavior"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))  # Random delay between keystrokes


def main():
    # Set up Chrome options to avoid detection
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    # Initialize variables
    count = 20
    max_comments = 5  # Limit number of comments to avoid spam detection

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    driver.get("https://www.facebook.com/login")
    time.sleep(random.uniform(2, 4))

    try:
        # Login process
        m_mail = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        m_pass = driver.find_element(By.CSS_SELECTOR, "input[name='pass']")
        login = driver.find_element(By.CSS_SELECTOR, "button[name='login']")

        # Enter credentials with human-like behavior
        m_mail.click()
        time.sleep(random.uniform(0.5, 1))Navigate to the post
        human_like_typing(m_mail, "?")  # Replace ? with your fb account email/phone no

        time.sleep(random.uniform(1, 2))
        m_pass.click()
        time.sleep(random.uniform(0.5, 1))
        human_like_typing(m_pass, "?")  # Add your password here

        time.sleep(random.uniform(1, 2))
        login.click()

        # Wait for login to complete (reduced from 120)
        print("Logging in...")
        time.sleep(30)

        # Below is the link to the post where you want to auto-comment.
        driver.get(
            "https://www.facebook.com/story.php?story_fbid=711687591679708&id=100085154203996&_rdr"
        )
        time.sleep(random.uniform(5, 8))

        # Scroll to comment section
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(random.uniform(2, 3))

        # Comment loop with limit
        comments_posted = 0
        while comments_posted < max_comments:
            try:
                # Try multiple selectors for the comment box
                comment_selectors = [
                    "div[aria-label='Write a comment…']",
                    "div[contenteditable='true'][role='textbox']",
                    "div.notranslate[contenteditable='true']",
                    "div[data-lexical-editor='true']",
                ]

                comment_input = None
                for selector in comment_selectors:
                    try:
                        comment_input = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        print(f"Found comment box with selector: {selector}")
                        break
                    except:
                        continue

                if comment_input:
                    # Click on the comment box
                    comment_input.click()
                    time.sleep(random.uniform(1, 2))

                    # Clear any existing text
                    comment_input.send_keys(Keys.CONTROL + "a")
                    comment_input.send_keys(Keys.DELETE)
                    time.sleep(random.uniform(0.5, 2))

                    # Type the comment with human-like speed
                    comment = f"Mim kacchi cai ({count})"
                    human_like_typing(comment_input, comment)
                    time.sleep(random.uniform(2, 5))

                    # Submit the comment
                    comment_input.send_keys(Keys.RETURN)
                    print(f"{count} no Comment posted successfully!")
                    count += 1
                    comments_posted += 1

                    # Wait between comments (important to avoid detection)
                    wait_time = random.uniform(
                        30, 60
                    )  # Wait 30-60 seconds between comments
                    print(f"Waiting {wait_time:.0f} seconds before next comment...")
                    time.sleep(wait_time)

                    # Occasionally scroll the page (human behavior)
                    if random.random() > 0.5:
                        scroll_amount = random.randint(100, 300)
                        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                        time.sleep(random.uniform(1, 2))
                        driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")

                else:
                    print("Could not find comment box")
                    break

            except Exception as e:
                print(f"Error in comment loop: {e}")
                # If blocked, wait longer before trying again
                print("Might be rate limited. Waiting 5 minutes...")
                time.sleep(300)  # Wait 5 minutes

        print(f"Completed posting {comments_posted} comments")

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")
        print("Screenshot saved as error_screenshot.png")

    finally:
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    main()
