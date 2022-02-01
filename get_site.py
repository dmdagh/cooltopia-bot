from bs4 import BeautifulSoup
import requests
import os


def main():
    url_base = "https://cooltopia.coolcatsnft.com"
    result = requests.get(url_base)
    doc = BeautifulSoup(result.text, "html.parser")
    url_suffixes = [
        a.attrs["href"]
        for a in doc.find_all("a")
        if "." not in a.attrs["href"]
        and "#" not in a.attrs["href"]
        and "/" != a.attrs["href"]
    ]
    url_suffixes.insert(0, "/")
    for url_suffix in url_suffixes:
        url = url_base + url_suffix
        url_split = url.replace("https://", "").split("/")
        if len(url_split) == 2 and url_split[1] == "":
            filepath = f"{url_split[0]}/main.md"
        elif len(url_split) == 2 and url_split[1] != "":
            continue
        elif len(url_split) == 3:
            filepath = f"{url_split[0]}/{url_split[1]}/{url_split[2]}.md"
            dirpath = f"{url_split[0]}/{url_split[1]}"
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        title = doc.find("div", {"dir": "auto", "data-testid": "page.title"})
        title2s = doc.find_all(
            "div", {"dir": "auto", "data-rnw-media-class": "208__207"}
        )
        divs = doc.find_all(
            "div",
            {"dir": "auto"},
        )
        with open(filepath, "w") as f:
            tabstr = ""
            last_line = ""
            for div in divs:
                if len(div.text) < 30 and "Previous" in div.text:
                    break
                elif div == title:
                    last_line = f"# {div.text}\n\n"
                    f.write(last_line)
                elif (
                    div in title.parent.parent.parent.parent.descendants
                    and div.has_attr("data-rnw-media-class")
                ):
                    last_line = f"\n## {div.text}\n\n"
                    f.write(last_line)
                elif (
                    div in title.parent.parent.parent.parent.descendants
                    and div.parent.has_attr("tabindex")
                    and div.text in last_line
                ):
                    continue
                elif (
                    div in title.parent.parent.parent.parent.descendants
                    and div.parent.has_attr("tabindex")
                ):

                    tabstr = "|"
                    for divc in div.parent.parent:
                        tabstr = f"{tabstr} {divc.text} |"
                    last_line = tabstr + "\n"
                    f.write(last_line)
                    othline = "|" + (" --- |" * len(div.parent.parent)) + "\n"
                    f.write(othline)
                elif (
                    div in title.parent.parent.parent.parent.descendants
                    and div.parent.parent.parent.parent.has_attr("data-rnw-int-class")
                ):
                    tabstr = "|"
                    for divc in div.parent.parent.parent.parent:
                        tabstr = f"{tabstr} {divc.text} |"
                    last_line = tabstr + "\n"
                    f.write(last_line)
                elif div in title.parent.parent.parent.parent.descendants:
                    f.write(f"{div.text}\n")
        print(f"wrote {filepath}")


if __name__ == "__main__":
    main()
