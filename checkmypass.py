#import necessary libraries before running the code on your local compiler

import requests
import hashlib

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    print(res)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code},check API')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    #check if password exists in API response
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times....change password')
        else:
            print(f'{password} not found.....Good Password')
    return 'done'

def get_passwords():
    no_passwords = int(input("Enter the no of passwords to be checked: "))
    passwordList = []
    for i in range(no_passwords):
        password = input('Enter Password:  ')
        passwordList.append(password)
    return passwordList

main(get_passwords())
