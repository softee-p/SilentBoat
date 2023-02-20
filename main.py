from my_tools import create_dataframe, r_wait, load_main_url, navigate_back
# import pychrome
import unittest
import settings
import page


class YachtworldTest(unittest.TestCase):
    results = []

    @classmethod
    def setUpClass(cls):
        print("Class Setup")
        cls.driver = settings.set_driver()
        cls.main_url = "achtworld.co.uk"
        # my_ip = settings.Connection()
        # my_ip.cycle_wireguard()
        # my.tools.clean_dir()
        # self.driver = settings.set_driver()
        # self.tab = settings.DevTools.set_tab()
        # time.sleep(1)
        # settings.DevTools.set_listener(self.tab)
        # self.driver.get("chrome://settings/clearBrowserData")

    def setUp(self):
        self.checkpoint = load_main_url(self.driver, self.main_url)

    def test_collect_data(self):
        main_page = page.MainPage(self.driver)
        main_page.url = self.driver.current_url
        results_page = page.ResultsPage(self.driver)
        item_page = page.ItemPage(self.driver)
        if self.checkpoint is None:
            main_page.search()

        page_index = results_page.index
        pg_start, pg_current, pg_total = page_index[0], page_index[0], page_index[3]
        for i in range(1, pg_total - int(pg_start)):
            results_page.url = self.driver.current_url
            items = results_page.total_items()
            for x, item in enumerate(items):
                if self.checkpoint is not None and x < int(self.checkpoint):
                    continue
                r_wait(2, 4)
                results_page.open_itemlink(item)
                item_page.url = self.driver.current_url
                # item_page.item_images()
                item_id = int(pg_current), results_page.url, x, item_page.url

                df_row = [
                    results_page.itemfield_main(item), item_page.itemfield_0(),
                    item_page.itemfield_1(), item_page.itemfield_2(),
                    item_id
                ]
                self.results.append(df_row)
                navigate_back(self.driver)

            self.checkpoint = None
            print("Next Page: ({})-->".format(int(pg_current) + 1))
            results_page.index = ">"
            r_wait(2, 4)
            pg_current = results_page.index[0]

    @unittest.skip("Not currently in focus")
    def test_old(self):
        self.driver.get("achtworld.co.uk")
        print(input("Target set...Continue with scan?"))
        main_page = page.MainPage(self.driver)
        main_page.search()
        results_page = page.ResultsPage(self.driver)

        # data_rows = results_page.main_cycle()
        # my_tools.create_dataframe(data_rows)

    def tearDown(self):
        print("//...Initiating tearDown func for test...//")
        # create_dataframe(self.results)
        # self.tab.call_method("Network.disable")
        # time.sleep(1)
        # self.tab.stop()
        # time.sleep(1)
        # self.dev_tools.close_tab(self.tab)
        # time.sleep(1)
        for window in self.driver.window_handles:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.close()
        # time.sleep(3)
        # settings.Connection.disconnect_wireguard()
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        print("//...Initiating tearDownClass...//")
        create_dataframe(cls.results)


if __name__ == "__main__":
    try:
        unittest.main()
    except KeyboardInterrupt:
        YachtworldTest.tearDownClass()
