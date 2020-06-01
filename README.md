# lolBank

I exported CSV files from my bank account but they got all the same name + (1), so i don't know which one is which month.
I also have exported some month twice, so i have duplicates. Those CSV exports are also full of rows with "garbage".
What you gonna do?
Just writing a "small" program for it and go feature creepin.
When I implemented the "min money" search I was realising I should had made an sqlite importer or something like that...
Anyway its a nice sample program (mostly of how to NOT do some things), maybe useful for someone as example orr even to use.

## how-to

* place your CSV files in **bank_exports** or set the **path** in **config_ini**
* copy settings from **config_default.ini** to **config_ini** and set them according to your needs

cd into this directory and run:
```shell script
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 search.py
```

## features

* full text search
* search for 
* nice terminal output
* will make you probably really sad
