import os 
from bs4 import BeautifulSoup
import csv

data_folder = "data"
comments = []
limit = 10000

for (folder, labels, files) in os.walk(data_folder):
    for file_index, file in enumerate(files):
        if file_index < limit:
            file_path = f"{data_folder}/{file}"
            print(f"Parsing file {file_index}")
            with open(file_path, "r") as html_file:
                soup = BeautifulSoup(html_file, "html.parser")

                comment_name = ""
                comment_article = file.split(".")[0]
                comment_text = ""

                comment_elements = soup.select("div.x1gslohp > div > div") # Ugly but done because of speed

                for comment_element in comment_elements:
                    if comment_element is not None:
                        name_elements = comment_element.select("a span.x1s688f")
                        if name_elements:
                            comment_name = name_elements[0].text

                        text_element = comment_element.find("div", attrs={"dir": "auto"})
                        if text_element is not None:
                            comment_text = text_element.text

                        if comment_name:
                            comments.append({
                                "article": comment_article,
                                "name": comment_name,
                                "comment": comment_text
                            })
                 

with open("output.csv", "w") as csv_output:
    csv_writer = csv.writer(csv_output)
    csv_writer.writerow(["article", "name", "comment"])

    for comment in comments:
        csv_writer.writerow([comment.get("article"), comment.get("name"), comment.get("comment")])

print(f"All data added to the csv")
            