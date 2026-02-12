"""内存交互"""

from io import StringIO, BytesIO

f = StringIO()
f.write("hello")
f.write(" ")
f.write("world!")
print(f.getvalue())

f = StringIO("Hello!\nHi!\nGoodbye!")
while True:
    s = f.readline()
    if s == "":
        break
    print(s.strip())

f = BytesIO()
f.write("中文".encode("utf-8"))
print(f.getvalue())

f = BytesIO(b"\xe4\xb8\xad\xe6\x96\x87")
f.read()
