from selenium.webdriver.common.by import By
from selenium_ui.conftest import print_timing
from util.conf import CONFLUENCE_SETTINGS
from selenium_ui.base_page import BasePage

def app_specific_action_csi_view_page_document_macro(webdriver, datasets):

    page = BasePage(webdriver)

    @print_timing("selenium_app_custom_action:csi_view_page_document_macro")
    def measure():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/display/CSIO/Document+Macro+View")
        page.wait_until_visible((By.ID, "title-text"))  # Wait for title field visible
        page.wait_until_clickable((By.XPATH, "//div[@class='aui-message aui-message-error']/p[3]/button[@class='csi-error-message-missing-sharepoint-authentication-login aui-button' and 3]"))  # Wait for you app-specific UI element by ID selector
    measure()

def app_specific_action_csi_view_page_list_macro(webdriver, datasets):
    
    page = BasePage(webdriver)

    @print_timing("selenium_app_custom_action:csi_view_page_list_macro")
    def measure():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/display/CSIO/List+Macro+View")
        page.wait_until_visible((By.ID, "title-text"))  # Wait for title field visible
        page.wait_until_clickable((By.XPATH, "//div[@class='aui-message aui-message-error']/p[3]/button[@class='csi-error-message-missing-sharepoint-authentication-login aui-button' and 3]"))  # Wait for you app-specific UI element by ID selector
    measure()

def app_specific_action_csi_view_page_blog_document_macro(webdriver, datasets):
    
    page = BasePage(webdriver)

    @print_timing("selenium_app_custom_action:csi_view_page_blog_document_macro")
    def measure():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/display/CSIO/2021/01/01/Blog+Document+Macro+View")
        page.wait_until_visible((By.ID, "title-text"))  # Wait for title field visible
        page.wait_until_clickable((By.XPATH, "//div[@class='aui-message aui-message-error']/p[3]/button[@class='csi-error-message-missing-sharepoint-authentication-login aui-button' and 3]"))  # Wait for you app-specific UI element by ID selector
    measure()

def app_specific_action_csi_view_page_blog_list_macro(webdriver, datasets):
    
    page = BasePage(webdriver)

    @print_timing("selenium_app_custom_action:csi_view_page_blog_list_macro")
    def measure():
        page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/display/CSIO/2021/01/01/Blog+List+Macro+View")
        page.wait_until_visible((By.ID, "title-text"))  # Wait for title field visible
        page.wait_until_clickable((By.XPATH, "//div[@class='aui-message aui-message-error']/p[3]/button[@class='csi-error-message-missing-sharepoint-authentication-login aui-button' and 3]"))  # Wait for you app-specific UI element by ID selector
    measure()