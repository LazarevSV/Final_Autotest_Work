import subprocess


# Func starts with cmd
def run_process(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')


# Func search words in file
def find_words_in_file(filename, text_to_search):
    with open(filename, 'r') as file:
        flag = False
        for line in file:
            process = subprocess.Popen(['grep', text_to_search], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       text=True)
            output, _ = process.communicate(input=line)
            if text_to_search in output:
                flag = True
        return flag