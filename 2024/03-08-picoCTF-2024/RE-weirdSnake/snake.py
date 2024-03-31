# Create input_list
input_list = [4, 54, 41, 0, 112, 32, 25, 49, 33, 3, 0, 0, 57, 32, 108, 23, 48, 4, 9, 70, 7, 110, 36, 8, 108, 7, 49, 10, 4, 86, 43, 102, 126, 92, 0, 16, 58, 41, 89, 78]

# Create key_str
key_str = 't_Jo3'

# Generate key_list
key_list = [ord(char) for char in key_str]

# Extend key_list until its length is greater than or equal to input_list
while len(key_list) < len(input_list):
    key_list.extend(key_list)
    # key_list.pop()  # Pop the last element to match the length of input_list

# XOR operation
result = [(a ^ b) for a, b in zip(input_list, key_list)]

# Convert ASCII values to characters and join them
result_text = ''.join(map(chr, result))

print(' '.join(map(str, result)))
print(result_text)
