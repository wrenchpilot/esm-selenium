#!/usr/bin/env python3
"""Deletes Machine/App Server pairs in ESM.
Depends on `inventory/machines-delete-ENV.json`
"""
import importlib.metadata, subprocess, sys

required  = {'selenium'}
installed = {pkg.metadata['Name'] for pkg in importlib.metadata.distributions()}
missing   = required - installed

if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

import json
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

__author__ = "James Shawn Carnley"
__copyright__ = "Copyright 2024"
__credits__ = ["James Shawn Carnley"]
__license__ = "GPL"
__version__ = "3.0.0"
__maintainer__ = "James Shawn Carnley"
__email__ = "shawn.carnley@gatech.edu"
__status__ = "Production"

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process environment name.')

# Add an argument for the environment name
parser.add_argument('--env', required=True, help='The environment name (BDEVL,BTEST,BTESM,BPROD)')

# Parse the arguments
args = parser.parse_args()

# Use the environment name
env_name = args.env

# Load Config
with open('config.json', 'r') as file:
    config = json.load(file)

# Load credentials
with open('.credentials.json', 'r') as file:
    credentials = json.load(file)

# Load machines
with open('inventory/machines-delete-' + env_name.upper() +'.json', 'r') as file:
    machines = json.load(file)

# Set up the Selenium WebDriver (e.g., for Chrome)
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Open the login page
driver.get(config['esm_host'] + config['esm_login_form'])

# Wait for the page to load
wait = WebDriverWait(driver, 100)

# Locate and fill in the login form
username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
password_field = driver.find_element(By.NAME, "password")
login_button = driver.find_element(By.ID, "submit")

# Enter login credentials
username_field.send_keys(credentials['username'])
password_field.send_keys(credentials['password'])
login_button.click()

# Wait for the page to load
wait = WebDriverWait(driver, 100)

for machine in machines["machine"]:
    # Delete App Server
    driver.get(config['esm_host'] + config['esm_env_form'] + env_name)
    server_link = wait.until(EC.presence_of_element_located((By.XPATH, config['esm_appserver_xpath'])))
    server_link.click()
    wait = WebDriverWait(driver, 10)
    try:
        action_link = wait.until(EC.presence_of_element_located((By.XPATH, "//td[contains(text(),'" + machine['name'] + "')]")))
        action_parent = action_link.find_element(By.XPATH, "..")
        action_parent.click()
        remove_server_prompt = wait.until(EC.presence_of_element_located((By.XPATH, config['esm_remove_server_prompt_button_xpath'])))
        remove_server_prompt.click()
        remove_server = wait.until(EC.presence_of_element_located((By.XPATH, config['esm_remove_server_button_xpath'])))
        remove_server.click()
    except TimeoutException:
        # Skip if the element is not found within the specified timeout
        print(f"Element containing text '{machine['name']}' not found. Skipping...")


    # Delete Machine
    driver.get(config['esm_host'] + config['esm_env_form'] + env_name)
    server_link = wait.until(EC.presence_of_element_located((By.XPATH, config['esm_machines_xpath'])))
    server_link.click()
    wait = WebDriverWait(driver, 10)
    try:
        action_link = wait.until(EC.presence_of_element_located((By.XPATH, "//td[contains(text(),'" + machine['name'] + "')]")))
        action_parent = action_link.find_element(By.XPATH, "..")
        action_parent.click()
        remove_machine_prompt = wait.until(EC.presence_of_element_located((By.XPATH, config['esm_remove_machine_prompt_button_xpath'])))
        remove_machine_prompt.click()
        remove_machine = wait.until(EC.presence_of_element_located((By.XPATH, config['esm_remove_machine_button_xpath'])))
        remove_machine.click()
    except TimeoutException:
        # Skip if the element is not found within the specified timeout
        print(f"Element containing text '{machine['name']}' not found. Skipping...")


# Close the browser
driver.quit()
