import argparse
import re
import os

def is_js_file(url, jsurls):
    pattern = r'\.(js|json|jsx|ts|tsx)(?:$|\?|\&|\#)'
    if re.search(pattern, url):
        print(f"[+] JavaScript/JSON: {url}")
        jsurls.add(url)
    
def is_img(url, imgurls):
    pattern = r'\.(jpg|jpeg|png|gif|bmp|svg|ico)(?:$|/|\?|\&|\#)'
    if re.search(pattern, url):
        print(f"[+] Image: {url}")
        imgurls.add(url)
    
def is_css(url, cssurls):
    pattern = r'\.(css)(?:$|\?|\&|\#)'
    if re.search(pattern, url):
        print(f"[+] Stylesheet: {url}")
        cssurls.add(url)

def is_other(url, otherurls):
    js_pattern = r'\.(js|json|jsx|ts|tsx)(?:$|\?|\&|\#)'
    img_pattern = r'\.(jpg|jpeg|png|gif|bmp|svg|ico)(?:$|/|\?|\&|\#)'
    css_pattern = r'\.(css)(?:$|\?|\&|\#)'

    if not (re.search(js_pattern, url) or re.search(img_pattern, url) or re.search(css_pattern, url)):
        print(f"[+] Other: {url}")
        otherurls.add(url)

def is_valid_file_path(file_path, keyword=None):
    jsurls = set()
    imgurls = set()
    cssurls = set()
    otherurls = set()

    if os.path.isfile(file_path) and file_path.lower().endswith('.txt'):
        try:
            with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                urls = set(url.strip() for url in f if is_valid_url(url.strip()))

            if keyword:
                urls = {url for url in urls if keyword in url}

            for url in sorted(urls):
                is_js_file(url, jsurls)
                is_img(url, imgurls)
                is_css(url, cssurls)
                is_other(url, otherurls)

            write_urls_to_file("js.txt", jsurls)
            write_urls_to_file("img.txt", imgurls)
            write_urls_to_file("css.txt", cssurls)
            write_urls_to_file("others.txt", otherurls)

        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print(f"[-] Unexpected error while processing file: {e}")
    else:
        print("File path or extension is not valid")
        print("Only .txt file is acceptable")

def write_urls_to_file(filename, urls):
    try:
        with open(filename, "w", encoding='utf-8', errors='ignore') as f:
            for url in urls:
                f.write(url + '\n')
    except UnicodeEncodeError as e:
        print(f"[-] Error writing to {filename}: {e}")
    except Exception as e:
        print(f"[-] Unexpected error writing to {filename}: {e}")

def is_valid_url(url):
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https:// or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(re.search(url_pattern, url))

def get_user_input():
    parser = argparse.ArgumentParser(description='Process URLs from a file.')
    parser.add_argument('-f', '--file', type=str, required=True, help='Specify file name containing URLs')
    parser.add_argument('-k', '--keyword', type=str, help='Specify a keyword to filter URLs')
    args = parser.parse_args()

    print(args.file)
    print(args.keyword)

    if args.file:
        is_valid_file_path(args.file, args.keyword)

if __name__ == "__main__":
    get_user_input()
