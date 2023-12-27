def capitalize_first_letter(word):
    first_letter = word[0]
    first_letter = first_letter.upper()
    word = first_letter + word[1:]
    return word
