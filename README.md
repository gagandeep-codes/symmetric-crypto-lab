# Symmetric Cryptography Lab — DES, AES, GPG & Message Integrity

A hands-on lab exploring the fundamentals of **symmetric-key cryptography** and **message integrity**, completed as part of a Postgraduate Certificate in Cybersecurity & AI.

This repo covers three things:

1. **Symmetric encryption in Python** (DES & AES) using `pycryptodome`
2. **Symmetric encryption with GPG** from the command line, across multiple ciphers
3. **Message integrity verification** using a SHA-256 Message Authentication Code (MAC)

---

## Table of Contents

- [Concepts](#concepts)
- [Part 1 — DES & AES in Python](#part-1--des--aes-in-python)
- [Part 2 — GPG Symmetric Encryption](#part-2--gpg-symmetric-encryption)
- [Part 3 — Message Integrity (SHA-256 MAC)](#part-3--message-integrity-sha-256-mac)
- [Security Notes & Caveats](#security-notes--caveats)
- [What I Learned](#what-i-learned)
- [Repo Structure](#repo-structure)

---

## Concepts

**Symmetric encryption** uses a *single shared key* for both encryption and decryption. It's fast and well-suited to encrypting data at rest or in transit, but it raises the question of how two parties securely share that key in the first place.

**Confidentiality vs. integrity** are two separate goals:
- *Confidentiality* (encryption) keeps data secret.
- *Integrity* (hashing / MACs) detects whether data was altered.

You often need both — encryption alone does not tell you whether a message was tampered with.

---

## Part 1 — DES & AES in Python

A small `encryptDecrypt` class implements both algorithms using `pycryptodome`.

### Setup

```bash
python -m pip install pycryptodome
```

### How it works

| Algorithm | Key size | Block size |
|-----------|----------|------------|
| DES       | 8 bytes  | 64-bit     |
| AES-128   | 16 bytes | 128-bit    |

The process for both:

1. **Pad** the plaintext to the cipher's block size.
2. **Encrypt** the padded text with the key.
3. **Base64-encode** the ciphertext for safe display/transport.
4. **Decrypt** by reversing: Base64-decode → decrypt → unpad.

### Core methods

```python
def encryptAes(self, plainText, key):
    paddedText = pad(plainText, AES.block_size)
    aesCipher = AES.new(key, AES.MODE_ECB)
    return aesCipher.encrypt(paddedText)

def decryptAes(self, cipheredText, key):
    aesCipher = AES.new(key, AES.MODE_ECB)
    return unpad(aesCipher.decrypt(cipheredText), AES.block_size)
```

### Expected output

```
DES Decrypted Text:
b'Python is a very powerful language'

AES Decrypted Text:
b'Python is a very powerful language'
```

The decrypted text matches the original plaintext for both algorithms, confirming the round trip works.

---

## Part 2 — GPG Symmetric Encryption

This part uses **GnuPG (GPG)** for passphrase-based symmetric encryption — no key pair required. The passphrase derives the encryption key.

### List available ciphers

```bash
gpg --version
```

### Encrypt / decrypt across ciphers

A single text file was encrypted and decrypted with each of the following, to compare them:

```bash
# 3DES (legacy — modern GPG requires the override flag below)
gpg --symmetric --cipher-algo 3DES --allow-old-cipher-algos <file>.txt

# AES family (modern, recommended)
gpg --symmetric --cipher-algo AES128 <file>.txt
gpg --symmetric --cipher-algo AES192 <file>.txt
gpg --symmetric --cipher-algo AES256 <file>.txt

# Decrypt any of the above
gpg -d <file>.txt.gpg
```

> **Note:** The fact that modern GPG requires `--allow-old-cipher-algos` to use 3DES is itself a useful signal that the algorithm is outdated.

### Cipher comparison

| Cipher  | Key size | Block size | Status              |
|---------|----------|------------|---------------------|
| 3DES    | 168-bit  | 64-bit     | Legacy / deprecated |
| AES-128 | 128-bit  | 128-bit    | Modern              |
| AES-192 | 192-bit  | 128-bit    | Modern              |
| AES-256 | 256-bit  | 128-bit    | Modern (safe default) |

---

## Part 3 — Message Integrity (SHA-256 MAC)

Encryption protects secrecy but not integrity. To detect tampering, the sender and receiver each compute a tag (MAC) over the **shared key + message** using SHA-256, then compare.

```python
import hashlib

sharedkey_k = b'<shared-key>'
message = b'This lab demonstrates the steps taken by the sender and receiver to provide integrity'

# Sender computes the tag
sender = hashlib.sha256()
sender.update(sharedkey_k)
sender.update(message)
sender_mac = sender.hexdigest()

# Receiver recomputes the tag from the received message
received_message = message
receiver = hashlib.sha256()
receiver.update(sharedkey_k)
receiver.update(received_message)
receiver_mac = receiver.hexdigest()

# Compare
if receiver_mac == sender_mac:
    print("Integrity Verified: Message Accepted")
else:
    print("Integrity Failed: Message Rejected")
```

### Behaviour

- **Unchanged message** → tags match → `Message Accepted`
- **Modified message** (even one character) → tags differ → `Message Rejected`

This demonstrates exactly what an integrity check guarantees: any change to the message is detectable.

---

## Security Notes & Caveats

These are deliberate teaching simplifications. In production you would do the following differently:

- **ECB mode is insecure.** This lab uses `MODE_ECB` for simplicity, but ECB encrypts identical plaintext blocks identically, leaking structure (the "ECB penguin"). Use **CBC** or, better, **GCM** (which adds authentication).
- **DES and 3DES are deprecated.** DES's 56-bit effective key is brute-forceable; NIST has retired both. Use **AES** in real systems.
- **Use HMAC, not raw `hash(key + message)`.** The manual construction here illustrates the concept, but `hashlib`'s plain hash of key-then-message is vulnerable to length-extension attacks. The correct primitive is **HMAC** (`hmac.new(key, message, hashlib.sha256)`).
- **Never hardcode keys or passphrases.** Any keys/passphrases in lab files are placeholders. Use environment variables, a secrets manager, or a key-derivation function in real code.

---

## What I Learned

- Confidentiality (encryption) and integrity (MACs) are distinct security goals, and you often need both.
- Mode of operation (ECB vs. CBC vs. GCM) matters as much as the algorithm choice.
- Recognizing deprecated algorithms (DES, 3DES) and knowing *why* they're retired is part of practical security work.
- Moving from a Python implementation → a real CLI tool (GPG) → an integrity check end to end built genuine intuition, not just theory.

---

## Repo Structure

```
.
├── part1_des_aes.py          # Python DES & AES implementation
├── part3_integrity_mac.py    # SHA-256 MAC integrity check
├── screenshots/              # Execution screenshots
└── README.md
```

---

*Completed as part of a Postgraduate Certificate in Cybersecurity & AI. Currently working toward CompTIA Security+ and Microsoft SC-200.*
