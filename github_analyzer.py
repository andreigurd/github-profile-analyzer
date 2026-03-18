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
        url = f"https://api.github.com/users/{self.user_name}/repos?per_page=100"
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
        
        #------------ Total stars across all repos

        stars_count = {}
        for star_item in self.user_repo_data[:5]:            
            if stars_count:
                stars_count += star_item.get('stargazers_count')
            else:
                stars_count = star_item.get('stargazers_count')

        #------------ Most popular repository
        most_stars = []
        for star_item in self.user_repo_data[:5]:
            if not most_stars:
                most_stars = star_item
            elif star_item.get('stargazers_count') > most_stars.get('stargazers_count'):
                    most_stars = star_item

        #------------ Primary language (most repos in that language)

        languages_used = []
        for lang_item in self.user_repo_data[:5]:            
            if lang_item['language']:
                languages_used.append(lang_item['language']) 

        # Counter and .most(n) returns a list of tuples of element and count in descending order. (n) argument for how many tuples are returned.
        primary_language = Counter(languages_used).most(1)           

        #------------ Total forks across all repos

        forks_count = {}
        for fork_item in self.user_repo_data[:5]:            
            if forks_count:
                forks_count += fork_item.get('forks_count')
            else:
                forks_count = fork_item.get('forks_count')

    #----------------------------------------------------------
    def display_stats(self):
        stats = self.calculate_stats()
        # tabulate may be overcomplicated. just print single f' rows

        """Display complete repo stats dashboard"""
        print(f"\n{'='*60}")
        print(f"GitHub Profile Dashboard for: {self.user_name}")
        print(f"{'='*60}\n")

        print(f"Total Stars: {stats.stars_count}\n")
        print(f"Most Popular Repository: {stats.most_stars["name"]}\n")
        print(f"Primary Language Used: {stats.primary_language[0][0]}\n")
        # primary_language is counter result of tuples of language and count. want to display language name.

#----------------------------------------------------------
def main():
    dashboard = GitHub_Analyzer()

    # ask for user name and run get_user function
    while True:
        user_name = input(f'Enter GitHub username to lookup (or "quit"):\n')

        if user_name.lower() == 'quit':
            break
        elif user_name.lower() == '':
            print("Entry cannot be blank. Please try again.")
        else:
            break

        dashboard.get_user(user_name)
        dashboard.get_user_repos(user_name)
        # run  dashboard.calculate_stats(user_name) inside of display_stats
        dashboard.display_stats(user_name)

if __name__ == "__main__":
    main()



