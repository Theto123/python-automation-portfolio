import re

def check(p):
    s=0
    if len(p)>=8: s+=1
    if re.search(r"[A-Z]",p): s+=1
    if re.search(r"[a-z]",p): s+=1
    if re.search(r"\d",p): s+=1
    if re.search(r"[^\w]",p): s+=1
    return s

if __name__ == "__main__":
    print(check("StrongPass123!"))