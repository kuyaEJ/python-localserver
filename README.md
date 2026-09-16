# Custom Web Server Project

## Introduction
This project is a custom web server that doesn't use any frameworks outside of `Python` with it's built in libraries/tools. There is some `HTML` and `SQL` added to this project too. (Later I plan to add other tools to this project and I plan to expand it with frameworks too)

## Background Information

I did this so I could understand frameworks better and know how they make development of projects easier.

This was meant to be a practice project to strengthen my foundations and understanding of Web Development concepts from college studies that I wasn't confident in. 

I did this in order to learn how complicated projects work from a low-level.

I felt some concepts I learned weren't solidied due to intense curriculum and not enough practice.

I felt I could make a project that uses a database and use tools/libraries, but I didn't know why things actually worked that way or wasn't fully confident I could explain the way it worked.

This is why I decided to do a lower level simpler project I made on my own that helps me increase my confidence articulating and explaining projects, requirements, frameworks, apis, and more.

## Requirements
- Python 3.9.6 or later
- (OPTIONAL) Environment variable or alias commands for python command shortcuts

## Project Libraries/Tools
All tools and libraries in this project do not require any installing. The project should run perfectly fine since it uses the built-in Python libraries and tools
- http.server
- os
- threading
- socketserver
- urllib

If you have the following:
- A *python installation of version 3.9.6 or older* that comes *pre-installed* with your system
- The requests library
- And have a urllib version earlier than 1.26.x (e.g: 1.27.x or higher 2.x) 

> You may need to downgrade your urllib library since it autoinstalls a higher version. To do this run these commands to create a virtualenv that downgrades your urllib library and updates your dependencies

```python
python3 -m venv .venv
```

```python
python3 -m pip install -r requirements.txt --force-reinstall
```

## How to use
It is always recommended to use a virtual environment when running any projects since each project has different library versions or python installation requirements.

Additionally, you should never trust code you didn't make so creating/using a VirtualBox of your OS with the files already on it will help to determine if the project has any malicious code.

> Note: You do not need to install requirements.txt
1. Run the code:
```python
python3 server.py
```
Now the web server should be running. 

2. To test if it is working and being displayed properly, open any browser and in the URL type:
```
localhost:4040
```
You should see a "Hello World" message and the project should be working like a website does.

The supported routes and paths being used in this project are:
- localhost:4040
- localhost:4040/help
- localhost:4040/links
- localhost:4040/signup
- localhost:4040/login

Any other routes and paths will show `404 Not Found`

Enjoy! Feel free to use the code to learn or add things in

## Results
Later add images and gifs of project here