#!/usr/bin/env python3

# Import necessary libraries
import requests
import os
import sys
import zipfile
import json

# Import ANSI color codes from a custom module
from .ansi_colors import *


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
            print('Downloading the latest version...')

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
                                print(f"Upgraded to: {latest_version}")
                                print("Release Notes:\n" + description)
                                break

                            # Handle Windows platform
                            elif "win" in platform_name.lower():
                                # Extract the downloaded zip file
                                with zipfile.ZipFile(package_name, 'r') as zip_ref:
                                    zip_ref.extractall()

                                print("Download complete.")
                                print(f"{package_name} downloaded and extracted in your current directory!")
                                # Delete the downloaded zip file
                                os.system(f"del {package_name}")
                                print("\nRelease Notes:\n" + description)

                                # Terminate the script execution
                                sys.exit()

        # If the latest version matches the current version
        else:
            print(f'\n{green}[+] The tool is up to date!{reset}')

    # If unable to retrieve the latest version from GitHub
    else:
        print(f'{red}[-] Failed to retrieve the latest version from Github.{reset}')
