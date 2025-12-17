KB = {
    "cap": "CAP theorem states that a distributed system can only guarantee two of Consistency, Availability, and Partition Tolerance."
}

def lookup(topic: str) -> str:
    return KB.get(topic.lower(), "not found")

#Tools must be pure & deterministic
# No hidden side effects (yet)