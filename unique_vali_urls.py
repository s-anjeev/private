import argparse
import os
import re

def output_file(data, filename):
    try:
        with open(filename, "w", encoding='utf-8', errors='replace') as file:  # Use 'replace' to handle encoding issues
            for url in data:
                file.write(f"{url.strip()}\n")
        print(f"[+] Output successfully saved into {filename}")
    except UnicodeEncodeError as e:
        print(f"[-] Error while writing to file: {e}")

def is_valid_url(url, keyword=None):
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http://, https://, or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(url_pattern, url):
        if keyword:
            return keyword in url
        else:
            return True
    return False

def process_file(filename, keyword=None):
    valid_urls = set()  # Using a set to avoid duplicates directly
    if os.path.isfile(filename):
        try:
            with open(filename, "r", encoding='utf-8', errors='ignore') as file:  # Use 'utf-8' encoding
                for line in file:
                    line = line.strip()
                    if is_valid_url(line, keyword):
                        valid_urls.add(line)
        except FileNotFoundError as err:
            print(f"[-] Error while reading file: {err}")
        except UnicodeDecodeError as er:
            print(f"[-] Error while reading file: {er}")
        except Exception as e:
            print(f"[-] Unexpected error: {e}")
    else:
        print("[-] File does not exist.")
    
    return valid_urls

def get_user_input():
    parser = argparse.ArgumentParser(description='Process URLs from a file.')
    parser.add_argument('-f', '--file', type=str, required=True, help='Specify file name containing URLs')
    parser.add_argument('-k', '--keyword', type=str, help='Specify a keyword to filter URLs')
    args = parser.parse_args()

    return args.file, args.keyword

def main():
    filename, keyword = get_user_input()
    valid_urls = process_file(filename, keyword)
    if valid_urls:
        output_file(valid_urls, filename)
    else:
        print("[-] No valid URLs found in the file.")

if __name__ == "__main__":
    main()
