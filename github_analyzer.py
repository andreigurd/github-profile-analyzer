import requests
import os
from datetime import datetime

class GitHub_Analyzer:

    def __init__(self, user_name):
        self.user_name = user_name

    def get_user(self):    
        url = f"https://api.github.com/users/{self.user_name}"

        response = requests.get(url)    

        try:
            # Check if successful
            if response.status_code == 200:
                print("User Status Code:", response.status_code)
            # Get specific data from the JSON
            
                user_data = response.json()       
                print("Name:", user_data.get('name') or "N/A")
                print("Bio:", user_data.get('bio') or "N/A")
                print("Location:", user_data.get('location') or "N/A")
                print("Public Repos:", user_data.get('public_repos', "N/A"))
                # .get(key, default) wont replace 0 with N/A
                    
                    
            elif response.status_code == 404:
                print(f"User '{self.user_name}' not found")
                return None
            else:
                print(f'Error: {response.status_code}')
                return None
            
        except requests.exceptions.ConnectionError:
            print("Network error: Could not connect to the API")
        except requests.exceptions.Timeout:
            print("Request timed out")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")


    #----------------------------------------------------------
    def get_user_repos(self):
        url = f"https://api.github.com/users/{self.user_name}/repos?sort=updated&per_page=5"
        try:
            response = requests.get(url)    
        
            if response.status_code == 200:
                print("User_Repositories Status Code:", response.status_code)
            # Get specific data from the JSON
                user_repo_data = response.json()     
                
            elif response.status_code == 404:
                print(f"Repositories for '{self.user_name}' not found")
                return None        
                
            else:
                print(f'Error: {response.status_code}')
                return None
        
        except requests.exceptions.ConnectionError:
            print("Network error: Could not connect to the API")
        except requests.exceptions.Timeout:
            print("Request timed out")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    #----------------------------------------------------------
    def calculate_stats(self):
        pass

def main():
    github_user = GitHub_Analyzer()

    # ask for user name and run get_user function
    while True:
        user_name = input(f'Enter GitHub username to lookup (or "quit"):\n')

        if user_name.lower() == 'quit':
            break
        elif user_name.lower() == '':
            print("Entry cannot be blank. Please try again.")
        else:
            break

        github_user.view_user_repos(user_name)

if __name__ == "__main__":
    main()



