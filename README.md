# Ellucian Solution Manager (ESM) Automator

## About

ESM has no API. Use [Selenium](https://www.selenium.dev/) library to automate tasks.

## Setup

* Using VS Code: setup a `.venv` [Python Virtual Environment](https://code.visualstudio.com/docs/python/environments#_using-the-create-environment-command) and  activate the environmentselect this repo's `requirements.txt`
* Environment setup:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

  * To Deactivate environment

     ```bash
     deactivate
     ```

* Copy `.credentials.example.json` to `.credentials.json` and edit to add your ESM credentials
* Edit `config.json` and set 
  * `esm_host` ( e.g. `http://your_school_esm.edu:PORT` )
  * `esm_webapps_path` ( e.g. `/opt/tomcat/webapps` )
  * `esm_machine_suffix` ( e.g. `.subdomain.your_school_esm.edu` )
  * `esm_deploy_agent_suffix` ( e.g. `_BMUI_AGENT` )
* Edit `machines-ENV.json` inventory (ENV = BDEVL, BTEST, BTESM, BPROD)
* Edit `machines-delete-ENV.json` inventory (ENV = BDEVL, BTEST, BTESM, BPROD)

## Usage

* Create Machines

   ```bash
   ./create-machines.py --env ENV
   ```

* Delete Machines

  ```bash
  ./delete-machines.py --env ENV
  ```

* Update Machines

  ```bash
  ./update-machines.py --env ENV
  ```

* Inventory Formats
  * **Deletion**

   ```json
   {
      "machine": [
         {
               "name": ""
         },
         {
               "name": ""
         },
         ...
      ]
   }
   ```

  * **Create/Update**

   ```json
   {
      "machine": [
         {
               "name": "HOSTNAME_BMUI_AGENT",
               "private_ip": "",
               "public_ip": "",
               "public_hostname": "",
               "esm_env": "",
               "esm_b8_help_path": "/your/banner/path/B8help",
               "esm_b9_help_path": "/your/banner/path/B9help",
               "esm_b9_war_path": "/your/banner/path/XE_staging"
         },
         ...
      ]
   }
   ```
