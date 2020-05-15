# AES-Easy - Easy AES encryption for Python
AES-Easy provides a convenient way of encrypting smaller byte strings
for storage on disk. The primary use case for this package is to be combined
with pickle for safely and securely storing serialized objects. For example,
if a program needs to cache session cookies from the python requests library,
these can be encrypted and stored on disk for subsequent executions of
the script. By defualt, the package uses 256 bit AES keys with a 128 bit
block size. This should provide reasonable security when combined with other
methods of obfuscation such as chmodding the key file and using an application
user.

## Disclaimer
This package is provided as a wrapper for the existing cryptography library.
The implementation was developed from the official documentation but its
security has not been audited. This package's license provides no warranty.

## Examples

#### Encrypting and decrypting a string of bytes
```py
from aes_easy import AESManager

msg = b'Meet me at the park at midnight.'
# Using the default constructor generates a new key using urandom.
encryptor = AESManager()

# Ensure that you store the generated key in a safe place
encryption_key = encryptor.key

enc = encryptor.encrypt(msg)
#    <aes_easy.EncryptedFile object at 0x000001B27E39BB08>
enc.data
#     b'\x99a{\xe8\...\xbe'

# Passing a key parameter skips the generation of a new key
decryptor = AESManager(key=encryption_key)

# decrypt can accept either an EncryptedFile object or the individual parameters
decryptor.decrypt(enc_file=enc)
#    b'Meet me at the park at midnight.'

```

#### Generating a key and saving it to a file
```py
from aes_easy import AESManager

encryptor = AESManager()

with open('key.dat', 'wb') as key_file:
  key_file.write(encryptor.key)
```

#### Generating a key with a different length
By default, the library generates a 256 bit key (maximum length for the underlying cryptography library). If for whatever reason you would like to generate a smaller key, you can do so by either passing it as a constructor kwarg, or when calling the `generate_key()` function.
Note that the key is provided as a length of bytes (e.g. 16 bytes = 128 bits, 32 bytes = 256 bits)
```py
from aes_easy import AESManager

# Constructor
encryptor = AESManager(key_length = 16)

# As an argument when calling the function.
encryptor.generate_key(24)

```

#### Using the helper methods to load a SSFF file into memory
The curiously named `EncryptedFile` class has a number of helper methods to read and write encrypted data along with all of the non-secret data required to decrypt them. the static `read()` function constructs an EncryptedFile that is ready to be decrypted by an AESManager's `decrypt()` function.

```
from aes_easy import AESManager, EncryptedFile

decryptor = AESManager(key=secret_key)

enc_file = EncryptedFile.read('./my_secret_file.sec')
decryptor.decrypt(enc_file=enc_file)
#    b'hunter2'

```


## SecureSerialize File Format
The SecureSerialize File Format is a space-efficient standard for storing
encrypted data in a binary format along with the information needed to decrypt
it. All values in the file header (before the datastream) are stored as
little-endian.
This inital declaration of the SSFF is incomplete and may be revised or
enhanced in the future. While future versions will feature bytes for versioning,
the SecureSerialize library will provide a method to upgrade file versions
whenever feasible.

The first two bytes (`0x00` - `0x01`) store the number of bytes occupied by
the initialization vector (iv). The iv is used during encryption and decryption
when using AES-CBC and must be included.

The next byte (`0x02`) stores the number of bytes of padding that were added to
the decrypted data in order to use CBC.

from `0x03` and onwards is the datastream. This contiguous block of data has
the iv first, followed by the actual encrypted data. As it is contiguous, there
is no deliniation between the two. Programmers are expected to use the
short int stored in `0x00` - `0x01` to calculate where the iv ends and the encrypted
data begins.

### Okay, but why not just pickle the EncryptedFile?
Touché. That would have been an easier solution. While not standardized, the SecureSerialize File Format is ever so slightly more efficient. This is compounded when storing many smaller files since pickle adds around 100 bytes.

Oh well, it was a a fun learning experience. You can pickle it if you want.


## Requirments and attributions
Uses AES primitives from [cryptography](https://pypi.org/project/cryptography/), which is distributed under the Apache Software License Version 2.0