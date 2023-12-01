import os
import sys
from datetime import datetime, timedelta, timezone
from time import sleep, time_ns
import time
from MySQLdb import Time
from requests import Session

CYAN = "\x1b[36m"
RED = "\x1b[31m"
YELLOW = "\x1b[33m"
RESET = "\x1b[0m"

AOC_BASE_URL = "https://adventofcode.com/%(year)s/day/%(day)s/input"

date = datetime.now(timezone.utc)
print(date)
YEAR = date.year
MONTH = date.month
DAY = date.day

if DAY not in range(1, 26):
    print(RED + "Day not in 1..25" + RESET)
    raise SystemExit(0)

START_TIME = datetime(YEAR, 12, 1 if MONTH == 11 else DAY + 1, 5, 0, 1, 0, timezone.utc)
TIME_OFFSET = timedelta(0, 120, 0, 0, 0, 0, 0)

time_left = START_TIME - date

print(RESET + f"Today: {DAY}.{MONTH}.{YEAR}")
hours = time_left.seconds // 3600
mins = time_left.seconds // 60 - hours * 60
seconds = time_left.seconds - hours * 3600 - mins * 60

if DAY <= 24:
    print(RESET + "NOTE: Next day begins in %s hours %s mins and %s seconds" % (hours, mins, seconds))
    if MONTH == 11 and time_left.seconds > 120:
        raise SystemExit(0)

elif DAY == 25:
    print(RESET + "NOTE: Today is the last day")

if hours == 0 and mins <= 1 and time_left.seconds >= 0:
    if mins == 1:
        print(CYAN + "It begins in a moment...")
        sleep(seconds)
    while time_left.seconds >= 0:
        date = datetime.now(timezone.utc)
        time_left = START_TIME - date
        print(CYAN + "%s seconds left...\r" % time_left.seconds, end="")
        sleep(.5)
    print(YELLOW + "AOC starts today ..." + RESET)
    print()

DAY_REPR = str(DAY).zfill(2)
FOLDER_NAME = "day" + DAY_REPR

if not os.access(FOLDER_NAME,  os.R_OK | os.W_OK):
    print(CYAN + "INFO: Creating folder %r" % FOLDER_NAME)
    os.mkdir(FOLDER_NAME)
else:
    print(CYAN + "INFO: Folder alreay exists")

args = sys.argv[1:]
filetype = ""   # filetype needs to be extension
if "h" in args or "haskell" in args or "hs" in args:
    filetype = "hs"
elif "java" in args:
    filetype = "java"
elif "c" in args:
    filetype = "c"
elif "py" in args:
    filetype = "py"
else:
    print(RED + "No filetype specified" + RESET)
    print(RED + "Usage: python_executable %s <programming_language> [-f] [-d] [-p2] [-nc]" % os.path.relpath(__file__, os.getcwd()) + RESET)
    print(RED + "Possible programming languages: %s" % ', '.join(os.path.basename(f).split(os.path.extsep)[0] for f in os.listdir(os.getcwd()) if os.path.isfile(f) and f.endswith("templ")) + RESET)
    raise SystemExit(1)       

part = "2" if "-p2" in args else "1"
FILENAME = os.path.join(FOLDER_NAME, "day" + DAY_REPR + "_part" + part + "." + filetype)
DATA_FILE = os.path.join(FOLDER_NAME, "data_" + FOLDER_NAME.lower() + ".txt")
cur_langs = [os.path.basename(f_name).split(os.path.extsep)[-1] 
             for f_name in  os.listdir(FOLDER_NAME) 
             if print(f_name) or os.path.isfile(os.path.join(FOLDER_NAME, f_name)) and os.path.basename(f_name).split(os.path.extsep)[-1] == filetype]
same_language = filetype in cur_langs

print(cur_langs, same_language)

if not os.access(FILENAME, os.R_OK | os.W_OK) or "-f" in args:
    if "-p2" not in args or "-nc" in args or not same_language:
        print(CYAN + "INFO: Created file for part%s..." % part)
        has_templ = False
        try:
            with open(filetype + ".templ", "r") as tf:
                template = tf.read() \
                    .replace("$$FILE$$", DATA_FILE.replace("\\", "\\\\")) \
                    .replace("$$FILE_O_EXT$$", DATA_FILE.split(os.sep)[-1].rsplit(".", 1)[0].replace("\\", "\\\\")) \
                    .replace("$$FOLDER$$", FOLDER_NAME)
        except FileNotFoundError:
            print(YELLOW + "WARNING: No template for file type %r found" % filetype)
        else:
            has_templ = True

        with open(FILENAME, "w") as f:
            if has_templ:
                f.write(template)  # type: ignore

    else:
        print(CYAN + "Copying file from part 1...")
        try:
            with open(FILENAME.replace("part2", "part1"), "r") as f_part1, open(FILENAME, "w") as f_part2:
                f_part2.write(f_part1.read())
        except FileNotFoundError:
            print(RED + "File from part1 not found" + RESET)
            raise SystemExit(1) from None

        except FileExistsError:
            print(RED + "File already exists" + RESET)
            raise SystemExit(1) from None

        else:
            print(CYAN + "File for part2 has been created")

else:
    print(YELLOW + "WARNING: File '%s' already exists. Use -f override" % FILENAME)

print(RESET)

print(CYAN + "INFO: Fetching todays puzzle input...")
day_url = AOC_BASE_URL % {"year": YEAR, "day": DAY}

SESSION_FILE = ".session_id"
try:
    with open(SESSION_FILE) as sess_file:
        sess_id =  sess_file.read().strip()

except FileNotFoundError:
    print(RED + "ERROR: Could not read session id")
    print(RED + "ERROR: Is the file %r present?" % SESSION_FILE)
    print(RED + "ERROR: If creating, don't forget to put the file into your .gitignore" + RESET)
    raise SystemExit(1)


print(CYAN + "INFO: Trying to access URL %r..." % day_url)
with Session() as s:
    s.cookies.update({"session": sess_id})
    response = s.get(day_url)
    if not response.ok:
        print(YELLOW + "WARNING: Server responded with %s" % response.status_code + RESET)
        raise SystemExit(1)

    data = response.text

print(CYAN + "INFO: Creating data file...")

if not os.access(DATA_FILE, os.W_OK | os.R_OK) or "-d" in args:
    with open(DATA_FILE, "w") as f:
        f.write(data)

else:
    print(YELLOW + "WARNING: Data file already exists")
    print("WARNING: Use -d to override")

print(CYAN + "INFO: Done" + RESET)
