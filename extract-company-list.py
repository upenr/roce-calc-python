""" import json

# Read the data from list.txt
with open('list-2024.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# Load the JSON data
data_list = json.loads(data)

# Extract symbols
symbols = [item["symbol"] for item in data_list]

# Write symbols to a new file
with open('mySymbols.txt', 'w') as file:
    for symbol in symbols:
        file.write(f'"{symbol}",')

print("Symbols have been written to mySymbols.txt") """

import json

# Read the data from list.txt with utf-8 encoding
with open('list-2024.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# Load the JSON data
data_list = json.loads(data)

# Extract symbols
symbols = [item["symbol"] for item in data_list]

# Define the number of entries per file
entries_per_file = 10000

# Calculate the number of files needed
num_files = (len(symbols) + entries_per_file - 1) // entries_per_file

# Write symbols to separate files
for i in range(num_files):
    # Determine the start and end indices for the current file
    start_index = i * entries_per_file
    end_index = min((i + 1) * entries_per_file, len(symbols))
    
    # Create the filename
    filename = f'mySymbols-{i + 1}.txt'
    
    # Write the current batch of symbols to the file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(', '.join(f'"{symbol}"' for symbol in symbols[start_index:end_index]))
    
    print(f"Symbols have been written to {filename}")
