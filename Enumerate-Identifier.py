import re

def identify_function_calls(file_path):
    """
    Identifies instances where application functions are accessed by passing
    an identifier of the function in a request parameter in a large input file.

    Args:
    file_path (str): The path to the input file containing URLs.

    Returns:
    list: A list of matched URLs containing potential function access patterns.
    """
    # Updated regular expression pattern to match keywords in query strings
    pattern = re.compile(
    r"[\w\-.]+\?(?:[^&]*&)*(?:action|func|method|cmd|do|type|mode|operation|task|process|view|execute|op|page|event|controller|route|id|module|target)=[^&]*",
    re.IGNORECASE
)

    matched_urls = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Search for pattern in each line
                if pattern.search(line):
                    matched_urls.append(line.strip())

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")

    return matched_urls

def append_to_file(output_file, data):
    """
    Appends data to the specified output file.

    Args:
    output_file (str): The file to which the data will be appended.
    data (list): The data to append to the file.
    """
    try:
        with open(output_file, 'a', encoding='utf-8') as file:
            for line in data:
                file.write(line + '\n')
        print(f"Results have been appended to {output_file}.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

def main():
    # Prompt the user for the file path
    file_path = input("Enter the path to the input file: ")
    
    # Identify function calls in the provided file
    results = identify_function_calls(file_path)

    # Output results
    if results:
        print("\nIdentified function access patterns:")
        for url in results:
            print(url)
        
        # Append results to 'Enumerate-Identifier.txt'
        output_file = "Enumerate-Identifier.txt"
        append_to_file(output_file, results)
    else:
        print("No function access patterns were identified in the input file.")

if __name__ == "__main__":
    main()
