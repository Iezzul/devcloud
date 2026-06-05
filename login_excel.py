import os
import pandas as pd
from playwright.sync_api import sync_playwright, expect


df = pd.read_excel("users.xlsx")

os.makedirs("screenshots", exist_ok=True)

results = []

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

        print(f"Login user: {username}")

        context = browser.new_context()

        page = context.new_page()

        try:

            page.goto("https://www.qacloud.dev/")

            page.get_by_role(
                "button",
                name="Login / Register"
            ).click()

            page.get_by_role(
                "button", name="Login", exact=True
            ).click()

            page.get_by_role(
                "textbox", name="Username or Email"
            ).fill(username)

            page.get_by_role(
                "textbox", name="Password"
            ).fill(password)

            page.locator("#loginForm").get_by_role(
                "button", name="Login"
            ).click()

            page.wait_for_timeout(3000)

            expect(
                page.get_by_role(
                    "button",
                    name="Logout"
                )
            ).to_be_visible(timeout=5000)

            status = "PASS"

            page.screenshot(
                path=f"screenshots/{username}_PASS.png"
            )

            print(f"PASS: {username}")

        except Exception as e:

            status = "FAIL"

            page.screenshot(
                path=f"screenshots/{username}_FAIL.png"
            )

            print(f"FAIL: {username}")
            print(e)

        results.append({
            "username": username,
            "status": status
        })

        context.close()

    browser.close()
pd.DataFrame(results).to_excel(
    "login_results.xlsx",
    index=False
)

print("Testing completed")


