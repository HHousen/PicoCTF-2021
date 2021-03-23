import binascii
from Crypto.Cipher import DES
from tqdm import tqdm

padding = "  "
encrypted_flag = binascii.unhexlify("6f745ccee635f76746be185541b9f9c046b8d707f93d0522e2325fb041c59ec7bbbaa818d7c51381")

def pad(msg):
    block_len = 8
    over = len(msg) % block_len
    pad = block_len - over
    return (msg + " " * pad).encode()

custom_known_text = pad(binascii.unhexlify("13371337").decode())
custom_ciphertext = binascii.unhexlify("8f45ca8a9264c2aa")

encrypt_table = {}
for key in tqdm(range(999999), desc="Bruteforcing 1st Key"):
    key = (f"{key:06}" + padding).encode()
    cipher = DES.new(key, DES.MODE_ECB)
    encrypted_custom = cipher.encrypt(custom_known_text)
    encrypt_table[encrypted_custom] = key

decrypt_table = {}
for key in tqdm(range(999999), desc="Bruteforcing 2nd Key"):
    key = (f"{key:06}" + padding).encode()
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted_custom = cipher.decrypt(custom_ciphertext)
    decrypt_table[decrypted_custom] = key

print("Finding Key Intersection...")
encrypt_table_set = set(encrypt_table.keys())
decrypt_table_set = set(decrypt_table.keys())
for encrypt_decrypt_value in encrypt_table_set.intersection(decrypt_table_set):
    encrypt_key = encrypt_table[encrypt_decrypt_value]
    decrypt_key = decrypt_table[encrypt_decrypt_value]
    break
print("1st Key Found: %s" % encrypt_key)
print("2nd Key Found: %s" % decrypt_key)

cipher1 = DES.new(encrypt_key, DES.MODE_ECB)
cipher2 = DES.new(decrypt_key, DES.MODE_ECB)
flag_intermediate = cipher2.decrypt(encrypted_flag)
flag = cipher1.decrypt(flag_intermediate).decode()
print("Flag: %s" % flag)
