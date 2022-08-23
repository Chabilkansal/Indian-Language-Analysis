Please read this before executing the assignment:-

Plugins-
Software: python3(.sh files run python3 files)

Dependencies-
Python Libraries: pandas, numpy, scipy, datetime, collections

Programs-

.sh files:

assign2.sh 
  Top level script that runs the entire assignment

(1) percent-india.sh
  Runs Question1.py python file
  Generates percent-india.csv 

(2) gender-india.sh
  Runs Question2.py python file
  Generates gender-india-a.csv,gender-india-b.csv,gender-india-c.csv

(3) geography-india.sh
  Runs Question3.py python file
  Generates geography-india-a.csv,geography-india-b.csv,geography-india-c.csv

(4) Note: question4 uses percent-india.csv generated in question 1
(4-a) 3-to-2-ratio.sh
  Runs Question4_3-to-2.py python file
  Generates 3-to-2-ratio.csv

(4-b) 2-to-1-ratio.sh
  Runs Question4_2-to-1.py python file
  Generates 2-to-1-ratio.csv

(5) age-india.sh
  Runs Question5.py python file
  Generates age-india.csv

(6) literacy-india.sh
  Runs Question6.py python file
  Generates literacy-india.csv

(7) region-india.sh
  Runs Question7.py python file
  Generates region-india-a.csv, region-india-b.csv

(8) age-gender.sh
  Runs Question8.py python file
  Generates age-gender-a.csv,age-gender-b.csv,age-gender-c.csv

(9) literacy-gender.sh
  Runs Question9.py python file
  Generates literacy-gender-a.csv,literacy-gender-b.csv,literacy-gender-c.csv

How to use:
To run the whole assignment at once run the following command from the terminal-
bash assign2.sh 

To run each code seperately run the following command from the terminal-
bash FILE_NAME.sh
where FILE_NAME is the name of the .sh file you want to run

Output-
All the output files generated are stored in the Results' folder.


Note: In question 2,3 part a -> mono, part b->bi, part c->tri
while In question 8,9 part a -> tri, part b->bi, part c->mono

Some points to keep in mind:

* If any sh file does not execute please change permissions for the file and try again.

* All the python programs and the datasets are provided in the same folder. Python program are named Question1,Question2,Question3, and so on for each question respectively

* Along with all the datasets provided for this assignment.
   
* Please keep all the python programs, the datasets and the CSV files folder within the same directory otherwise, there will be execution errors.

* Please do not use any dataset other than those provided by me as I have removed some Null values from the dataset manually and the programming is done with these datasets in
  consideration.

* As I have done complete assignment on Jupyter Notebook so I have also added a Jupyte notebooks folder in case you want to run code in notebook format. For running them with proper path
  just bring the notebooks out of the Jupyter Notebooks folder to assignment folder.

* I have tried to explain everything in my code using comments, if still in case you face any problem feel free to contact me.

email: chabilk21@iitk.ac.in
phone: 9149040922