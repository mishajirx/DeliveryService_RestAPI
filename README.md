# "Sweetness from All Troubles" REST API Service #

Service performs the REST API access to the delivery service app, including
1. Distribution of orders
3. Changing the order statuses
2. Assigning roles of the users 

Moreover, every component workability was checked by the unit tests, contained in the project

## Transferring the Repository Folder to Your Computer ##
1. Click the fork button in the repository https://github.com/mishajirx/YandexBackend
2. Open the command line
3. Navigate to the folder of your choice
4. Enter the command git clone https://github.com/<YourName>/YandexBackend

## Installing Required Software ##
#### To download the necessary libraries, follow these steps: ####
0. Perform all actions listed below in the terminal
1. Navigate to the project directory in the command line
2. Execute pip install -r requirements.txt
#### Example ####
$ pip install -r requirements.txt

## Running the Application ##
To run the application, simply execute in the console
python3 main.py (or sudo python main.py)
#### Example #### 
$ python3 main.py

## Running Tests ##
To run tests, you need to:
1. Repeat the steps from the "Running the Application" section
2. Press ctrl+z. Execute bg
3. Execute pytest-3 test.py -x -s
4. Enter 'y'
#### Example: ####
$ sudo python3 main.py
$ ^Z
& bg
$ pytest-3 test.py -x -s

## Auto Start ##
To make the server start on system boot, enter the following commands in the console:
1. crontab -e
2. In the opened file, type the following in the last line:
   @reboot python3 /path_to_the_project/main.py
