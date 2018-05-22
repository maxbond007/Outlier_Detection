University Project by Bondarenko M. 18.05.2018

///////////////////////////////////////////////////////////////////////
	
It is implemented algorithm of detection, 
consists of several parts: import of data from information system, preprocessing and 
transformation of imported data records with variables of different data types 
into numerical vectors, using well known statistical methods for detection outliers 
and evaluation of the quality and accuracy of the algorithm. 
The result of creating the algorithm is vector of parameters containing anomalies, 
which has to make the work of data manager easier. 
This algorithm is designed for extension the palette 
of information system functions (CLADE-IS) on automatic monitoring the quality of data 
by detecting anomalous records. 

///////////////////////////////////////////////////////////////////////


Description of the files in my project

Data.csv
	This is the data received at the output from the SQL_import.py

main.py
	The main file which run the algorithm.

 SQL_import.py
	This is the sql import of data from database.

transform.py
	There are additional function for SQL_import.py.

generator_anomalies.py
	This file is responsible for generate anomalies in data.

detection.py
	It is the main algorithm for detection of outliers in data.
