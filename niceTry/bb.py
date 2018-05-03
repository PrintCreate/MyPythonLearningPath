#! python3
# E:\PythonCode\pic\1.jpg -o E:\PythonCode\1.txt
from PIL import Image
import argparse

'''def handle_command():
    '命令行参数处理'
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',help = '图片的路径')
    parser.add_argument('-o','--output',help = '是否输出文件')
    parser.add_argument('--width',type = int,default = 180)
    parser.add_argument('--heigth',type = int,default = 180)
    #获取命令行参数
    return parser.parse_args()'''

#args = handle_command()
print('复制目录到此')
filename=input()
IMG=filename
WIDTH=180
HEIGHT=180
OUTPUT='e:\\1.txt'

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# 将256灰度映射到70个字符上
def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]

if __name__ == '__main__':

    rgb_im = Image.open(IMG)#打开图片
    im = rgb_im.convert('RGB')

    #使用resize()方法重新设置图片大小，其中第一个参数应是一个尺寸元组
    #而第二个参数resample有四个选项，分别是Image.NEAREST、Image.BILINEAR、
    #Image.BICUBIC、Image.LANCZOS，默认是第一个，第四个质量最高
    im = im.resize((WIDTH,HEIGHT), Image.LANCZOS)
    txt = ""

    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j,i)))
        txt += '\n'
    #这段代码是使用getpixel()方法获取某坐标像素点的RGBA值，再通过设置好的对应关系使图片被转换成字符画
    #PNG是一种使用RGBA的图像格式，其中A是指alpha即色彩空间
    #然后使用get_char函数将这个值转换成字符，换行时加上换行符
    #其中getpixel()方法会返回四个元素的元组，
    #而get_char(im.getpixel((j, i )))使用了*则会把返回的元组元素依次赋给get_char()函数的四个参数
    print (txt)

    #字符画输出到文件
    if OUTPUT:
        with open(OUTPUT,'w') as f:
            f.write(txt)
    else:
        with open("output.txt",'w') as f:
            f.write(txt)