import os
from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    username = os.environ["ESMART_USERNAME"]
    password = os.environ["ESMART_PASSWORD"]

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://kabu.com/")
    with page.expect_popup() as page1_info:
        page.locator("#pc-header").get_by_role("link", name="ログイン").click()
    page1 = page1_info.value
    page1.get_by_role("textbox", name="口座番号").fill(username)
    page1.get_by_role("button", name="次へ").click()
    page1.locator("//input[@id='password']").fill(password)
    page1.get_by_role("button", name="ログイン").click()
    page1.get_by_role("link", name="情報ツール").click()
    page1.get_by_role("link", name="先物OPボード", exact=True).click()
    page1.get_by_role("link", name="オプション", exact=True).click()
    page1.locator("#disp").select_option("ALL")
    page1.get_by_role("link", name="表示").click()

    page1.reload()
    table = page1.locator("//table[contains(@class, 'table_nopadding')]")
    with open("table.html", "w") as f:
        print(table.evaluate("el => el.outerHTML"), file=f)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
