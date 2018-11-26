import string

table = str.maketrans(string.ascii_lowercase,"cdefghijklmnopqrstuvwxyzab")
s="g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
print(str.translate(s, table))
print(str.translate("http://www.pythonchallenge.com/pc/def/map.html",table))
# ocr