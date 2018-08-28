# Button recorder

Run a custom python script on a Google Voice Kit (Raspberry Pi) to play and record silly sounds, using the [Button Basher](https://github.com/orangespaceman/button-basher)


## Usage

Once this is set up, you can play sound effects by hitting any button on the board

You can record new sounds by pressing the button on the Voice Kit, and then assign them to a button on the board

![Button Recorder](assets/button-recorder.jpg)


## Installation

* Set up a Google Voice Kit with a Raspberry Pi, following the [online instructions](https://aiyprojects.withgoogle.com/voice)

* Create a button board (or similar) following [these instructions](https://github.com/orangespaceman/button-basher)

* Install `xbindkeys` and `mpg321` onto the Pi:

  ```
  sudo apt-get install xbindkeys mpg321
  ```

* Clone this repo onto the Pi into the directory:

  ```
  /home/pi/AIY-voice-kit-python/
  ```

* From this directory, start the virtualenv:

  ```
  source env/bin/activate
  ```

* Move into the cloned directory

  ```
  cd button-recorder/
  ```

* Copy (or link) the xbindkeysrc file to `~/.xbindkeysrc`

  ```
  ln -s ~/AIY-voice-kit-python/button-recorder/xbindkeysrc ~/.xbindkeysrc
  ```

  (Note that you will have to restart the machine for this to take effect)

* Install the requirements:

  ```
  pip install -r requirements.txt
  ```

* Ensure the script works by running it manually:

  ```
  DISPLAY=":0" /home/pi/AIY-voice-kit-python/env/bin/python3 -u /home/pi/AIY-voice-kit-python/button-recorder/record.py
  ```

* Set up the script to start when you power up the Pi:

  ```
  sudo cp button-recorder.service /lib/systemd/system/
  sudo systemctl enable button-recorder.service
  ```

* To manually start/stop this service, run:

  ```
  sudo service button-recorder start
  sudo service button-recorder stop
  sudo service button-recorder status
  ```
