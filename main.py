import os
import sys


SEARCH_IN_MASK = False
MASK = 'txt'  # *.txt
SEARCH_IN_UPTOSIZE = False
SEARCH_IN_CONTENT = True
SIZE = 5242880  # 5 MB
ROOT_DIR = "C:/"
QUERY = "medved"


def parse_arguments():
    # such 'global' declaration needed to modify a global variable
    global SEARCH_IN_MASK
    global MASK
    global SEARCH_IN_UPTOSIZE
    global SEARCH_IN_CONTENT
    global SIZE
    global ROOT_DIR
    global QUERY

    if len(sys.argv) < 3:
        print("Usage: ./main where what")
        print("Parameters\n"
              " -t X search in *.X only\n"  # was: (in *.txt if X is omitted)\n"
              " -s Y search in files up to Y bytes length\n"
              " -nc to ignore the content (file names only)")
        input("Press Enter to continue...")
        return

    # root folder for the search
    ROOT_DIR = sys.argv[1]
    # query to search in files
    QUERY = sys.argv[2]

    waiting_for_size = False
    waiting_for_type = False
    for param in sys.argv[3:]:  # 0 for script name 1 for where 2 for what so params start from index 3
        if param == '-t':
            SEARCH_IN_MASK = True
            waiting_for_type = True
            continue
        elif param == '-s':
            SEARCH_IN_UPTOSIZE = True
            waiting_for_size = True
            continue
        elif param == '-nc':
            SEARCH_IN_CONTENT = False
            continue

        if waiting_for_type:
            MASK = param
            waiting_for_type = False
            continue

        if waiting_for_size:
            SIZE = int(param)
            waiting_for_size = False
            continue
    search()

    input("Press Enter to continue...")


def find_all(base, sub):
    occurrences = []
    start = 0
    while True:
        start = base.lower().find(sub.lower(), start)
        if start == -1:
            return occurrences
        occurrences.append(start)  # add to our list
        start += len(sub)  # use start += 1 to find overlapping matches


def search():
    # get the list of all files in the root
    list = list_files(ROOT_DIR)
    for file_name in list:
        if SEARCH_IN_MASK:
            i = file_name.rfind('.')  # last dot in a file
            if i != -1:  # contains dot
                ext = file_name[i+1:]  # getting the extension of a file
                if ext != MASK:
                    continue  # not our client
            else:
                continue

        if SEARCH_IN_UPTOSIZE:
            size = os.path.getsize(file_name)
            if size > SIZE:
                continue  # too large

        occurrences = find_all(file_name, QUERY)
        if len(occurrences) > 0:
            print(file_name, ":")
            headPrinted = True
            for occurrence in occurrences:
                print("\tAt file name\tat pos {0:d}\n\t{1:s}".format(occurrence, file_name), end='\n')
                print("\t{0}^".format(' ' * occurrence))

        if SEARCH_IN_CONTENT:
            with open(file_name, "r", encoding="ISO-8859-1") as file:
                lines = file.readlines()
                headPrinted = False
                lineNumber = 0
                for line in lines:
                    line = line.strip()
                    occurrences = find_all(line, QUERY)
                    if len(occurrences) > 0:
                        if not headPrinted:
                            print(file_name, ":")
                            headPrinted = True
                        for occurrence in occurrences:
                            print("\tline {0:d}\tat pos {1:d}\n\t{2:s}".format(lineNumber, occurrence, line), end='\n')
                            print("\t{0}^".format(' '*occurrence))
                    lineNumber += 1


def list_files(directory):
    list = []
    if not os.path.isdir(directory):
        list.append(directory)
    else:
        try:
            for each in sorted(os.listdir(directory)):
                list += (list_files(directory + '\\' + each))
        except PermissionError:
            print('Permission Denied: folder '+directory)
    return list


if __name__ == '__main__':
    parse_arguments()
