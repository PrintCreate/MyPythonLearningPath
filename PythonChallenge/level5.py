import urllib.request
import pickle

def main():
    req = urllib.request.urlopen("http://www.pythonchallenge.com/pc/def/banner.p").readlines()
    # res = req.read()
    # res = res.decode("UTF-8")
    data = pickle.loads(b''.join(req))
    for r in data:
        result = ''
        for s in r:
            result = result + s[0] * s[1]
        print(result)

if __name__ == '__main__':
    main()
    # channel

    '''
    笨办法
    # with open("level5.txt", "w", encoding='utf-8') as f:
    #     f.write(res)
    # pickle.UnpicklingError: the STRING opcode argument must be quoted
    # \r\n  convert \n
    with open("level5.txt","rb") as f:
        # data=pickle.dump(f,encoding="bytes")
        data=pickle.load(f)
        print(data)
    '''