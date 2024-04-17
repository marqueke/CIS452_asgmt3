# CIS457_asgmt3

The assignment consists of two programs to run: 
1. ftp_server.py
2. ftp_client.py

The assignment also consists of two example files:
1. sample55.c (in the client directory)
2. test_client.txt (in the server directory)

Open the .py files on two separate terminals. Compile the files on the computer's terminal with command "python3 -m py_compile". Run the ftp_server.py file first with command "python3 ftp_server.py". Run the ftp_client.py file in its respective window with the command "python3 ftp_client.py 127.0.0.1 2121". The ftp_client.py file works as follows:
Typing "LIST" will display the files included in the ftp_server.py directory.
Typing "STORE <filename>" will upload the specified file from the client directory to the server directory.
  In this context, the file "sample55.c" was used as the specified file.
Typing "RECEIVE <filename>" will download the specified file from the server directory into the client directory.
  In this context, the file "test_client.txt" was used as the specified file.
Typing "QUIT" will terminate the client socket and program and the server will terminate its connection and wait for the next connection.
