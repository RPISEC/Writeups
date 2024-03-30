PicoCTF 2024 Crypto
rsa_oracle
300 Points

Description: Can you abuse the oracle?
An attacker was able to intercept communications between a bank and a fintech company. They managed to get the message (ciphertext) and the password that was used to encrypt the message.
After some intensive reconassainance they found out that the bank has an oracle that was used to encrypt the password and can be found here nc titan.picoctf.net 50551. Decrypt the password and use it to decrypt the message. The oracle can decrypt anything except the password.

Hints:
* Crytography Threat models: chosen plaintext attack.
* OpenSSL can be used to decrypt the message. e.g openssl enc -aes-256-cbc -d ...
* The key to getting the flag is by sending a custom message to the server by taking advantage of the RSA encryption algorithm.
* Minimum requirements for a useful cryptosystem is CPA security.

We are given a secret.enc that presumably has the encrypted flag. The second hint suggests that the flag is encrypted with
aes and we need to decrypt the password first to decrypt the flag. The RSA oracle will encrypt or decrypt anything we give it except for decrypting the password ciphertext.

Based on the hints, I began researching chosen plaintext attacks on RSA and found the following CPA. 
Given ciphertext $c*$ which an oracle will not decrypt, compute $c'= c* r^e (mod n)$. The oracle will then decrypt $c'$ into $m' = (c* r^e)^d = m r (mod n)$ where m is the original message. From there, one can compute $m = m' r^{-1} (mod n)$ to get the message.

The problem with this approach is that neither e nor n are provided, and guessing e = 65537 did not work. 
So instead, I sent a very simple message, just an exclamation mark which the oracle encrypted as $c_r = 1133697604741311354555965158888471583460206384676756410244938771294844134725343255704000707426845469467316324672197364029412911640375465954374197864603087$. I multiplied this by the encrypted password for $c_r c_p = 4793583506436899988509600873558926590111032353384630668198465067678412912500062389506645888108565357282556179703986373298976497928706792080377716695827738543845665186162239354237846821846664687429316694994435755173829991199528878247119402284072071325788650130975008956945195365183023261499563821229598499502$. The oracle was happy to decrypt this for me into $d = m_r m_p$, and I found the original password with
```python
d = "cf087376059"
password_hex = hex(int(d, 16) // ord("!"))
print("Password: ", ''.join([chr(int(password_hex[i:i+2], 16)) for i in range(2, len(password_hex), 2)]))
```

So the password is da099 and we get the flag with 
```bash
openssl enc -aes-256-cbc -d -in secret.enc -k da099
```
picoCTF{su((3ss_(r@ck1ng_r3@_da099d93}