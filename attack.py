import hashlib
import time

def getHash(bytes, num):
    ## Hash the bytes
    readable_hash = hashlib.sha256(bytes).hexdigest()

    ## Return last n digits of hex hash
    return int(readable_hash, 16) & (2 ** (num * 4) - 1)

def bdayAttack(n):
    with open("real.txt", "rb") as f:
        bytes_real_og = f.read()

    with open("fake.txt", "rb") as f:
        bytes_fake_og = f.read()

    real_seen = [getHash(bytes_real_og, n)]
    fake_seen = [getHash(bytes_fake_og, n)]
    real_map = {getHash(bytes_real_og, n):0}
    fake_map = {getHash(bytes_fake_og, n):0}

    counter = 0

    bytes_real = bytes_real_og
    bytes_fake = bytes_fake_og

    while (True):
        counter += 1

        bytes_real += b' '
        bytes_fake += b' '

        ## Get Hashes
        hash1 = getHash(bytes_real, n)
        hash2 = getHash(bytes_fake, n)
        
        ## Check Append
        if hash1 in fake_seen:
            real = counter
            fake = fake_map[hash1]
            break
        elif hash2 in real_seen:
            real = real_map[hash2]
            fake = counter
            break
            
        ## Update Arrays
        real_seen.append(hash1)
        fake_seen.append(hash2)
        real_map[hash1] = counter
        fake_map[hash2] = counter

    ## Produce New Files
    with open(f"real_{n}same.txt", "wb") as f:
        f.write(bytes_real_og + real * b' ')

    with open(f"fake_{n}same.txt", "wb") as f:
        f.write(bytes_fake_og + fake * b' ')

    return counter

if __name__ == "__main__":
    for i in range(2, 11):
        t1 = time.time()
        num = bdayAttack(i)
        t2 = time.time()
        print("*************************************")
        print(f"********* {i} digits Matching *********")
        print("*************************************")
        print(f"Time of Attack: {t2 - t1}")
        print(f"Attempts: {num}")
        print(f"Expected Attempts: {2 ** (i * 2)}")
        print("\n\n\n")