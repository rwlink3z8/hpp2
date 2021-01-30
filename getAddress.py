import pyautogui
import time

# idle was not working properly so I hard coded the coordinates needed in
'''
this script does the following
# 1. click in the excel window with the first lat long selected - x,y
# 2. move the arrow down
# 3. ctrl c to copy the lat long
# 4. click 3 times in the search box to select all - search box is a,b
# 5. press delete to clear the search box a,b
# 6. paste lat long into the search box
# 7. click search button - search_x, search_y
# 8. now wait because it takes a second or so to search depending on your computer
# 9. copy address to clipboard - addy_x, addy_y
# 10. click back to excel window from step 1
# 11. move to the cell to the right of the lat long
# 12. paste the address here
# 13. move down
# 14. move left
# 15. repeat

tldr - get addresses from lat-longs 
'''


wait_for_it = 5
time.sleep(wait_for_it)



x,y = pyautogui.position(x=3354, y=88)  # border of excel window
a,b = pyautogui.position(x=258, y=112)  # in the search field to delete previous search and paste new one
search_x, search_y = pyautogui.position(x=320, y=113) # location of seach button
addy_x, addy_y = pyautogui.position(x=378, y=541) # location of clipboard on google

i = 0       #Integer to be used in the while loop.
c = 2113 # number of houses 
while(i < c):
    pyautogui.click(x,y)      #The script clicks the excel Window.
    time.sleep(.1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.1)
    pyautogui.click(a,b)
    pyautogui.click(a,b)  
    pyautogui.click(a,b)     #triple click to select all
    pyautogui.hotkey('delete')
    time.sleep(.1)
    pyautogui.hotkey('ctrl', 'v')      #The script pastes the lat long into the search field.
    time.sleep(.1)
    pyautogui.click(search_x, search_y)
    time.sleep(5) # adjust this based on your browser speed - this will take a while at 5 seconds
    pyautogui.click(addy_x, addy_y)
    pyautogui.click(addy_x, addy_y)
    time.sleep(.1)
    pyautogui.click(x,y)      #The script clicks the excel Window.
    time.sleep(.1)
    pyautogui.press('right') # go to the right of the lat long
    time.sleep(.1)
    pyautogui.hotkey('ctrl', 'v') # paste in the address
    time.sleep(.1)
    pyautogui.press('down') # go down
    time.sleep(.1)
    pyautogui.press('left') # go left to get the next address
    time.sleep(.1)
    i += i
