def writeFile(urlToWrite):
    fn = 'compare.txt'
    with open(fn, 'w') as createFile:
        createFile.write(urlToWrite)
        print("Wrote: " + urlToWrite)  # if you want it to see on console.

def readFile():
    fn = 'compare.txt'
    old_url = ""
    try:
        with open(fn, 'r') as rf:
            old_url = rf.read()
            print("Read: " + old_url)  # if you want it to see on console.
    except FileNotFoundError: # create file if not exists
        writeFile("")
    return old_url

curr_url = "tatasaa"
old = readFile()
if old != curr_url:
    writeFile(curr_url)