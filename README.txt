The language I am parsing is a subset of the Chinese language, utilizing a limited character set and limited grammar rules. 
The characters are limited to simple subjects, times, places, verbs, and objects. 
For a complete list of recognized characters please see all terminals in the lark grammar within the ChineseParser.py file.
The limited grammar rules allow for sentences of the structure subject + time + place + verb + object, where subject and time
can be switched as is allowed in traditional Chinese grammar. These sentences are broken down into two categories, simple sentences
and "go" sentences. 
A simple sentence involves a subject being at a place performing an action on an object.
A go sentence involves a subject going to a place to perform an action on an object.
Both sentence types must include the aforementioned subject, time, place, verb, and object components. 

Some things to take note of in the grammar: 
The grammar is easily extendable, primarily in the verb, place, and object sections. There are thousands of possible verb + object 
combinations, each of which can be performed at a variety of places, but for the scope of this project I limited these to just a handful. 
It is also important to note that adding a place involves adding a "atplace" and "goplace" instance, as the translation and grammar for
being at a place and performing an action and going to a place to perform an action are quite different in English and Chinese. 

Some things to take note of in the code: 
Formatting a "gosentence" involves more manipulation than a "simplesentence", and so in the tree iteration loop I treated "gosentence" as
a standard case and handled the "simplesentence" case with minimal reworking after the tree iteration. 
I use an array to store the various time aspects and append these to the end of the sentence as this is a simple way to maintain grammatical 
correctness in English across both sentence types. 
I use the tree iteration to properly format sections of the final English string, such as the place and surrounding words (to, the, at, etc.)
as well as to handle capitalization and the use of "o'clock" for time.
Lastly, once the sentence is assembled I use array and string manipulation to capitalize the first word of the sentence, add spacing, and a period.

This code will run on any command line where the "python SCRIPTNAME.py" command will execute, which is supported on MacOS, Linux, and Windows. 
To run the code without any input, type "python ChineseParser.py" in the command line. This will trigger 3 print statements explaining
how to format a valid input for the program. To execute the program and translate a sentence, you must pass in a command line argument consisting
of a single Chinese sentence which contains a subject, time, verb, place, and object with no spaces and valid Chinese grammar. This can be done
by typing "python ChineseParser.py CHINESESENTENCE" where CHINESESENTENCE may also be formatted with quotation marks. 

Example inputs with corresponding outputs can be found in the sample-programs.txt file within the repository. 