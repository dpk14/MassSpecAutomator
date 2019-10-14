THERM_STEP = 10
STATIC_RESPONSE_HEADER_LENGTH_IN_BYTES = 2

def decode_response(response, input_data_length):
    response_length = ord(response[0])
    nonempty_data_length = ord(response[1])
    loop_offset = STATIC_RESPONSE_HEADER_LENGTH_IN_BYTES + input_data_length + 1
    decoded_response = []
    for index in range(loop_offset, STATIC_RESPONSE_HEADER_LENGTH_IN_BYTES + nonempty_data_length):
        decoded_response.append(response[index])
    decoded_response = ''.join(decoded_response)
    return decoded_response