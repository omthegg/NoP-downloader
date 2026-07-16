from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp
from markdownify import markdownify

sb = sb_cdp.Chrome()
sb.goto("https://www.google.com/")
sb.sleep(10)
sb.open_new_tab()
sb.goto("https://old.reddit.com/r/NatureofPredators/comments/1sjnres/absolute_victory_prologue/")

main_element = sb.find_element(".usertext-body .md")
inner_html = main_element.get_attribute("innerHTML")
markdown = markdownify(inner_html)

title = sb.find_element(".title .may-blank").text
title_text = "Title: " + title + "\n\n"

author = sb.execute_script("""
    const t = document.querySelector('.top-matter');
    const a = t.querySelector('.author');
    return a ? a.textContent : null;
""")

author_text = "Author: " + str(author) + "\n\n"

date = sb.execute_script("""
    const d = document.querySelector('.date');
    const i = t.getElementsByTagName('time')[0];
    return i ? i.getAttribute('datetime') : null;
""")

date_text = "Submission date: " + str(date) + "\n\n"

with open("file.md", "w") as f:
    f.write(title_text)
    f.write(author_text)
    f.write(date_text)
    f.write(markdown)

sb.sleep(10)
sb.quit()
