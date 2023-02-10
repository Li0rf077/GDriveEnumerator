# GDriveEnumerator
This program is used to monitor a user's Google Drive, look for publically visible files and make them private.

# Requirements
At first execution, the script will redirect to a google authorization page to allow the needed access scope for the program to run properly. Later on the program will save the generated token to allow continous execution. 
The scope used - 'https://www.googleapis.com/auth/drive'

# Known Issues
1. The authorization app used is not yet verified, and the following page will occur:
<img width="509" alt="image" src="https://user-images.githubusercontent.com/87004055/218041386-56ff5112-f88f-4dd5-b8b2-2c2b2270ec21.png">
2. If the given file name is not in english - an error might occure and the visibility of the file will not change. Example output below.

# Example Output
![image](https://user-images.githubusercontent.com/87004055/218041638-de0a6d0b-cac2-403d-922d-4c19d7d597f8.png)
