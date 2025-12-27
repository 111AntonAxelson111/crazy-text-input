# crazy-text-input

It works like this:

You start the python program. 
Then it opens a json file in the users computer. 
Here the python program iterates slowly over the keys of the dictionary.
If it has read and there was no valid input then it will write X on that index.
Then it restarts and all inputslots get values:""

To make an valid input you must have USER_SEP at start and end. 
While it is running you can also change the string for separating valid input and the 
time inbetween each read from json file. 

Then when there has been valid input it is displayed by writing that in the json file.
Then it is saved to the clipboard.






