# keygenme-py

## Problem

> keygenme-trial.py

* [Program](./keygenme-trial.py)

## Solution

1. The program contains a variable called `key_part_static1_trial` that has the first part of the flag: `picoCTF{1n_7h3_|<3y_of_`. The portion of the flag we need to find if `key_part_dynamic1_trial`.

2. When the user chooses option "c", the `enter_license` function is called. It calls `check_key` with the user provided key (the flag) and `bUsername_trial`, which is `b"GOUGH"`.

3. The `check_key` functions contains the code that fills in the `key_part_dynamic1_trial`. It takes the hexdigest of the sha256 hash of `b"GOUGH"` and then selects a certain character by an indexing to a certain point on that string.

4. We can simply find the hexdigest of the sha256 hash of `b"GOUGH"` and then get the characters at the positions it checks: `"".join([hashlib.sha256(b"GOUGH").hexdigest()[x] for x in [4,5,3,6,2,7,1,8]])`. This is the missing section of the flag.

5. We can now complete the flag: `picoCTF{1n_7h3_|<3y_of_xxxxxxxx}` --> `picoCTF{1n_7h3_|<3y_of_f911a486}`

### Flag

`picoCTF{1n_7h3_|<3y_of_f911a486}`
