ascii_numbers = [
    68, 92, 120, 48, 102, 92, 120, 49, 52, 70, 164, 170, 245, 92, 120, 57, 48, 34, 82, 92, 120, 57, 51, 122, 92, 120, 
    48, 48, 212, 92, 120, 57, 49, 186, 240, 231, 207, 191, 191, 92, 120, 48, 56, 92, 120, 56, 99, 92, 120, 57, 98, 248, 
    88, 231, 249, 254, 211, 105, 255, 95, 175, 92, 120, 57, 98, 74, 214, 92, 120, 57, 98, 193, 210, 174, 44, 176, 55, 
    # ... continue with the rest of your numbers
]

# Decode ASCII values to characters
decoded_chars = [chr(num) if num < 128 else '?' for num in ascii_numbers]  # Replace non-ASCII with '?'
decoded_text = ''.join(decoded_chars)

print(decoded_text)