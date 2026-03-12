from playwright.sync_api import sync_playwright


def pagination_parse(base_url):
    page_num = 1
    all_quotes = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        while True:
            url = f"{base_url}/page/{page_num}/"
            page.goto(url)
            page.wait_for_selector(".quote")

            quote_elements = page.locator(".quote")
            count = quote_elements.count()

            for i in range(count):
                quote = quote_elements.nth(i)

                text = quote.locator(".text").inner_text()
                author = quote.locator(".author").inner_text()

                author_link = quote.locator("a[href^='/author/']").first.get_attribute("href")
                author_link = f"{base_url}{author_link}"

                tag_elements = quote.locator(".tag").all()
                tags = [t.inner_text() for t in tag_elements]
                tags_str = ", ".join(tags)

                all_quotes.append(
                    {
                        "text": text,
                        "author": author,
                        "author_link": author_link,
                        "tags": tags_str,
                    }
                )

            next_button = page.locator("li.next a")
            if not next_button.count():
                break

            page_num += 1

        browser.close()

    return all_quotes