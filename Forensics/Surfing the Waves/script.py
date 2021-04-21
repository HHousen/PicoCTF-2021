from scipy.io import wavfile

# Load the audio file
_, audio_data = wavfile.read('main.wav')

# Remove last two digits since they are noise of every frame in the
# audio file.
rounded_data = [int(str(data)[:2]) for data in audio_data]

# Get and sort the 16 unique data points.
unique_data = list(set(rounded_data))
unique_data.sort()

flag_hex = []
# Loop through the rounded data points
for encoded_hex_char in rounded_data:
    # Decode each data point by mapping it to its respective hexadecimal
    # character.
    decimal_hex_char = unique_data.index(encoded_hex_char)
    # Convert to hexadecimal and remove the `0x`
    hex_char = hex(decimal_hex_char)[2:]
    flag_hex.append(hex_char)

# Convert the list of hexadecimal characters to one long string.
flag_hex_str = "".join(flag_hex)

# Convert hexadecimal to ascii.
flag_str = bytearray.fromhex(flag_hex_str).decode()

print(flag_str)
