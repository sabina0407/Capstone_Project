from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Setup Chrome options in headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0")

try:
    driver = webdriver.Chrome(options=options) # Launch Chrome in headless mode 
    driver.get("https://www.baseball-almanac.com/pitching/piwins4.shtml") # Load the webpage 

    # Wait for the table to load 
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    # Extract data from the table 
    rows = table.find_elements(By.TAG_NAME, "tr")
    data = []

    # Loop through each row in the table 
    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, "td") # get all <td> cells in the row 
            if len(cells) == 8:
                al_year = cells[0].text.strip()
                al_player = cells[1].text.strip()
                al_wins = cells[2].text.strip()
                al_wins = int(al_wins) if al_wins.isdigit() else None
                al_team = cells[3].text.strip()

                nl_year = cells[4].text.strip()
                nl_player = cells[5].text.strip()
                nl_wins = cells[6].text.strip()
                nl_wins = int(nl_wins) if nl_wins.isdigit() else None
                nl_team = cells[7].text.strip()

                # Append the data to the list 
                data.append([al_year, al_player, al_wins, al_team, "AL"])
                data.append([nl_year, nl_player, nl_wins, nl_team, "NL"])

        except Exception as e:
            print(f"Error processing row: {e}")

finally:
    driver.quit()

try:
    # Create a DataFrame from the extracted data 
    df = pd.DataFrame(data, columns=["Year", "Player", "Wins", "Team", "League"])

    # save the df to a CSV file
    df.to_csv("leaders_for_wins.csv", index=False)
    print(f"Extracted {len(df)} rows.")
    print("Data saved to leaders_for_wins.csv")
except Exception as e:
    print(f"Error saving data to CSV: {e}")
