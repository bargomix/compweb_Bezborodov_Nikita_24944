import csv

from playwright.sync_api import sync_playwright

def login_demo(page):

    login_url = "https://quotes.toscrape.com/login"

    try:
        page.goto(login_url)
        
        page.fill("input[name='username']", "my_login")
        page.fill("input[name='password']", "my_password")

        page.wait_for_timeout(10000)  

        page.click("input.btn.btn-primary")
        page.wait_for_load_state("networkidle")

        print("Попытка входа выполнена.")

    except Exception as e:
        print("Не удалось выполнить логин:", e)



def pagination_parse(page):
    base_url = "https://quotes.toscrape.com"
    page_num = 1
    all_quotes = []

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

        # Проверяем, есть ли кнопка Next
        next_button = page.locator("li.next a")
        if not next_button.count():
            break

        page_num += 1

    write_to_csv(all_quotes)

    print("Парсинг завершен")

def write_to_csv(data):
    
    csv_filename = "quotes.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["text", "author", "author_link", "tags"]
        )
        writer.writeheader()
        writer.writerows(data)
    print("Данные сохранены")
    

def main():
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        login_demo(page)

        pagination_parse(page)

        browser.close()

if __name__ == "__main__":
    main()