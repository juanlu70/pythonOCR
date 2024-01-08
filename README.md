# pythonOCR

A program to scan an image and find a solution for the recognized test.


# REASON

This program was done for passing LinkEdin exams, the reason is that I hate all kind of tests and exams, so I invented
a way to surpass it using my logic thinking that equals the logic thinking that you have to employ for pass the exam. 

Someone could think that this is a way to make a way of cheating, but the effort I put on this and the things I learned 
making it are equivalent to the tedious study to pass the exams and including with study always there are a question 
that could be specially difficult or confusing.

Then multiply this for the big number of exams LinkEdin has, and then you are able with some luck to surpass a little
number of them despite your skills and experience.

I made this thinking in other kind of exams too, not only LinkEdin.

So I made a system to surpass most of the exams as possible by technical means and my own tests demonstrate that it 
works, and it is possible to surpass a lot of exams with this tool, maybe not all.


# MORE REASONS

Why exams are not a good way to test skills?

Because many of us, the developers, have to memorize so big bunch of functions, methods, or operations in different
languages and frameworks, and tools that we didn't memorize anything at all, it is not productive, so the success of 
webs like stackoverflow.com, and most recently the use of IA as an online manual always available to find fast results, 
we focus on the program flow, the object architecture that we are building, this is most important in a program 
because it has to be scalable and easy to modify in the long term future.

Tests and exams has nothing to do with the long term, all are focused on how good are you on the very short term,
how fast you think and how much volumes of information you can memorize, developer jobs are not the same way as other 
jobs when you are asked about your demonstrable experience, as developers they demand from us more than our CV says, 
whatever it is good and adequate for the job or not, I think these tests don't reflect the real developer work and 
don't demonstrate that a developer that pass it will make the work better than others.

I know that sometimes there are different developers that are good for a same certain job position, any way the fast on
the short term is prevalent over the others.

Also, making this project I made my first OCR based program, I learned about event development in python and introduced
myself in the world of LLMs, my first tought was to use ChatGPT API or Bard API, but the first it is not free and the
second still not available at the time I was making this program, so finally I learned about Llamafile, LlamaCPP and
all the rest of models and frameworks to work with LLMs.

Also, I learned a little about image manipulation with PIL library and numpy.


# THE FINAL AND DEFINITIVE REASON

This project is the main demonstration of how long term thinking could beat any form of short term thinking test or 
exam.


# INSTALLATION

This is a Python program, so its installation follow the normal path of any python program, except one step that is
done with the LLM installation and the recomended LLM model.

You have to install the requirements provided:

```
pip3 install -r requirements.txt
```

Then you install the LLM python program, and then you need to install the mistral-7b-openorca model (that is the
recommended model at the time this program was done, in the future could be others) so to access mistral-7b-openorca you
need first to install the gpt4all model:

You can see the models you have installed locally on your machine in LLM with this command:
```
llm models
```

If you don't see the mistral-7b-openorca you have to install previously the gtp4all model:

```
llm install gpt4all
```

Then install the mistral-7b-openorca:

```
llm install mistral-7b-openorca
```

And it is recommended to set the mistral-7b-openorca model as default:

```
llm models default mistral-7b-openorca
```

then you can test is the model is the default:

```
llm chat
```

You can see something like this:

```
Chatting with mistral-7b-openorca
Type 'exit' or 'quit' to exit
Type '!multi' to enter multiple lines, then '!end' to finish
```

So you can begin to use the mistral-7b-openorca model by default.


# HOW THE PROGRAM WORKS

This program is intended to get a screen capture in a certain directory of your own, then the program waits for a new
file creation in that directory and when a new file (capture) is created in the directory, it applies the OCR, then
looks for a solution (if provided) and then uses the IA model to answer the question.

The image captured is processed to increase the contrast, it detects automatically if an image is prominently light 
or dark, if dark then inverts the image to ease the OCR process over the image, hovewer the OCR process it is never
perfect.

Ideally the image captured is the question with the answers, but I made it to be able to analyze all the screen for
saving capture time, at least with LinkEdin exams.

It is recommended to use the browser maximized and to disable bookmarks tab when making the captures, the less garbage
scanned it offer better OCR results, also a light image will work better than a dark image despite the program will 
detect light and invert the image if dark.

There is a trash_text.txt that is a list of strings that will remove the lines containing it, this is made to remove
any kind of spam or unwanted text for sending it to the LLM.

WARNING: If you are not using a system program to make the capture sometimes the program could store the capture in a
cloud, and then you have to donwload the image, try to use a temp directory to download the image and then copy to the
main directory where the program expects the capture files, if not the temporary file used for the download will be 
sent to the OCR.

WARNING: The program tries to isolate question and answers, and try to apply a number to each answer to help to get 
better results with the LLM, obviously not always can enumerate the answers or sometimes partially.


# ARGUMENTS

You can get help with the -h flag in command-line.

The -i or --image flags refers to an image to test an image already done, also you must use this flag with the 
destination directory where the captures will be stored.

The -s or --solution flags refers to the file with the solutions, it is made for README.md files with the solutions
inside, the solution it is found using a similar_text technique but sometimes could fail.

The -v or --verbose flags are to show all the information about the process.


# TO DO

Still working on making tests, maybe I will add a Dockerfile, but this is designed as a tool, something you can use 
at any time and not depending on a server.
