O pip precisa ser atual

para instalar

Make sure you have python 3.11.6 or lower

If you have a GPU (unlike me) then change the code line `results = model(frame, device='cpu', classes=0, conf=0.8)` to `results = model(frame, device=0, classes=0, conf=0.8)`

The video must be in MP4 format

# YOLOv8 Face and Person, Tracking and bluring

This project is a simple usage of the YOLOv8 from Ultralytics.

## Features

- Track face
- Track People
- Blur face
- Count total of people and faces in the video
- Save an output video

## Pre-Requirements
Before running the project, make sure you have the following:

- [Python 3.11.6](https://www.python.org/downloads/) installed on your system
   - Specially with python3.11 [venv](https://docs.python.org/3/library/venv.html) 
- [Git](https://git-scm.com/downloads) installed (for cloning the repository)

## Installation

1. Clone the repository
   ```
   git clone git@github.com:pauloDiego-sudo/Management-API.git
   ```
2. Go to the project directory
3. Create a python virtual enviroment (venv):
   ```
   python -m venv env
   ```
4. Activate the enviroment using the scripts:   
   For example on Windows cmd:
   ```
   .\env\Scripts\activate.bat
   ```
   For Linux
   ```
   source \env\bin\activate
   ```
6. Install the dependencies using pip:
   ```
   pip install -r requirements.txt
   ```
7. Run the app:
   ```
   python yolo.py
   ```

## Usage
Everytime you run the application, it must be in the enviroment previously created.

Put the video at the same folder as this aplication, then in the code `yolo.py` change the `video_path` variable with your video name or path.

Run the aplication by calling 

```
python yolo.py
```
You will be able to the tracking in real time, and in the output file called "output.mp4"
## Samples

The code is considering the file `samples/video2.mp4` as the default video. It can be changed as mentioned above at the "Usage" section.

Here an example how the video would turn out:

![]()

## License

This project is licensed under the terms of the MIT license.