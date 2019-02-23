import urllib.request

def internet_on():
    try:
        urllib.request.urlopen('http://172.217.18.238',timeout=1)
        print("Good wifi.")
        return True
    except Exception as e:
        print("Bad wifi.")
        raise TypeError(e)
        return False

if __name__ == '__main__':
    internet_on()