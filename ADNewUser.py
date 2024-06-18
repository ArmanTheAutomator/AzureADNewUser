# For complete instructions, please refer to the README file. 

import requests
import json

# Replace with your Azure credentials (consider environment variables)
tenant_id = "your_tenant_id"
client_id = "your_client_id"
client_secret = "your_client_secret"

# Get user input for variables
user_principal_name = input("Please assign the new user's principal name (i.e. new_user@example.com): ")
user_name = input("Please assign the new user's username (i.e. New User): ")
password = input("Please assign a strong temporary password for the new user: ")

# Azure AD Graph API endpoints
user_url = f"https://graph.microsoft.com/v1.0/users"
role_assignment_url = f"https://graph.microsoft.com/v1.0/directoryRoles/{role_id}/members/$ref"

# Function to get an access token
def get_access_token():
  resource = "https://graph.microsoft.com"
  token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
  payload = {
      "grant_type": "client_credentials",
      "client_id": client_id,
      "client_secret": client_secret,
      "scope": f"{resource}/.default"
  }
  headers = {"Content-Type": "application/x-www-form-urlencoded"}
  response = requests.post(token_url, data=payload, headers=headers)
  response.raise_for_status()  # Raise exception for non-200 status codes
  return response.json()["access_token"]

# Create user request body
user_data = {
  "displayName": user_name,
  "userPrincipalName": user_principal_name,
  "passwordProfile": {
    "password": password
  }
}

# Get access token
access_token = get_access_token()

# Set headers with access token
headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

try:
  # Send request to create user
  response = requests.post(user_url, headers=headers, json=user_data)
  response.raise_for_status()  # Raise exception for non-200 status codes
  print(f"User created successfully: {user_principal_name}")

  # Get the user object ID
  user_object_id = response.json()["id"]

  # Replace with the desired role ID (find role IDs in Azure AD)
  role_id = input("Please enter the role ID for the new user.")

  # Assign role to user request body
  assignment_data = {"@odata.id": f"{role_assignment_url}/{user_object_id}"}

  # Send request to assign role
  response = requests.post(role_assignment_url, headers=headers, json=assignment_data)
  response.raise_for_status()  # Raise exception for non-200 status codes
  print(f"Role assigned successfully: {role_id}")
except requests.exceptions.RequestException as e:
  print(f"Error creating user or assigning role: {e}")
