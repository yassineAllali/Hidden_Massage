import cv2
import os.path

# a binary 8-bits number has four parts
# the length of each part is 2
def get_part_of_binary(binary, part_number):
    if part_number < 4:
        return binary[(part_number * 2):((part_number * 2) + 2)]


def convert_to_binary_8_bits(number):
    return bin(number)[2:].zfill(8)


def binary_to_int(binary):
    return int(binary, 2)


def binary_string_chunks(text):
    result = ''
    for char in text:
        binary_char = convert_to_binary_8_bits(ord(char))
        result += binary_char
    result = [result[i:i + 2] for i in range(0, len(result), 2)]
    return result


def chunk_string_to_8_bits(binary_text):
    return [binary_text[i:i + 8] for i in range(0, len(binary_text), 8)]


def change_tail(b_number, tail):
    tail_str = str(tail)
    b_number = list(b_number)
    b_number[-1] = tail_str[1]
    b_number[-2] = tail_str[0]
    return ''.join(b_number)


def embed_text_to_image(image, text, result_image_name):
    text += '<<end>>'
    chunks = binary_string_chunks(text)
    number_chunks = len(chunks)
    chunks_count = 0
    exit_loop = False

    for i in range(len(image)):
        if exit_loop:
            break
        for j in range(len(image[i])):
            if exit_loop:
                break
            for k in range(len(image[i][j])):
                binary_element = convert_to_binary_8_bits(image[i][j][k])
                binary_element = change_tail(binary_element, chunks[chunks_count])
                image[i][j][k] = binary_to_int(binary_element)
                chunks_count += 1
                if chunks_count >= number_chunks:
                    exit_loop = True
                    break

    cv2.imwrite(result_image_name + '.png', image)


def decrypt_embedded_text(encrypted_img):
    decrypted = ''
    for i in range(len(encrypted_img)):
        for j in range(len(encrypted_img[i])):
            for element in encrypted_img[i][j]:
                binary_element = convert_to_binary_8_bits(element)
                decrypted += get_part_of_binary(binary_element, 3)

    decrypted = chunk_string_to_8_bits(decrypted)
    decrypted_text = ''
    for char in decrypted:
        ascii_char = binary_to_int(char)
        decrypted_text += chr(ascii_char)

    return decrypted_text.split('<<end>>')[0]


print('**************************************************')
print('*             Hidden Message                     *')
print('**************************************************')
print('\nChoose an option:\n1-Embed a text to an image\n2-Extract a text from an image')

choice = input('Option : ')

if choice == '1':
    print('\n*Embed a text to an image*\n')
    image_path = input('Enter the path to the image: ')
    if not os.path.isfile(image_path):
        print('Image Not Found')
    else:
        if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print('Invalid Image')
        else:
            print('Image Selected!\n')
            txt = input('Enter the text to embed: ')
            new_img_name = input('Enter a name for the generated Image: ')
            img = cv2.imread(image_path)
            print('Processing ...')
            embed_text_to_image(img, txt, new_img_name)
            print('\nThe text was embedded successfully!')

elif choice == '2':
    print('\n*Extract a text from an image*')
    image_path = input('Enter the path to the encrypted image: ')
    if not os.path.isfile(image_path):
        print('Image Not Found')
    else:
        if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print('Invalid Image')
        else:
            print('Image Selected!\n')
            img = cv2.imread(image_path)
            embedded_message = decrypt_embedded_text(img)
            print('The hidden message is : ' + embedded_message)

else:
    print('Invalid option')

