from selenium.webdriver.support.ui import WebDriverWait
from my_tools import SeleniumWrapper
from locator import *


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.get = SeleniumWrapper(self.driver, self.wait)
        self.popups = 0
        self.last_link = None
        self.url = None


class MainPage(BasePage):
    used = MainPageElements.UsedButton()
    type_sail = MainPageElements.TypeButton()
    len_feet = MainPageElements.LenFeetButton()
    len_meters = MainPageElements.LenMetersButton()
    country_select = MainPageElements.CountrySelection()
    currency_select = MainPageElements.CurrencySelection()
    search_button_new_tab = MainPageElements.SearchButton()
    wait_for_popup = ResultPageElements.PopUp()

    def search(self):
        self.used.click()
        self.type_sail.click()
        self.len_feet.click()
        self.country_select = ["Greece"]
        self.currency_select = ["Euros"]
        new_tab = self.search_button_new_tab
        popup = self.wait_for_popup
        print("- SEARCH COMPLETE -")


class ResultsPage(BasePage):

    index = ResultPageElements.Index()
    results_itemfield = ResultPageElements.ResultsInfoTable()
    item_link_new_tab = ResultPageElements.ItemLink()
    wait_for_popup = ResultPageElements.PopUp()


    def total_items(self):
        elements = self.get.elements(ResultsPageLocators.BOATS)
        print(len(elements), " items on each page")
        return elements

    def open_itemlink(self, item):
        item_link = self.get.element(ResultsPageLocators.ITEM_LINK_ALT, item)
        popup2 = self.wait_for_popup
        self.item_link_new_tab = item
        return item_link

    def itemfield_main(self, item):
        ext_model, ext_price, ext_location, ext_broker, ext_description = None, None, None, None, None
        try:
            ResultPageElements.ResultsInfoTable.parent = item
            main_items = self.results_itemfield
            ext_model, ext_price, ext_location, ext_broker, ext_description = \
                main_items[0].text, main_items[1].text, main_items[2].text, main_items[3].text, main_items[4].text
        finally:
            return ext_model, ext_price, ext_location, ext_broker, ext_description


"""
    def open_item_link(self, item):
        retries = 0
        while True:
            try:
                retries += 1
                item_link = self.get.element(ResultsPageLocators.ITEM_LINK_ALT, item)
                ActionChains(self.driver).move_to_element(item_link).key_down(Keys.CONTROL).click(item_link).key_up(Keys.CONTROL).perform()
                print("Waiting for new tab to load")
                self.wait.until(EC.number_of_windows_to_be(2))
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(1)
                self.wait.until(
                    lambda d: self.driver.execute_script('return document.readyState') == 'complete')
                print("Done")
                popup2 = self.wait_for_popup
                return item_link
                # ResultPageElements.ItemLink.parent = item
                # self.item_link_new_tab = 1
            except CE.TimeoutException:
                print("Timeout: New tab not loading, Retrying...")
                self.driver.close()
                time.sleep(1)
                self.driver.switch_to.window(self.driver.window_handles[0])
                time.sleep(1)
                if retries <= 3:
                    continue
            break
"""


class ItemPage(BasePage):
    itemfield0 = ItemPageElements.ItemInfoTable0()
    itemfield1 = ItemPageElements.ItemInfoTable1()
    itemfield2 = ItemPageElements.ItemInfoTable2()
    image_carousel = ItemPageElements.ItemImages()


    def itemfield_0(self):
        broker_tel = None
        try:
            elements = self.itemfield0
            broker_tel = elements[0].text
        finally:
            return broker_tel

    def itemfield_1(self):
        year, loc_inner, length, matrl, engine, yw_id, broker_addr, img, desc_inner, item_url =\
            None, None, None, None, None, None, None, None, None, None
        try:
            item_url = self.driver.current_url
            elements = self.itemfield1
            year = elements[1].text
            loc_inner = elements[2].text
            length = elements[3].text
            matrl = elements[4].text
            engine = elements[5].text
            yw_id = elements[6].text.split('-')[-1]
            broker_addr = elements[7].text
            img = elements[0].get_attribute('src')
            fuckyou = self.driver.find_elements_by_xpath("//*[contains(concat(' ', @class, ' '), '{}')]".format(yw_id))
            desc_inner = ()
            for fuck in fuckyou:
                desc_inner = desc_inner + (fuck.text,)
        finally:
            return year, loc_inner, length, matrl, engine, yw_id, broker_addr, img, desc_inner, item_url

    def itemfield_2(self):
        full_specs = None
        try:
            elem = self.itemfield2
            full_specs = elem[0].text
        finally:
            return full_specs

    def item_images(self):
        self.image_carousel = 2
