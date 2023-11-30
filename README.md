# What is this?
The file `daySetup.py` is more or less a terminal program for creating the day folder and files


# How to use it?
1. Create a file called `.session_id` and insert the session token from the cookies from the webpage. This is used to download your puzzle input
2. Run the python file with following syntax in the terminal: `python3 daySetup.py <programming_language> [-f] [-d] [-p2] [-nc]`
   `programming langauge` can be `hs`, `py`, `c` and `java`. This decides the template which should be used  
   `-d` is to update the data file if it already exists  
   `-f` replaces the current programming language file with the template (all data may be lost)  
   `-p2` Creates the file for the second part and tries to copy the solution from part1. If the given languages differ it behaves the same as for part1, but the filename contains "part2" 
   `-nc` Do not copy the solution of part1 for the second file
3. Now there should be a folder for the day as well as a file for the solution of part 1
