from selenium import webdriver

"""

This program is an educational project designed to practice web-scraping and digesting data in a usable format.
While it may not be the most efficient way to gather the information and would benefit greatly from utilizing APIs,
this was mainly done to learn the ins and outs of finding elements on a webpage through xPath selectors and
manipulating data in a manner that is easily digestible for the end user.

The main purpose is to grab the starting goaltender information off Daily FaceOff and display the data within
the program.

"""

# Possible improvements:

# - Add inputs for users who had specific goaltenders to follow as a watchlist.
# - Notify user by email if a goaltender on their watchlist has been confirmed as starting.
# - Have the program run efficiently on a loop in the background and alert the user of any status change.
# - Look into API integration (may require a rewrite or new program)
# - Look into storing the goaltenders as flag variables instead of list and add booleans for starting = True/False
# - Implement GUI

# Things to Fix:
# - Incorporate better new line implementation in the get_starting_goaltenders function.
# - Make the grab_information_from_site function more efficient and run faster

"""

Initiate the web driver with selenium. Headless option added to prevent it from opening as we just want the info.

"""

# Option to allow or disallow opening of the browser

option = webdriver.ChromeOptions()
option.add_argument('headless')

# Open chromedriver to Starting Goalies Page on Daily FaceOff

driver = webdriver.Chrome(r'C:\Users\tyler\PycharmProjects\chromedriver.exe', options=option)
driver.get('https://www.dailyfaceoff.com/starting-goalies/')
driver.refresh()  # Refresh added here b/c previous iterations did not display current info sometimes.

"""

Setting up the list variables to be appended from the site information as it populates.

"""

header_list = []
goalie_list = []
status_list = []

"""

This function pulls the information from the site looking for Game Name: Goalie: Status. Utilizing nested for loops
to cycle through all of the possible xPaths. 

"""


# Definite opportunity for optimization here as it loads slow.

def grab_information_from_site():
    for x in range(1, 11):
        for y in range(1, 5):
            for z in range(1, 5):
                goalie1 = driver.find_elements_by_xpath('//*[@id="goalies-'
                                                        + str(x) + '"]/div['
                                                        + str(y) + ']/div/div['
                                                        + str(z) + ']/div[1]/div[1]/a/h4')
                goalie_id = [x.text for x in goalie1]
                if goalie_id:
                    goalie_list.append(goalie_id)
            header1 = driver.find_elements_by_xpath('//*[@id="goalies-'
                                                    + str(x) + '"]/div['
                                                    + str(y) + ']/h4')
            header1value = [x.text for x in header1]
            if header1value:
                header_list.append(header1value)

            status1 = driver.find_elements_by_xpath('//*[@id="goalies-'
                                                    + str(x) + '"]/div[2]/div/div['
                                                    + str(y) + ']/div[1]/div[2]/div[2]/h5')
            status_id = [x.text for x in status1]
            if status_id:
                status_list.append(status_id)


"""

This function takes all of the list elements and presents them in a "prettier" format to be viewed by user.

"""


# Probably a better way to display this, maybe look into a dictionary for future iterations?


def get_starting_goaltenders():
    i = 0  # start the iteration at 0 so we have a value to increment through the lists
    for header in range(0, len(header_list)):
        print(header_list[header])  # return name of game Goalies are starting in.
        print('')  # Look into incorporating a better way to implement new lines.
        print('Goalie: ', str(goalie_list[i]))  # the goalie_list and the status_list should always have the same len
        print('Status: ', str(status_list[i]))  # so we can simply increment the value by 1 after it prints to get next
        print('')
        i += 1
        print('Goalie: ', str(goalie_list[i]))
        print('Status: ', str(status_list[i]))
        print('')
        i += 1


"""

Calling the functions to run the program.

"""

grab_information_from_site()

g_list = [item for sublist in goalie_list for item in sublist]
s_list = [item for sublist in status_list for item in sublist]

changes = {"Confirmed": True,
           "Likely": False,
           "Unconfirmed": False
           }

s_list_bool = [changes.get(x, x) for x in s_list]
dic = dict(zip(g_list, s_list_bool))
print(str(dic))

driver.quit()
