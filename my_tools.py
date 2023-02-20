from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions as CE
from random import randint
import subprocess
import pandas
import time
import os


def cli_execute(command):
    if "sudo" in command:
        sudo_command = command.split(" ")
        var1 = subprocess.Popen(sudo_command)
    else:
        var1 = subprocess.Popen([command],
                                universal_newlines=True,
                                stdout=subprocess.PIPE,
                                shell=True,
                                stderr=subprocess.PIPE)

    output, error = var1.communicate()
    if var1.returncode != 0:
        print("Subprocess-Command failed. Exit code: ", var1.returncode, "Error: ", error)
        return False
    # output_split = output.split("\n")
    return output


def r_wait(tmin, tmax):
    time.sleep(randint(tmin, tmax))


def clean_dir():
    if cli_execute("rm -rv ./user_dir_primary/*"):
        print("Clean-up Complete")
        time.sleep(3)
        cli_execute("cp -r ./user_dir_fresh/* ./user_dir_primary")
        print("Copied from fresh chrome user_directory\nSleep 5 sec...")
        time.sleep(3)
    else:
        print("ERROR: REFRESH FAILED")


def navigate_back(driver):
    if len(driver.window_handles) > 1:
        for window in driver.window_handles[1:]:
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(1)
    else:
        driver.back()


def retry_page(driver, wait, link=None):
    url = driver.current_url

    if len(driver.window_handles) > 1:
        for window in driver.window_handles[1:]:
            driver.close()
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(1)
        if link is None:
            ActionChains(driver).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()
            time.sleep(1)
            wait.until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(url)
        else:
            ActionChains(driver).move_to_element(link).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
            wait.until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(1)
    else:
        driver.back()
        time.sleep(5)
        driver.forward()

    wait.until(
        lambda d: driver.execute_script('return document.readyState') == 'complete')
    print("Page loaded")



def create_dataframe(df_rows):

    if df_rows == []:
        print("No Data for Dataframe")
        return

    new_df_rows = []
    for df_row in df_rows:
        ext_model, ext_price, ext_location, ext_broker, ext_description = df_row[0]
        broker_tel = df_row[1]
        year, loc_inner, length, matrl, engine, yw_id, broker_addr, img, desc_inner, item_url = df_row[2]
        full_specs = df_row[3]
        pagenum, pageurl, itemnum, itemurl = df_row[4]

        new_df_row = [ext_model, ext_price, ext_location, ext_broker, ext_description, broker_tel, year,
                      loc_inner, length, matrl, engine, yw_id, broker_addr, img, desc_inner, full_specs,
                      pagenum, pageurl, itemnum, itemurl]
        score = 0
        for item in new_df_row:
            score += 1 if item is not None else score
        if score != 0:
            new_df_rows.append(new_df_row)

    if new_df_rows == []:
        print("No Data for Dataframe")
        return

    dataframe = pandas.DataFrame(new_df_rows,
                                 columns=["ext_model", "ext_price", "ext_loc", "ext_broker", "ext_description",
                                          "broker_tel", "year", "loc_inner", "length", "material", "engine", "yw_id",
                                          "broker_address", "img_src", "desc_inner", "FULL SPECS",
                                          "Page Nr.", "Page Url", "Item Nr.", "Item Url"])

    if not os.path.isfile("./yachtworld.csv"):
        dataframe.to_csv("./yachtworld.csv", index=True)
        print("Created new dataframe")
    else:
        old_df = pandas.read_csv('./yachtworld.csv')
        old_df2 = old_df[:-1]
        result = old_df2.append(dataframe, sort=False)

        result.to_csv("./yachtworld.csv", index=False)
        # dataframe.to_csv("./yachtworld.csv", mode='a', header=False, index=True)
        print("Existing dataframe was overwritten.\n",
              "Item Nr: [", old_df.tail(1).values.tolist()[0][0], "] was reprocessed")




def save_progress(current_page, current_item, current_url, total_scanned):
    with open('./progress_save.txt', 'a') as save_file:
        print(current_page, file=save_file)
        print(current_item, file=save_file)
        print(current_url, file=save_file)
        print(total_scanned, file=save_file)


def load_main_url(driver, main_url):
    if os.path.isfile('./yachtworld.csv'):
        df = pandas.read_csv('./yachtworld.csv')
        last_row = df.tail(1)
        dflist = last_row.values.tolist()

        page_nr = dflist[0][25]
        page_url = dflist[0][26]
        item_nr = dflist[0][27]
        item_url = dflist[0][28]

        print("// Checkpoint found.")
        print("// Item Location: \n", "Page: ", page_nr, "\n", "Item: ", item_nr)
        print(input("Enter to START"))
        driver.get(page_url)
        return item_nr, page_url

    else:
        print("No checkpoint found.")
        driver.get(main_url)
        print(input("Enter to START"))
        return None









class SeleniumWrapper(object):
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.tags = ["a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi",
                     "bdo", "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code",
                     "col", "colgroup", "data", "datalist", "dd", "del", "details", "dfn", "dialog", "div",
                     "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "footer", "form", "h1",
                     "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "iframe",
                     "img", "input", "ins", "kbd", "keygen", "label", "legend", "li", "link", "main", "map",
                     "mark", "menu", "menuitem", "meta", "meter", "nav", "noscript", "object", "ol", "optgroup",
                     "option", "output", "p", "param", "pre", "progress", "q", "rb", "rp", "rt", "rtc", "ruby",
                     "s", "samp", "script", "section", "select", "small", "source", "span", "strong", "style",
                     "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th",
                     "thead", "time", "title", "tr", "track", "u", "ul", "var", "video", "wbr"]

    def element(self, locator, parent=None, clickable=False, invisible=False):
        element = None
        self.wait.until(
            lambda d: self.driver.execute_script('return document.readyState') == 'complete')
        parent = self.driver if parent is None else parent
        parent = self.element(parent) if type(parent) == str else parent
        if parent == "":
            print("ERROR(get_element): Parent not found")
            return parent
        if locator == "":
            return parent
        elif (locator[0] == '.' and './/' not in locator) or locator[0] == '#' or locator in self.tags:
            print("Waiting for lambda element: {} css".format(locator))
            try:
                self.wait.until(
                    lambda p: parent.find_element_by_css_selector(locator))
            except CE.TimeoutException:
                print("ERROR: No such Element: {}...".format(locator))
                return element
            print("DOne")
            element = parent.find_element_by_css_selector(locator)
            if not invisible:
                print("Waiting for EC.visibility of element: {}".format(locator))
                element = self.wait.until(
                    EC.visibility_of(element))
                print("DOne")
            if clickable:
                print("Waiting for clickable element: {}".format(locator))
                element = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
            # element = parent.find_element_by_css_selector(locator)
            return element
        else:
            print("Waiting for lambda element: {} Xpath".format(locator))
            try:
                self.wait.until(
                    lambda p: parent.find_element_by_xpath(locator))
            except CE.TimeoutException:
                print("No such Element: {}...".format(locator))
                return element
            print("DOne")
            element = parent.find_element_by_xpath(locator)
            if not invisible:
                print("Waiting for EC.visibility of element: {}".format(locator))
                element = self.wait.until(
                    EC.visibility_of(element))
                print("DOne")
            if clickable:
                print("Waiting for clickable element: {}".format(locator))
                element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, locator)))
                # element = parent.find_element_by_css_selector(locator)
            return element

    def elements(self, locator, parent=None, clickable=False, timeout=20):
        elements = []
        self.wait.until(
            lambda d: self.driver.execute_script('return document.readyState') == 'complete')
        parent = self.driver if parent is None else parent
        parent = self.element(parent) if type(parent) == str else parent
        if parent == "":
            print("ERROR(get_element): Parent not found")
            return parent
        if locator == "":
            return parent
        elif (locator[0] == '.' and './/' not in locator) or locator[0] == '#' or locator in self.tags:
            print("Waiting for lambda find elements: {} css".format(locator))
            try:
                self.wait.until(
                    lambda p: parent.find_elements_by_css_selector(locator))
            except CE.TimeoutException:
                print("No such Element(s)...")
                return elements
            print("Done")
            elements = parent.find_elements_by_css_selector(locator)
            # print("Waiting for visibility of all elements")
            # elements = self.wait.until(
                # EC.visibility_of_all_elements_located((By.CSS_SELECTOR, locator)))
            # print("Done")
            if clickable:
                print("Waiting for one of all elements to be clickable: {}".format(locator))
                elements = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
            return elements
        else:
            print("Waiting for lambda find elements: {} xpath".format(locator))
            try:
                self.wait.until(
                    lambda p: parent.find_elements_by_xpath(locator))
            except CE.TimeoutException:
                print("No such Element(s)...")
                return elements
            print("Done")
            elements = parent.find_elements_by_xpath(locator)
            # print("Waiting for visibility of all elements")
            # elements = self.wait.until(
                # EC.visibility_of_all_elements_located((By.XPATH, locator)))
            print("Done")
            if clickable:
                print("Waiting for one of all elements to be clickable: {}".format(locator))
                elements = self.wait.until(EC.element_to_be_clickable((By.XPATH, locator)))
            return elements


class MyExpectedConditions:

    class ElementHasAttribute(object):
        """An expectation for checking that an element has a particular css attribute.
        locator - used to find the element
        returns the WebElement once it has the particular css class
        """

        def __init__(self, locator, keyword, attribute):
            self.locator = locator
            self.keyword = keyword
            self.attribute = attribute

        def __call__(self, driver):
            element = driver.find_element(*self.locator)  # Finding the referenced element
            if self.keyword in element.get_attribute(self.attribute):
                return element
            else:
                return False

# Wait until an element with id='myNewInput' has desired attribute value
# element = wait.until(ElementHasAttribute((By.ID, 'myNewInput'), "Keyword", "class/value/text()"))

    class ElementHasText:

        def __init__(self, locator, keyword):
            self.locator = locator
            self.keyword = keyword

        def __call__(self, driver):
            element = driver.find_element(*self.locator)
            if self.keyword in element.text:
                return element
            else:
                return False
