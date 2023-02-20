import element


class MainPageLocators(object):
    USED = "#lbl-condition-used"
    TYPE = "#lbl-type-sail"
    LEN_MT = "#luom-m"
    LEN_FT = "#luom-ft"
    COUNTRY_DRP = "#select-cint"
    #~
    CURRENCY_DRP = "#select-currencyid"
    #~
    SEARCH_BUTTON = "//button[@onclick='jsSubmit();']"


class MainPageElements:

    class UsedButton(element.Button):
        locator = MainPageLocators.USED
        parent = None

    class TypeButton(element.Button):
        locator = MainPageLocators.TYPE
        parent = None

    class LenFeetButton(element.Button):
        locator = MainPageLocators.LEN_FT
        parent = None

    class LenMetersButton(element.Button):
        locator = MainPageLocators.LEN_MT
        parent = None

    class CountrySelection(element.Selection):
        locator = MainPageLocators.COUNTRY_DRP
        parent = None

    class CurrencySelection(element.Selection):
        locator = MainPageLocators.CURRENCY_DRP
        parent = None

    class SearchButton(element.Link):
        locator = MainPageLocators.SEARCH_BUTTON
        parent = None
        new_tab = False


class ResultsPageLocators(object):
    POPUP = ".box-text"
    POPUP_X = ".close-button"
    INDEX_HEADER = "#searchResultsHeader .navPage"
    PAGE_CUR = "#searchResultsHeader .navCurrentPage"
    PAGE_NEXT = "#searchResultsHeader .navNext .navNext"
    BOATS = ".row"
    # IMG = (By.CLASS_NAME, "boatAd__img")
    NAME = ".make-model"
    PRICE = ".price"
    LOC = ".location"
    BROKER = ".broker"
    DESC = ".description"
    # -
    ITEM_LINK = ".image-header"
    ITEM_LINK_ALT = ".image-container"


class ResultPageElements:

    class PopUp(element.PopUp):
        locator = ResultsPageLocators.POPUP_X
        parent = None

    class Index(element.PageIndex):
        parent = ".searchResultsNav"
        locator = ".//*"

    class ResultsInfoTable(element.InfoTable):
        parent = None
        locator = [".make-model", ".price", ".location", ".broker", ".description"]
        reveal_button = None

    class ItemLink(element.Link):
        locator = ".image-container"
        new_tab = True


class ItemPageLocators(object):
    # TEL.GET_ATTRIBUTE("href")
    IMG = "//div[contains(concat(' ', @class, ' '), 'galleria')]//img"
    TEL_RVL = ".phone-reveal"
    TEL = "//a[contains(concat(' ', @href, ' '), 'tel')]"
    TEL2 = "//a[contains(@href, 'tel')]"
    ADDRS = ".header p"

    YEAR = ".firstColumn dd:nth-child(2)"
    LOC = ".secondColumn dd:nth-child(2)"
    LENGTH = ".firstColumn dd:nth-child(4)"
    MATERIAL = ".secondColumn dd:nth-child(4)"
    ENGINE = ".firstColumn dd:nth-child(6)"
    YACHTWORLD_ID = ".secondColumn dd:nth-child(6)"

    SPECS_TAB = ".fullspecstab"
    FULL_SPECS = ".fullspecs"

    # SPECS[1]
    SPECS = "//strong[contains(concat(' ', text(), ' '), 'Specs')]"
    DIMENSIONS = "//*[contains(concat(' ', text(), ' '), 'Dimensions')]"


class ItemPageElements:

    class ItemInfoTable0(element.InfoTable):
        parent = None
        reveal_button = ".phone-reveal"
        locator = ["//a[contains(concat(' ', @href, ' '), 'tel')]"]

    class ItemInfoTable1(element.InfoTable):
        parent = None
        reveal_button = None
        locator = [ItemPageLocators.IMG, ItemPageLocators.YEAR, ItemPageLocators.LOC, ItemPageLocators.LENGTH,
                   ItemPageLocators.MATERIAL, ItemPageLocators.ENGINE, ItemPageLocators.YACHTWORLD_ID, ItemPageLocators.ADDRS]

    class ItemInfoTable2(element.InfoTable):
        parent = None
        reveal_button = ItemPageLocators.SPECS_TAB
        locator = [ItemPageLocators.FULL_SPECS]

    class ItemImages(element.ImageCarousel):
        carousel_open_locator = None
        img_header_locator = ".galleria-image"
        next_button_locator = ".galleria-image-nav-right"
        owner_id_locator = ".secondColumn dd:nth-child(6)"