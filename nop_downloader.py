from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp
from markdownify import markdownify
import os
import random

archive_folder_name = "NoP_archive"

get_author_script = """
    (() => {
    const t = document.querySelector('.top-matter');
    const a = t.querySelector('.author');
    return a ? a.textContent : null;
    })();
"""

get_date_script = """
    (() => {
    const d = document.querySelector('.date');
    const i = t.getElementsByTagName('time')[0];
    return i ? i.getAttribute('datetime') : null;
    })();
"""

url_list = []
while True:
    url_list_path = str(input("URL list file name: "))
    url_list_file = None
    try:
        url_list_file = open(url_list_path, "r", encoding="utf-8")
    except FileNotFoundError:
        print("File not found.")
        continue

    url_list = url_list_file.read().split()
    print(url_list)
    break


print("Enter indices of the first and last urls. Count from 1.")
starting_index = 0
ending_index = 0


while True:
    starting_index_input = int(input("Starting index: "))
    if starting_index_input < 1:
        print("Enter a positive number.")
        continue

    elif starting_index_input > (len(url_list)):
        print("Don't enter a number larger than the url list size.")
        continue

    starting_index = starting_index_input - 1
    break


while True:
    ending_index_input = int(input("Ending index: "))
    if ending_index_input < 1:
        print("Enter a positive number.")
        continue

    elif ending_index_input > (len(url_list)):
        print("Don't enter a number larger than the url list size.")
        continue

    elif ending_index_input < starting_index:
        print("Don't enter a number lower than the starting index.")
        continue

    ending_index = ending_index_input
    break


sb = sb_cdp.Chrome()
sb.goto("https://www.google.com/")
sb.sleep(10)

for i in range(starting_index, ending_index):
    sb.sleep(random.uniform(5.0, 10.0))
    sb.get_active_tab().close()
    sb.open_new_tab()
    sb.goto(url_list[i])

    main_element = sb.find_element(".usertext-body .md")
    inner_html = main_element.get_attribute("innerHTML")
    markdown = markdownify(inner_html)

    title = sb.find_element(".title .may-blank").text
    title_text = "Title: " + title + "\n\n"

    author = sb.execute_script(get_author_script)

    author_text = "Author: " + str(author) + "\n\n"

    date = sb.execute_script(get_date_script)

    date_text = "Submission date: " + str(date) + "\n\n"

    file_name = title_text + ".md"

    if not os.path.exists(archive_folder_name):
        os.mkdir(archive_folder_name)

    save_path = archive_folder_name + "/" + file_name
    with open(save_path, "w") as f:
        f.write(title_text)
        f.write(author_text)
        f.write(date_text)
        f.write(markdown)


sb.sleep(10)
sb.quit()
