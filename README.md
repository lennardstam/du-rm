# DU-RM Script

This script runs find, du and rm to remove files.
Results are sorted on disk usage from a given path.

It can be run in cron jobs, but its main purpose is to manually walk trough the files to decide what to remove.

This script is only supported on Linux. It requires at least python3.7.

## How to use

* Clone this repository via git.
* The `rm` command is commented out with an # for safety reason. Flip the # from line 9,and add it on line 10 in durm.py
* Run the script via `python3 durm.py {path} --options`.

## Features

* Shows the size of the files.
* Can run interactive to skip file deletion
* Can run check mode to see quick results without deletion
* Can run force mode for example cronjobs 
* Can search only results with modification date > then given days (default disabled)
* Set the limit of results to show (default 5)
* Define to search only files or directories. Default searches for both.
* Can return brief lists of results. Default is detailed (filename, filesize, filetype).

* Uses `du`, `find`,  and `rm` operations


## Examples:
```
# Show results with file details, without removal.
python3 durm.py /srv/app/logs/ -c -f

# Show results of 10 files with the most disk usage, without removal.
python3 durm.py /srv/app/logs/ -l 10 -c -f

# Show results with only filenames, without removal.
python3 durm.py /srv/app/logs/ -b -c -f

# Show results with only directories, without removal.
python3 durm.py /srv/app/logs/ -t d -c -f

# Remove files only older then 90 days, without prompt and detail.
python3 durm.py /srv/app/logs/ -d 90 -f -b
```

## Options:
```
-h, --help                      show this help message and exit
-l, --limit                     Number of files to return (default 5)
-d, --days                      Amount of days file is not modified (default "0")
-t, --filetype                  File is of type (default "f,d")
-b, --brief                     Dont show file details (default: False)
-c, --check,                    Run without making any changes (default: False)
-f, --force,                    Do not prompt before removal (default: False)
```


## TODO

* Nothing for now

## Changelog

### v0.0.1

* Initial release
