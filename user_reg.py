import pandas as pd
from playwright.sync_api import sync_playwright


df = pd.read_excel("users.xlsx")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        slow_mo=300
    )

    for index, row in df.iterrows():

        username = str(row["username"])
        email = str(row["email"])
        password = str(row["password"])

        email_prefix = email.split("@")[0]

        print(f"Creating user: {username}")

        context = browser.new_context()

        page = context.new_page()

        page.goto("https://www.qacloud.dev/")

        page.get_by_role(
            "button",
            name="Login / Register"
        ).click()

        page.get_by_role(
            "textbox",
            name="Username"
        ).fill(username)

        page.get_by_role(
            "textbox",
            name="your@email.com"
        ).fill(email)

        page.get_by_role(
            "textbox",
            name="Password (min 6 characters)"
        ).fill(password)

        page.get_by_role(
            "textbox",
            name="Confirm password"
        ).fill(password)

        page.get_by_role(
            "button",
            name="Register Now"
        ).click()

        print(f"Registration submitted: {email}")

        
        page1 = context.new_page()

        page1.goto("https://yopmail.com/en/")

        page1.get_by_role(
            "textbox",
            name="Login"
        ).fill(email_prefix)

        page1.get_by_title(
            "Check Inbox @yopmail.com"
        ).click()

        print(f"Checking inbox: {email_prefix}")

        
        page1.wait_for_timeout(10000)

        with page1.expect_popup() as popup_info:
             page1.locator("iframe[name='ifmail']")\
                 .content_frame\
                 .get_by_role("link").click()
        
        verify_page = popup_info.value

        page1.wait_for_timeout(3000)

        context.close()

    browser.close()