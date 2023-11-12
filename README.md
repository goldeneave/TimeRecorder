# TimeRecorder

## Description
Timekeeper is a Python software that allows users to start a timer from a specified time and record time intervals in seconds. It also supports time acceleration from a specified position. The primary purpose of this software is to assist in video editing by recording the desired segments for clipping and generating a CSV file containing the recorded information.

Please note that the current version of Timekeeper is incomplete as there are issues with the time acceleration calculation logic.

## Features
- Start a timer from a specified time
- Record time intervals in seconds
- Support time acceleration from a specified position
- Generate a CSV file containing the recorded information

## Installation
1. Clone the repository from GitHub:
```
git clone https://github.com/goldeneave/TimeRecorder.git
```

## Usage
1. Open the terminal and navigate to the project directory.
2. Run the following command to start the Timekeeper software:
```
python window.py
```
3. Once you want use custom time start point, you should first fill the blank in the UI, and then press the Enter key, after you see the infos on the console, you have set it.
4. If you also want set a record speed, you just fill the blank, no need to press Enter.

## Known Issues
- Time acceleration calculation logic is incorrect.
- Each time you run the software, the csv file generated last time will be rewrite, so move it to another path after use.
- Except time acceleration calculation, if you just want calculate the 1* speed I think the software works well.

## Content write for me

Although it is an unfinish project, I still upload it and make a repo for it, it is my first time try to write a GUI, it is unfinished because of many reason, if someone someday get into the repo by accident, and you have enough time and ability, please help me
finish the project. If you are a Chinses speaker or Chinses user, I also prepare a ppt for more detail informations, though it may not prepare for the Github at first.

It is the second time write the README file, I return the last page by mistake, so that' s all I want write, and I will attach an UI image below, thanks!

## UI Screenshot
![UI_SCREENSHOT_IMAGE](https://github.com/goldeneave/TimeRecorder/blob/main/ui_screenshot.png)

