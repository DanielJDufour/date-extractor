
_zero_to_nine_in_arabic = [unichr(1632+n) for n in range(10)]
# takes in int and returns arabic version of it
def toArabic(n):
    return "".join(map(lambda x: _zero_to_nine_in_arabic[int(x)],str(n)))

# pass in arabic number as string and get int in return
def fromArabic(s):
    return int("".join([str(ord(c)-1632) for c in text]))
