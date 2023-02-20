from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from my_tools import cli_execute
import pychrome
import socket
import time


def set_driver(browser="chrome"):
    def chrome():
        options = set_options(Profile.stealth())
        path = "D:/PythonProjects/chromedriver-85-0-4183-87/chromedriver.exe"
        driver = webdriver.Chrome(options=options, executable_path=path)
        print(input("Driver ready. Configuration Timeout: Press Enter to Continue"))
        return driver

    def safari():
        options = set_options(Profile.default())
        driver = webdriver.Safari(options)
        return driver

    if "safari" in browser:
        return safari()
    else:
        return chrome()


def set_options(profile):
    options = Options()
    for opt in profile[0]:
        options.add_argument(opt)
    for optex in profile[1]:
        options.add_experimental_option(optex[0], optex[1])
    for ext in profile[2]:
        options.add_extension(ext)
    return options


class Profile:
    @staticmethod
    def default():
        opt = [Opt.UD_DIR]  # Opt.DEBUG_PORT
        optex = []
        ext = []
        return opt, optex, ext

    @staticmethod
    def stealth():
        opt = [Opt.UD_DIR, UserAgent.cycle(), Opt.INCOG, Opt.NO_PL, Opt.SET_BLINK, Opt.NO_BLINK]
        optex = [OptEx.SET_AUTO, OptEx.NO_AUTO]
        ext = [Ext.BADGER, Ext.ADBLOCK, Ext.NOSCRIPT, Ext.FINGERDEF, Ext.REFERER]
        return opt, optex, ext

    @staticmethod
    def headless():
        opt = [Opt.NO_HEAD, Opt.WIN_SIZE, Opt.NO_GPU, Opt.UD_DIR2, UserAgent.cycle(), Opt.INCOG, Opt.NO_PL, Opt.NO_EX,
               Opt.SET_BLINK, Opt.NO_BLINK]
        optex = [OptEx.SET_AUTO, OptEx.NO_AUTO, OptEx.BLOCK_3RD_COOKIES, OptEx.MINIMAL]
        ext = []
        return opt, optex, ext


# POINT Opt.DEBUG_PORT TO DEVTOOLS URL.
class DevTools:

    @staticmethod
    def set_tab():
        dev_tools = pychrome.Browser(url="http://localhost:8000")
        time.sleep(1)
        tab = dev_tools.list_tab()[0]
        tab.start()
        time.sleep(1)
        return tab

    @staticmethod
    def close_all_tabs(dev_tools):
        if len(dev_tools.list_tab()) == 0:
            return

        for tab in dev_tools.list_tab():
            try:
                tab.stop()
            except pychrome.RuntimeException:
                pass

            dev_tools.close_tab(tab)

        time.sleep(1)
        assert len(dev_tools.list_tab()) == 0

    @staticmethod
    def set_listener(tab):
        def start(**kwargs):
            print("LISTENER STARTED")

        def end(**kwargs):
            print("LISTENER STOPPED")

        tab.call_method("Network.enable", _timeout=20)
        time.sleep(1)
        tab.set_listener("Network.requestWillBeSent", start)
        tab.set_listener("Network.responseReceived", end)
        time.sleep(1)

    @staticmethod
    def intercept_requests(tab):
        tab.call_method("Network.enable", _timeout=20)
        time.sleep(1)
        tab.call_method("Network.setRequestInterception", {})
        tab.call_method("Network.requestIntercepted", {})
        tab.call_method("Network.continueInterceptedRequest")

    @staticmethod
    def block_url(tab):
        tab.call_method("Network.setBlockedURLs", ("*.css", "*.jpg"))

    @staticmethod
    def emulate_cellular(tab, driver):

        # TIME WITHOUT NETWORK CONDITIONS FIRST
        start = time.time()
        driver.get("https://google.com")
        print(int(time.time() - start))

        tab.call_method("Network.emulateNetworkConditions",
                        offline=False,
                        latency=100,
                        downloadThroughput=9375,  # BYTES
                        uploadThroughput=3125,
                        connectionType="cellular3g")
        # TEST WITH NET-CON
        start = time.time()
        driver.get("https://google.com")
        print(int(time.time() - start))


class UserAgent:
    used = []
    desktop_list = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",]

    @classmethod
    def cycle(cls):
        # On first start assign current UA to empty list: used = []
        for ua in cls.desktop_list:
            if ua not in cls.used:
                option = f'user-agent={ua}'
                cls.used.append(ua)
                return option


class Connection:
    used = []
    multihop_list = ["mlvdse1ch6", "mlvdse1ch7", "mlvdse1dk2", "mlvdse1fi2",
                     "mlvdse1fi3", "mlvdse15ch3", "mlvdse15ch5", "mlvdse15nl4",
                     "mlvdse15nl5", "mlvdse15no2", "mlvdse15no3", "mlvdse2ch5",
                     "mlvdse2nl4", "mlvdse2no3", "mlvdse2se10", "mlvdse4dk3",
                     "mlvdse4fi1", "mlvdse6ch5"]

    @staticmethod
    def socket_test():
        try:
            # connect to the host -- tells us if the host is reachable
            sock = socket.create_connection(("www.google.com", 80))
            if sock is not None:
                print('Closing socket')
                sock.close()
            return True
        except OSError:
            pass
        return False

    @classmethod
    def disconnect_wireguard(cls):
        if cls.used != []:
            cli_execute("sudo wg-quick down {}".format(cls.used[-1]))
            print("Disconnected from {}. Sleeping for // 10 sec.".format(cls.used[-1]))
            time.sleep(10)
        else:
            print("//You were not connected to a proxy.")

    @classmethod
    def cycle_wireguard(cls):
        # On first start assign used connections to empty list used = []
        # If previous connection exists put it inside the list
        cls.disconnect_wireguard()

        for config in cls.multihop_list:
            if config not in cls.used:
                print("Connecting to {}".format(config))
                cli_execute("sudo wg-quick up {}".format(config))
                print("Connection to {} was Successfull!".format(config))
                time.sleep(1)
                print("Timeout for // 20s.")
                time.sleep(20)
                print("Testing connection to google.com...")
                if cls.socket_test():
                    cls.used.append(config)
                    print("Connection to google via {} is stable".format(config))
                    time.sleep(5)
                    break
                else:
                    cls.used.append(config)


class MullvadOptions(object):
    SET_ACCOUNT = "mullvad account set *18&*&!*&!*&@"
    SHOW_ACCOUNT = "mullvad account get"
    UPDATE_LIST = "mullvad relay update"
    SHOW_LIST = "mullvad relay list"
    LOC_SELECT = "mullvad relay set location mma"
    SPECIFIC_SELECT = "mullvad relay set location mma se-mma-001"
    CONNECT = "mullvad connect"
    DISCONNECT = "mullvad disconnect"
    CONNECTION_STATUS = "mullvad status"
    AUTO_CONNECT_ON = "mullvad auto-connect set on"
    AUTO_CONNECT_OFF = "mullbad auto-connect set off"
    LAN_ACCESS_SET = "mullvad lan set allow"


class WireGuardOptions(object):
    CHECK_KEY = "mullvad tunnel wireguard key check"
    REGENERATE_KEY = "mullvad tunnel wireguard key regenerate"
    SET_ON = "mullvad relay set tunnel wireguard any"


class ChromeScript(object):
    # ex. chrome --headless --disable-gpu --screenshot --window-size=1280,1696 https://www.chromestatus.com/
    PRT_DOM = "--dump-dom"
    PRT_PDF = "--print-to-pdf"
    PRT_SCR = "--screenshot"


class Opt(object):
    # USE UD_DIR TO STORE COOKIES ETC
    UD_DIR = "--user-data-dir=./user_dir_primary"
    UD_DIR2 = "--user-data-dir=./user_dir_headl"
    UA = f'user-agent={"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0"}'
    INCOG = "--incognito"
    NO_PL = "--disable-plugins-discovery"
    NO_EX = "--disable-extensions"
    # DISABLE WebDriver DETECTION
    SET_BLINK = "--disable-blink-features"
    NO_BLINK = "--disable-blink-features=AutomationControlled"
    # WHEN HEADLESS ALSO SPECIFY WINDOW SIZE // OTIONAL: USE DEBUG PORT WITH http://localhost:9222 IN ANY BROWSER
    NO_HEAD = "headless"
    WIN_SIZE = "window-size=1400,600"
    NO_GPU = "--disable-gpu"
    # --
    MAX_VIEW = "--start-maximized"
    MAC_MAX_VIEW = "--kiosk"
    LANG_EN = '--lang=en_US'
    # USE PROXIES
    PROXY = '--proxy-server={}'
    # EX. CHROME DEV TOOLS PORT
    DEBUG_PORT = '--remote-debugging-port=8000'


class OptEx(object):
    NO_IMG = ["prefs", {"profile.managed_default_content_settings.images": 2}]
    # DISABLE AUTOMATION HEADER
    SET_AUTO = ["excludeSwitches", ["enable-automation"]]
    NO_AUTO = ['useAutomationExtension', False]
    # 2 IS BLOCK
    DEF_COOKIES = ["prefs", {"profile.default_content_setting_values.cookies": 2}]
    BLOCK_3RD_COOKIES = ["prefs", {"profile.block_third_party_cookies": False}]

    CUSTOM = ["prefs", {"profile.managed_default_content_settings": 2,
                        "profile.default_content_setting_values.notifications": 2,
                        "profile.managed_default_content_settings.geolocation": 2,
                        "profile.managed_default_content_settings.media_stream": 2}]
    # MINIMAL CONTENT SETTINGS
    MINIMAL = ["prefs", {  # "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.javascript": 1,
        "profile.managed_default_content_settings.plugins": 1,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.media_stream": 2}]


class Ext(object):
    ADBLOCK = 'D:/PythonProjects/chromedriver_ext/AdBlockP/3.9.5_0.crx'
    BADGER = 'D:/PythonProjects/chromedriver_ext/PrivacyBadger/2020.8.25_0.crx'
    NOSCRIPT = 'D:/PythonProjects/chromedriver_ext/NoScript/11.0.42_0.crx'
    REFERER = 'D:/PythonProjects/chromedriver_ext/RefererConf/1.35_0.crx'

    RANDOMUA = 'D:/PythonProjects/chromedriver_ext/RandomUA/2.2.13_0.crx'
    MODHEADER = 'D:/PythonProjects/chromedriver_ext/ModHeader/3.1.9_0.crx'
    FINGERDEF = 'D:/PythonProjects/chromedriver_ext/FingerprintDef/0.1.8_0.crx'
    CSSINSPECTOR = 'D:/PythonProjects/chromedriver_ext/CSSInspector/1.1.1_0.crx'
