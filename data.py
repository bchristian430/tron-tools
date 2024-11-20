def process_line(line):
    # Split line into parts and determine the structure
    parts = line.split()
    if len(parts) == 5:  # address1, address2, num1, num2, num3
        address1, address2, num1, num2, num3 = parts
        result = (int(num3) << 224) | (int(num2) << 112) | int(num1)
        print(f"{address1}, {address2}, {result}")
    elif len(parts) == 4:  # address, num1, num2, num3
        address, num1, num2, num3 = parts
        result = (int(num3) << 224) | (int(num2) << 112) | int(num1)
        print(f"{address}, {result}")

# process_line("TX4xgxs6ctAz8RFbpk4rPzBrULWHE7Siiq 1 10000000 0")
process_line("TX4xgxs6ctAz8RFbpk4rPzBrULWHE7Siiq 1055327408000 1 0")
# process_line("TX4xgxs6ctAz8RFbpk4rPzBrULWHE7Siiq 5279303715007579585600 1 1")
# process_line("TX4xgxs6ctAz8RFbpk4rPzBrULWHE7Siiq 1055327480 10000000000000000000000000 2")
# process_line("TX4xgxs6ctAz8RFbpk4rPzBrULWHE7Siiq 5279303715007579585600 10000000000000000000000000 3")
# process_line("TX4xgxs6ctAz8RFbpk4rPzBrULWHE7Siiq 1 1000000 2")
# process_line("TX4xgxs6ctAz8RFbpk4rPzBrULWHE7Siiq 1000000 100000000000 3")

# Read lines from the data file

# with open('data', 'r') as file:
#     for line in file:
#         process_line(line)