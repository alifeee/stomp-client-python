import pickle

FILE = "msg.pkl"

with open(FILE, "rb") as f:
    msg = pickle.load(f)

for m in msg:
    print()
    print(m)
