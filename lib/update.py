#!/usr/bin/env python3

# Import necessary libraries
import requests
import os
import sys
import zipfile
import json
import platform
import zipfile

# Import ANSI color codes from a custom module
from .ansi_colors import *
# Import Alerts
from .alerts import *

# Function to get the current version of the tool
def get_current_version():
	# Read the current configuration
	with open("config/version.json", "r") as file:
		version = json.load(file)

	# Modify the current version
	current_version = version["current_version"]

	return current_version


# Function to get both current and latest versions of the tool
def get_current_and_latest_version():
	latest_version = ""
	current_version = get_current_version()

	# API endpoint for the latest release on GitHub
	repository = 'https://api.github.com/repos/sAjibuu/Upload_Bypass/releases/latest'

	# Send a GET request to the GitHub API
	response = requests.get(repository)

	# Check if the request was successful (status code 200)
	if response.status_code == 200:
		# Extract the latest version from the JSON response
		latest_version = response.json()['tag_name']

	return current_version, latest_version

def create_delete_script(script_path, tool_directory):
	delete_script_path = os.path.join(script_path, os.pardir, "delete_script.bat")
	temp_delete_script_path = os.path.join(script_path, os.pardir, "temp_delete_script.bat")

	# Create the delete script
	with open(delete_script_path, "w") as delete_script:
		delete_script.write('@echo off\n')
		delete_script.write(f'rmdir /s /q "{tool_directory}"\n')

		# Create a temporary batch script to delete the original batch script
		delete_script.write(f'echo @echo off > "{temp_delete_script_path}"\n')
		delete_script.write(f'echo del "{delete_script_path}" >> "{temp_delete_script_path}"\n')
		delete_script.write(f'timeout 4 >> "{temp_delete_script_path}"\n')  # Delay for about 5 seconds
		delete_script.write(f'echo del "{temp_delete_script_path}" >> "{temp_delete_script_path}"\n')  # Delete temp script itself

		# Execute the temporary batch script
		delete_script.write(f'start cmd /c "{temp_delete_script_path}"\n')
		
	return delete_script_path

# Function to check for updates and perform the update if available
def check_for_updates():
	# API endpoint for the latest release on GitHub
	repository = 'https://api.github.com/repos/sAjibuu/Upload_Bypass/releases/latest'

	# Create a session for making requests
	session = requests.Session()

	# Send a GET request to the GitHub API
	response = session.get(repository)

	# Get the current version of the tool
	current_version = get_current_version()

	# Check if the request was successful (status code 200)
	if response.status_code == 200:
		# Extract the latest version from the JSON response
		latest_version = response.json()['tag_name']

		# Check if the latest version is different from the current version
		if latest_version != current_version:
			print('\nDownloading the latest version...')

			# Get the URL for assets associated with the latest release
			assets_url = response.json()['assets_url']

			# Send a GET request to the assets URL
			assets_response = session.get(assets_url)

			# Check if the request was successful (status code 200)
			if assets_response.status_code == 200:
				assets_json = assets_response.json()
				description = response.json()["body"]

				# Loop through each asset in the assets JSON
				for asset in assets_json:
					if asset['name'].endswith('.zip'):
						asset_url = asset['url']

						# Define headers for the asset request
						headers = {
							"Accept": "application/octet-stream"
						}

						# Get the name of the package
						package_name = asset['name']

						# Send a GET request to download the asset
						asset_response = session.get(asset_url, headers=headers)

						# Check if the request was successful (status code 200)
						if asset_response.status_code == 200:
							# Write the asset content to a file
							with open(asset['name'], 'wb') as f:
								f.write(asset_response.content)

							# Determine the platform
							platform_name = sys.platform

							# Handle Linux platform
							if "linux" in platform_name.lower():
								# Move the downloaded package to /tmp directory
								os.system(f"mv ./{package_name} /tmp/{package_name}")
								# Extract the package contents
								os.system(f"unzip -q /tmp/{package_name} -d /tmp")
								# Sync the extracted files to the current directory
								os.system(f"rsync --force -a /tmp/Upload_Bypass/* ./")
								# Clean up temporary files
								os.system(f"rm -rf /tmp/{package_name}")
								os.system(f"rm -rf /tmp/Upload_Bypass")

								print("Download complete.")
								print(f"\nUpgraded to: {latest_version}")
								print("\nRelease Notes:\n" + description)
								break

							elif "windows" in platform.system().lower():
								
								zip_file_name = package_name
								
								# Open the zip file
								with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
									# Extract all contents to the current folder
									zip_ref.extractall()

								# Close the zip file handle
								zip_ref.close()
								current_script_path = os.getcwd()

								parent_directory = os.path.abspath(os.path.join(current_script_path, os.pardir))
								os.system("move Upload_Bypass Upload_Bypass2")
								os.system("move Upload_Bypass2 ../")

								current_directory = os.getcwd()

								# Create the delete script
								delete_script_path = create_delete_script(current_script_path, current_directory)

								# Execute the delete script using subprocess
								import subprocess

								subprocess.call(delete_script_path, shell=True)
								temp_directory = parent_directory + "\\Upload_Bypass2"
								os.system(f'xcopy "{temp_directory}" "{current_script_path}" /E /H /C /I /Q')
								os.system(f'rmdir /S /Q "{temp_directory}"')

								print("\033c", end="")
								info("Download complete.")
								info(f"Upgraded to: {latest_version}")
								info(f"Upload Bypass is extracted and is available to use")
								info("Release Notes:")
								print("")
								print(description)

								# Terminate the script execution
								sys.exit()


		# If the latest version matches the current version
		else:
			info("You are already running the latest version.")

	# If unable to retrieve the latest version from GitHub
	else:
		error("Failed to retrieve the latest version from Github.")
