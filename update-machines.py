#!/usr/bin/env python3
"""Update Machine/App Server pairs in ESM.
Depends on `inventory/machines-ENV.json`
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

__author__ = "James Shawn Carnley"
__copyright__ = "Copyright 2024"
__credits__ = ["James Shawn Carnley"]
__license__ = "GPL"
__version__ = "1.0.0"
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
with open('inventory/machines-' + env_name.upper() +'.json', 'r') as file:
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

    # Update Machine
    driver.get(config['esm_host'] + config['esm_env_form'] + machine['esm_env'])
    machine_link = wait.until(EC.presence_of_element_located((By.XPATH, config['esm_machines_xpath'])))
    machine_link.click()
    wait = WebDriverWait(driver, 10)
    action_link = wait.until(EC.presence_of_element_located((By.XPATH, "//td[text()='" + machine['name'] + config['esm_machine_suffix'] + "']")))
    action_parent = action_link.find_element(By.XPATH, "..")
    action_parent.click()
    private_ip = wait.until(EC.presence_of_element_located((By.ID, config['esm_ip_field'])))
    private_ip.clear()
    private_ip.send_keys(machine['private_ip'])
    agent_name = wait.until(EC.presence_of_element_located((By.ID, config['esm_agent_field'])))
    agent_name.clear()
    agent_name.send_keys(machine['name'].upper() + config['esm_deploy_agent_suffix'])
    bash_shell = wait.until(EC.presence_of_element_located((By.ID, config['esm_shell_field'])))
    bash_shell.clear()
    bash_shell.send_keys(config['esm_bash_path'])
    public_name = wait.until(EC.presence_of_element_located((By.ID, config['esm_public_host_field'])))
    public_name.clear()
    public_name.send_keys(machine['public_hostname'])
    public_ip = wait.until(EC.presence_of_element_located((By.ID, config['esm_public_ip_field'])))
    public_ip.clear()
    public_ip.send_keys(machine['public_ip'])
    b8_help = wait.until(EC.presence_of_element_located((By.ID, config['esm_machine_b8_help_field'])))
    b8_help.clear()
    b8_help.send_keys(machine['esm_b8_help_path'])
    b9_help = wait.until(EC.presence_of_element_located((By.ID, config['esm_machine_b9_help_field'])))
    b9_help.clear()
    b9_help.send_keys(machine['esm_b9_help_path'])
    b9_war = wait.until(EC.presence_of_element_located((By.ID, config['esm_machine_b9_war_field'])))
    b9_war.clear()
    b9_war.send_keys(machine['esm_b9_war_path'])
    save_button = wait.until(EC.presence_of_element_located((By.XPATH, config['esm_save_machine_button_xpath'])))
    save_button.click()

    # Update App Server
    driver.get(config['esm_host'] + config['esm_env_form'] + machine['esm_env'])
    server_link = wait.until(EC.presence_of_element_located((By.XPATH, config['esm_appserver_xpath'])))
    server_link.click()
    # wait = WebDriverWait(driver, 30)
    action_link = wait.until(EC.presence_of_element_located((By.XPATH, "//td[contains(text(), '" + machine['name'] + "')]")))
    action_parent = action_link.find_element(By.XPATH, "..")
    action_parent.click()
    machine_select =  wait.until(EC.presence_of_element_located((By.TAG_NAME,'select')))
    machine_options = machine_select.find_elements(By.TAG_NAME, 'option')
    for option in machine_options:
        if machine['name'].lower() in option.text.lower():
            option.click()
            break
    ssl_checkbox = driver.find_element(By.ID, config['esm_server_ssl_field'])
    if not ssl_checkbox.is_selected():
        ssl_checkbox.click()
    webapp_path = wait.until(EC.presence_of_element_located((By.ID, config['esm_webapps_path_field'])))
    webapp_path.clear()
    webapp_path.send_keys(config['esm_webapps_path'])
    if machine['esm_admin_api_app_data_path']:
        webapp_path = wait.until(EC.presence_of_element_located((By.ID, config['esm_admin_api_app_data_path_field'])))
        webapp_path.clear()
        webapp_path.send_keys(machine['esm_admin_api_app_data_path'])
    save_button = wait.until(EC.presence_of_element_located((By.XPATH, config['esm_server_save_button_xpath'])))
    save_button.click()

# Close the browser
driver.quit()
