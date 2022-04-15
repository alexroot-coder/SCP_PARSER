import sys
import requests
from bs4 import BeautifulSoup
import pdfkit
import optparse
import os


def get_obj(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    a = soup.find_all("div", class_="menu-item")
    list_obj = []
    for tag in a:
        if "Объекты" in tag.text and "Объекты без перевода" not in tag.text:
            list_obj.append(tag.select("a"))
    result = []
    for li in list_obj:
        result.append(str(li[0]).split("\"")[1])
    return result


def get_page(url, name):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    a = soup.find("div", id="page-content")
    get_pdf(a, name)


def get_page_for_big_one(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    a = soup.find("div", id="page-content")
    return a


def get_pdf(a, name):
    try:
        with open(f'html/{name}.html', 'w', encoding="utf-8") as file:
            file.write("<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>")
            file.write(str(a))
            file.write("</body></html>")
    except UnicodeEncodeError:
        pass

    try:
        path_kit = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_kit)
        pdfkit.from_file(f"html/{name}.html", f"pdf/{name}.pdf", configuration=config)
    except OSError as e:
        print(e, name)
        pass


def get_value(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    a = soup.find("div", id="page-title")
    value = (a.text.split("Объекты ")[1].split("-"))
    if "Российского филиала\n" not in value[0]:
        result = (int(value[0].strip()), int(value[1].strip()), "not-ru")
        return result
    else:
        return 1001, 1999, "ru"


def test_404(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    a = soup.find("p", id="404-message")
    if a:
        return True
    else:
        return False


def get_without_big_one(url, link, start, finish):
    value = get_value(url + "/" + link)
    print(link)
    print(value)
    if "ru" not in link:
        print(start, finish)
        for i in range(int(start), int(finish) + 1):
            if i < 10:
                tmp = "00"
            elif i < 100:
                tmp = "0"
            else:
                tmp = ""
            last_url = url + "/scp-" + tmp + str(i)
            if not test_404(last_url):
                get_page(last_url, "/scp-" + tmp + str(i))
    else:
        for i in range(int(start), int(finish) + 1):
            last_ru_url = url + "/scp-" + str(i) + "-ru"
            if not test_404(last_ru_url):
                get_page(last_ru_url, "/scp-" + str(i) + "-ru")


def get_big_one_pdf(url, link, start, finish):
    result = []
    last_html_result = ""
    value = get_value(url + "/" + link)
    print(link)
    print(value)
    if "ru" not in link:
        print(start, finish)
        for i in range(int(start), int(finish) + 1):
            if i < 10:
                tmp = "00"
            elif i < 100:
                tmp = "0"
            else:
                tmp = ""
            last_url = url + "/scp-" + tmp + str(i)
            if not test_404(last_url):
                # get_page(last_url, "/scp-" + tmp + str(i))
                result.append(get_page_for_big_one(last_url))
    else:
        for i in range(int(start), int(finish) + 1):
            last_ru_url = url + "/scp-" + str(i) + "-ru"
            if not test_404(last_ru_url):
                # get_page(last_ru_url, "/scp-" + str(i) + "-ru")
                result.append(get_page_for_big_one(last_ru_url))

    for r in result:
        last_html_result += str(r)

    get_pdf(last_html_result, link+"_"+str(start)+"_"+str(finish))


def no_args():
    url = "http://scpfoundation.net"
    links = get_obj(url)
    print(links)
    for link in links:
        print(link)
        value = get_value(url+link)
        print(value)
        if value[2] != "ru":
            for i in range(value[0], value[1]):
                if i < 10:
                    tmp = "00"
                elif i < 100:
                    tmp = "0"
                else:
                    tmp = ""
                last_url = url + "/scp-" + tmp + str(i)
                if not test_404(last_url):
                    get_page(last_url, "/scp-" + tmp + str(i))
                    # print(url + "/scp-" + tmp + str(i))
        else:
            for i in range(value[0], value[1]):
                last_ru_url = url + "/scp-" + str(i) + "-ru"
                if test_404(last_ru_url):
                    get_page(last_ru_url, "/scp-" + str(i) + "-ru")
                    # print(last_ru_url)


def main():
    if os.path.exists("html") and os.path.exists("pdf"):
        pass
    else:
        os.mkdir("html")
        os.mkdir("pdf")

    url = "http://scpfoundation.net"

    if len(sys.argv) < 2:
        no_args()
    else:
        p = optparse.OptionParser()
        p.add_option("-b", "--big_one", default=0, help="1 - true, 0 - false", type="int")
        p.add_option("-s", "--scp_name", default=None, type='str', help="scp-name >> http://scpfoundation.net")
        p.add_option("-n", "--number_start", default=None, type="int", help="number to start parse")
        p.add_option("-N", "--number_finish", default=None, type="int", help="number to finish parse")
        options, arguments = p.parse_args()
        print(options)

        if options.big_one == 1:
            if options.scp_name == None:
                exit(0)
            elif options.number_start == None:
                exit(0)
            elif options.number_finish == None:
                exit(0)
            else:
                get_big_one_pdf(url, options.scp_name, options.number_start, options.number_finish)
        else:
            if options.scp_name == None:
                exit(0)
            elif options.number_start == None:
                exit(0)
            elif options.number_finish == None:
                exit(0)
            else:
                get_without_big_one(url, options.scp_name, options.number_start, options.number_finish)


if __name__ == "__main__":
    main()



