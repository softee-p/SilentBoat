from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as CE
from my_tools import retry_page
import time

# TODO: 1. USE __SET__ TO SET PARENT FOR ELEMENTS # ---> DONE (partially)


class Input(object):

    def __set__(self, obj, value):
        driver = obj.driver
        element = obj.get.element(self.locator, self.parent, clickable=True)
        element.clear()
        element.send_keys(value)

    def __get__(self, obj, owner):
        driver = obj.driver
        element = obj.get.element(self.locator, self.parent, clickable=True)
        return element


class Link(object):
    # TODO: Use below method to set parent element, in all other func
    def __set__(self, obj, value):
        attempts = 0
        driver = obj.driver
        self.parent = value
        element = obj.get.element(self.locator, self.parent)
        while True:
            try:
                attempts += 1
                obj.last_link = element
                if self.new_tab is False:
                    ActionChains(driver).move_to_element(element).click(element).perform()
                else:
                    ActionChains(driver).move_to_element(element).key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()
                    print("Waiting for windows")
                    obj.wait.until(EC.number_of_windows_to_be(2))
                    driver.switch_to.window(driver.window_handles[-1])

                time.sleep(2)
                obj.wait.until(
                    lambda d: driver.execute_script('return document.readyState') == 'complete')
                print("PAGE LOADED")
            except CE.TimeoutException as error:
                print(error, "\nTimeout: New tab not loading, Rereshing...")
                driver.refresh()
                time.sleep(4)
                if attempts <= 1:
                    continue
                retry_page(driver, obj.wait, element)
                if attempts <= 2:
                    continue
            except CE.ElementClickInterceptedException as error:
                print(error)
                try:
                    print("Trying to find ancestor link")
                    element = obj.get.element("./ancestor::href", element)
                    element.click()
                except CE.ElementNotInteractableException as error:
                    print(error)
                    print("No parent link found")
            break

    def __get__(self, obj, owner):
        attempts = 0
        driver = obj.driver
        wait = obj.wait
        element = obj.get.element(self.locator, self.parent, clickable=True)
        while True:
            try:
                attempts += 1
                obj.last_link = element
                if self.new_tab is False:
                    ActionChains(driver).move_to_element(element).click(element).perform()
                else:
                    ActionChains(driver).move_to_element(element).key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()
                    print("Waiting for windows")
                    obj.wait.until(EC.number_of_windows_to_be(2))
                    driver.switch_to.window(driver.window_handles[-1])

                time.sleep(2)
                wait.until(
                    lambda d: driver.execute_script('return document.readyState') == 'complete')
                print("PAGE LOADED")
            except CE.TimeoutException as error:
                print(error, "\nTimeout: New tab not loading, Rereshing...")
                driver.refresh()
                time.sleep(4)
                if attempts <= 1:
                    continue
                retry_page(driver, obj.wait, element)
                if attempts <= 2:
                    continue
            except CE.ElementClickInterceptedException as error:
                print(error)
                try:
                    print("Trying to find ancestor link")
                    element = obj.get.element("./ancestor::href", element)
                    element.click()
                except CE.ElementNotInteractableException as error:
                    print(error)
                    print("No parent link found")
            break
        return element


class Button(object):

    def __set__(self, obj, value):
        driver = obj.driver
        element = obj.get.element(self.locator, value, clickablue=True)
        return element

    def __get__(self, obj, owner):
        driver = obj.driver
        element = obj.get.element(self.locator, self.parent, clickable=True)
        return element


class Selection(object):

    # VALUE TAKES A LIST
    def __set__(self, obj, value):
        driver = obj.driver
        element = obj.get.element(self.locator, self.parent, clickable=True)
        select_object = Select(element)
        if len(select_object.all_selected_options) > 1:
            select_object.deselect_all()
            time.sleep(1)
        for thing in value:
            select_object.select_by_visible_text(thing)

    # RETURNS TWO(2) LISTS !!!
    def __get__(self, obj, owner):
        driver = obj.driver
        element = obj.get.element(self.locator, self.parent, clickable=True)
        select_object = Select(element)
        all_options = select_object.options
        all_selected_options = select_object.all_selected_options
        return all_options, all_selected_options


class PageIndex(object):

    def __set__(self, obj, value):
        print("//INDEX")
        driver = obj.driver
        elements = obj.get.elements(self.locator, self.parent)
        for elem in elements:
            elem_attri = elem.get_attribute('class')
            elem_text = elem.text
            if value in elem_text.lower() or value in elem_attri.lower():
                ActionChains(driver).move_to_element(elem).click(elem).perform()
                time.sleep(2)
                obj.wait.until(
                    lambda d: d.execute_script('return document.readyState') == 'complete')
                break

    def __get__(self, obj, owner):
        print("//INDEX")
        driver = obj.driver
        elements = obj.get.elements(self.locator, self.parent)
        pg_total = 0
        pg_next = None
        pg_first = None
        pg_last = None
        pg_current = None
        for elem in elements:
            elem_attri = elem.get_attribute('class')
            elem_text = elem.text
            if ">" in elem_text.lower():
                pg_next = elem
            if "last" in elem_text.lower() or elem_attri.lower():
                pg_last = elem
            if "first" in elem_text.lower() or elem_attri.lower():
                pg_first = elem
            if "current" in elem_attri.lower():
                pg_current = elem.text

            for word in elem.text.split(" "):
                if word.isdigit():
                    print(word)
                    if word == "1":
                        pg_first = elem
                    if int(word) > pg_total:
                        pg_total = int(word)
        print("Total pages in search results: ", pg_total)
        print("Current page: ", pg_current)
        return pg_current, pg_first, pg_next, pg_total, pg_last


class InfoTable(object):

    # SET VALUE = ATTRIBUTE TO GET ATTR.VALUE OF ELEMENTS LIST
    def __set__(self, obj, value):
        driver = obj.driver

        poop_list = []
        for poop in self.locator:
            element = obj.get.element(poop, self.parent)
            poop_list.append(element.get_attribute(value))
        return poop_list

    # GET ELEMENTS FROM LOCATOR LIST
    def __get__(self, obj, owner):
        irregularity = 0
        driver = obj.driver
        wait = obj.wait
        while True:
            print("Irreg: ", irregularity)
            if self.reveal_button is not None:
                reveal_button = obj.get.element(self.reveal_button, clickable=True)
                ActionChains(driver).move_to_element(reveal_button).click(reveal_button).perform()
            results = []
            for poop in self.locator:
                if irregularity < 4:
                    element = obj.get.element(poop, self.parent)
                else:
                    element = None
                    results.append(element)
                    continue

                results.append(element)
                if element is None:
                    irregularity += 1
                if irregularity == 2:
                    print("ERROR: Irregularity detected.\nReloading page...")
                    driver.refresh()
                    print("Finished Refresh, waiting... (4)")
                    time.sleep(4)
                    break
                elif irregularity == 3:
                    print("ERROR: Second Irregularity detected.\nRetrying Item-link...")
                    retry_page(driver, wait, obj.last_link)
                    break

            if irregularity == 0 or irregularity > 4:
                break
        return results


class PopUp(object):
    # SET VALUE = TIME TO WAIT FOR POPUP

    def __get__(self, obj, value):
        driver = obj.driver
        try:
            if obj.popups == 0:
                obj.popups += 1
                element = obj.get.element(self.locator, self.parent, clickable=True)
                element.click()
                print("- PopUp Closed -")

            else:
                print("PopUp already closed once")
        except CE.TimeoutException:
            print("Stopped waiting for PopUp.")


class Image(object):
    # SET MAKES SCRN OF ELEMENTS
    # GET RETURNS SRC

    def __set__(self, obj, value):
        driver = obj.driver
        results = []
        for loc in self.locator:
            img = obj.get.element(loc, self.parent)
            owner_id = obj.get.element(self.owner_id_locator).text
            img.screenshot("./YW_images/{}.png".format(owner_id))


    def __get__(self, obj, owner):
        driver = obj.driver
        results = []
        for loc in self.locator:
            element = obj.get.element(loc, self.parent)
            results.append(element.get_attribute('src'))
            owner_id = obj.get.element(self.owner_id_locator).text
            element.screenshot("./YW_images/{}.png".format(owner_id))
        return results





class ImageCarousel(object):
    # SET MAKES SCRN FOR 'value' NUM OF IMAGES, 0 for Infinite till dupe
    # GET RETURNS ONLY ELEMENTS

    def __set__(self, obj, value):
        driver = obj.driver
        if self.carousel_open_locator is not None:
            carousel_open = obj.get.element(self.carousel_open_locator, clickable=True)
            ActionChains(driver).move_to_element(carousel_open).click(carousel_open).perform()
            obj.wait.until(
                lambda d: d.execute_script('return document.readyState') == 'complete')
            carousel_close = obj.get.element(self.carousel_close_locator, clickable=True)

        next_button = obj.get.element(self.next_button_locator, clickable=True)
        passed = []
        temp = 0
        while temp < value or value == 0:
            img_header = obj.get.element(self.img_header_locator, invisible=True)
            img = obj.get.element("#img", img_header)
            print(img)
            print(img_header)
            src = img.get_attribute('src')
            if src in passed:
                break
            owner_id = obj.get.element(self.owner_id_locator).text
            img.screenshot("./YW_images/{}.png".format(owner_id))
            passed.append(src)
            temp += 1
            ActionChains(driver).move_to_element(next_button).click(next_button).perform()
            obj.wait.until(
                lambda d: d.execute_script('return document.readyState') == 'complete')
            # time.sleep(1)
        if self.carousel_open_locator is not None:
            ActionChains(driver).move_to_element(carousel_close).click(carousel_close).perform()
            time.sleep(1)

    def __get__(self, obj, owner):
        driver = obj.driver
        if self.carousel_open_locator is not None:
            carousel_open = obj.get.element(self.carousel_open_locator, clickable=True)
            ActionChains(driver).move_to_element(carousel_open).click(carousel_open).perform()
            obj.wait.until(
                lambda d: d.execute_script('return document.readyState') == 'complete')
            carousel_close = obj.get.element(self.carousel_close_locator, clickable=True)

        next_button = obj.get.element(self.next_button_locator, clickable=True)
        passed = []
        infinite = True
        while infinite:
            img_header = obj.get.element(self.img_header_locator)
            img_elem = obj.get.element(".//img", img_header)
            # src = img_elem.get_attribute('src')
            if img_elem in passed:
                break
            passed.append(img_elem)
            ActionChains(driver).move_to_element(next_button).click(next_button).perform()
            obj.wait.until(
                lambda d: d.execute_script('return document.readyState') == 'complete')
        if self.carousel_open_locator is not None:
            ActionChains(driver).move_to_element(carousel_close).click(carousel_close).perform()
        return passed
