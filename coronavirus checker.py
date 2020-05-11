# Modules
import re
import urllib.request
import time
import os

# User Agent (Browsers may block urllib with a HTTP 403 error. This is a bypass)
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent}


# Getting a response from the server.
utfdata = ''  # We want to use this data globally not locally, so we'll define it here and edit it within the function.
def get_response():
    global utfdata  # This lets us change the variable globally within the function - it makes life easier.
    url = 'https://www.worldometers.info/coronavirus/'  # This is the URL we will use to find coronavirus information.
    request = urllib.request.Request(url,None,headers)  # This sends a request to the URL to get the information.
    response = urllib.request.urlopen(request)  # This opens the response to the request the URL gives us.
    data = response.read()  # We read it and store it in data because it's easier.
    utfdata = data.decode('utf-8')  # Oh, we also need to decode it into UTF-8 because the server responds in bytes.


# Searching for the number of global cases in the server's response.
def get_global_cases():
    s1 = re.search(':', utfdata)  # The first colon in the source code is right next to the cases number - how lucky!
    start_point = s1.end()  # We're going to search between s1 and s2, so the end of s1 is our start point.
    s2 = re.search('Cases and', utfdata)  # Lucky us, this is right next to our cases!
    end_point = s2.start()  # Again, we're going to search between s1 and s2, so the start of s2 is our end point.
    string_result = utfdata[start_point:end_point].strip().replace(',', '')
    int_result = int(string_result)
    return int_result  # Here, we convert the result from a string to an integer, removing the commas.


# Searching for the number of global deaths in the server's response.
def get_global_deaths():
    s1 = re.search('Cases and', utfdata)  # Luckily for us, there are six cases ands, but the first is next to our death toll.
    start_point = s1.end()  # We're going to search between s1 and s2, so our start is the end of s1.
    s2 = re.search('Deaths from COVID-19 Virus Pandemic - Worldometer', utfdata)  # Lucky us, this is right next to our deaths too!
    end_point = s2.start()  # Again, we're going to search between s1 and s2, so the start of s2 is our end point.
    string_result = utfdata[start_point:end_point].strip().replace(',', '')
    int_result = int(string_result)
    return int_result  # Here, we convert the result from a string to an integer, removing the commas.


# Searching for the number of global recoveries in the server's response.
def get_global_recoveries():
    s1 = re.search('''color:#8ACA2B ">
<span>''', utfdata)
    start_point = s1.end()
    s2 = re.search('''</span>
</div>
</div>
<div style="margin-top:50px;"></div>''', utfdata)  # As you can see, this stuff uses multiple lines - why? Because the source code is awkward.
    end_point = s2.start()
    string_result = utfdata[start_point:end_point].strip().replace(',', '')
    int_result = int(string_result)
    return int_result  # Here, we convert the result from a string to an integer, removing the commas.


def store():
    local_time = time.localtime()
    current_time = time.strftime("%H:%M:%S, %B %d, %Y", local_time)  # Gets users local time to record when the data was saved.
    file_name = input("Enter a file name (Forbidden characters will be removed, .txt is not needed on the end of your input): ")
    file_name += '.txt'
    replacements = {":": "", "?": "", "*": "", "<": "", ">": "", '"': "", "/": "", "\\": "", "|": ""}
    replacements = dict((re.escape(k), v) for k, v in replacements.items())
    pattern = re.compile("|".join(replacements.keys()))
    clean_file_name = pattern.sub(lambda m: replacements[re.escape(m.group(0))], file_name)  # I have no idea what's happening here - thank God for stack overflow.
    with open(clean_file_name, 'w') as file:
        file.write(f"""Time recorded: {current_time}.

Global cases: {get_global_cases()}
Global deaths: {get_global_deaths()}
Global Recoveries: {get_global_recoveries()}
Mortality Rate: {round(((get_global_deaths() / get_global_cases()) * 100), 2)}%""")  # Setting all the data here.
    file.close()
    return 0


# The main section of the program - this is where all the user stuff is dealt with.
def main():
    #  Setting up the response.
    print("Loading response.")
    time1 = time.time()
    get_response()
    time2 = time.time()
    time_taken = time2 - time1
    print(f'Response loaded in {time_taken} seconds.')  # A simple calculation is made with time2 and time1 to find the difference.
    # Dealing with the user.
    print("\n\nCOVID-19 Checker - K. Catterall\n")  # Fancy title.
    print("Type /help to see commands.\n")
    while True:  # We break this when the user exits the program - we effictively control an infinite loop.
        user_input = input(">>> ")
        if user_input.lower().strip().replace(' ', '') == '/help':  # All this.lower, .strip and .replace stuff is to make it as idiot proof as possible.
            print("""\nCommands:\n/cases\tView global cases of COVID-19.\n/deaths\tView global deaths from COVID-19.
/recoveries View global recoveries from COVID-19.\n/mortality  View the mortality rate of COVID-19.
/store\tStores data in a local text file.\n/exit\tExits the program.\n""")
        elif user_input.lower().strip().replace(' ', '') == '/cases':
            print(f'Global Cases: {get_global_cases()}')
        elif user_input.lower().strip().replace(' ', '') == '/deaths':
            print(f'Global Deaths: {get_global_deaths()}')
        elif user_input.lower().strip().replace(' ', '') == '/recoveries':
            print(f'Global recoveries: {get_global_recoveries()}')
        elif user_input.lower().strip().replace(' ', '') == '/mortality':
            while True:  # Takes advantage of while loop to return to second stage of command on error, rather than 1st.
                try:
                    user_input = int(input("Round to how many decimal places? (Enter an INTEGER): "))
                    print(f'\nMortality Rate: {round(((get_global_deaths() / get_global_cases()) * 100), user_input)}%')
                    break
                except ValueError:
                    print("\nEnter an integer!\n")
                    time.sleep(1)
        elif user_input.lower().strip().replace(' ', '') == '/store':
            store()
        elif user_input.lower().strip().replace(' ', '') == '/exit':
            break
        else:  # This is also idiot control - it catches pretty much anything you throw at it... well, anything the average person knows anyway.
            print(f'\n"{user_input}" is not a command!\n')
            time.sleep(1)
    print("Thank you for using the COVID-19 checker by K. Catterall!")
    time.sleep(1)
    os._exit(0)


if __name__ == "__main__":  # To be totally honest, I'm not sure why this is needed, I just know people like it when it's there.
    main()  # Calls the main function - i.e starts the program for the user.
