tsv_file_name = str(input(".tsv file name: "))

tsv_string = ""
with open(tsv_file_name, "r", encoding="utf-8") as tsv_file:
    tsv_string = tsv_file.read()

tsv_values = tsv_string.split("	")

links = []
for value in tsv_values:
    if value.startswith("https://www.reddit.com"):
        print(value)
        links.append(value)

links_string = ""
for link in links:
    links_string += link
    links_string += "\n"

with open("links.txt", "w", encoding="utf-8") as links_file:
    links_file.write(links_string)

input("Done. File saved as 'links.txt'. Press any key to exit.")
