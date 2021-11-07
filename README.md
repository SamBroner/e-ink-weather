# E-Ink Weather & News

## Getting started

1. sudo python3 setup.py install
1. Add API secrets to .env file (instructions below)
1. python3 start.py


To refresh the screen, you'll need to add the python script to a cron job.

To access the cron file run the following
```sh
crontab -e 
```

Prepend a line like the below to the cron file. There are better guides to creating cronfiles, but this 
line runs the start script with python 3 every 15 minutes.
```
*/15 * * * * /usr/bin/python3 /home/pi/code/e-ink-weather/start.py
```


## Physical Dependencies (Stuff you need to buy)
* Raspberry Pi
* Waveshare e-ink display

## .env

Rename ```.env.template``` to ```.env```

**Remove** the debug flag from .env to trigger the e-ink display.

## TODO

Clean up log file

## Notes

* Because we use the waveshare library, waveshare files are included in lib. This is also why lib is not in the .gitignore.

* We only include the 5.83" dependencies...

* Update... this works