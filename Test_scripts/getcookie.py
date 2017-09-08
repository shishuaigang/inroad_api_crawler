import http.cookiejar
import urllib.request
import urllib.parse


def gecookie(api_ver):
    c = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(c))
    url = 'http://192.168.31.99:8088/API/Account/Login'
    data = {
        "APIVersion": api_ver,
        "phonenumber": "18121225109",
        "password": "123456",
        "rememberme": "True"
    }
    post_info = urllib.parse.urlencode(data).encode(encoding='UTF8')
    request = urllib.request.Request(url, post_info)
    html = opener.open(request).read()
    return c
