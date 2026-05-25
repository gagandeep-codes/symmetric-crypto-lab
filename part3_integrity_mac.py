# Part 3 - Message Integrity with a SHA-256 MAC
#
# Demonstrates how a receiver detects whether a message was altered in transit.
# NOTE: This manual hash(key + message) construction illustrates the concept.
# In production use HMAC instead: hmac.new(key, message, hashlib.sha256)

import hashlib

# Shared secret known to both sender and receiver (placeholder)
sharedkey_k = b'<shared-key>'
message = b'This lab demonstrates the steps taken by the sender and receiver to provide integrity'

# ---- Sender: compute the tag and "send" message + tag ----
sender = hashlib.sha256()
sender.update(sharedkey_k)
sender.update(message)
sender_mac = sender.hexdigest()
print("Sender MAC:  ", sender_mac)

# ---- Receiver: recompute the tag from the received message ----
received_message = message          # try changing one character to see rejection
received_mac = sender_mac

receiver = hashlib.sha256()
receiver.update(sharedkey_k)
receiver.update(received_message)
receiver_mac = receiver.hexdigest()
print("Receiver MAC:", receiver_mac)

# ---- Compare ----
if receiver_mac == received_mac:
    print("Integrity Verified: Message Accepted")
else:
    print("Integrity Failed: Message Rejected")
