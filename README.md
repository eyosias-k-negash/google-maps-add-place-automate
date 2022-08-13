# Automating Place entry on Google Maps

1. run `pip install -r requirements.txt` to install all dependencies.
2. Create a firefox profile with a google logedin session
- Open your regular firefox. Make sure your firefox is up-to-date.
- create a folder next to the script called `firefox_selenium_profile`
- Navigate to about:profiles
- click on `Create a New Profile` 
- Read and click `Next` 
- Enter profile name something distinct
- Click `Choose Folder...` 
- Navigate to folder you created earlier
- Click `Finish`
- Find the profile you created using the name and click `Launch profile in new browser`
- In the new window nativate to https://account.google.com/login
- login to the google account that will be used to place the locations
- after logging in close that window
3. create a csv of the places to add on google map in the following format
`Name,latituide,longituide,address`
- Header is not necessary as long as they are places in the right order
- If you include header make sure the first column is spelled `Name` exactly.
- If the address does not compute in google maps that entry will fail
	- If you are not sure of the address of the place make sure you skip it. 
	- The script will use google's plus code instead.
- Save the file next to script under the name `places.csv`
4. run python place_atms.py

## Note
- This code might need some hand holding.
- In the script output(log along) 
	- It is perfectly fine if it retries to place the same entry again and again.
	- But if it is stuck on a certain entry , say it is on trial 20 or higher follow the visual browser and see where it gives up working and restarts.
	- The script will move on to another entry if it fails to place it in the 50th trial.
