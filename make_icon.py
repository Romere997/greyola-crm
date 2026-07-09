from PIL import Image, ImageDraw

S = 256
img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
# green rounded background (brand color #4ade80)
d.rounded_rectangle([0, 0, S - 1, S - 1], radius=56, fill=(74, 222, 128, 255))
# black 2x2 grid logo (brand mark)
blk = (13, 13, 11, 255)
m, gap = 44, 20
bw = (S - 2 * m - gap) / 2

def rrect(x, y):
    d.rounded_rectangle([x, y, x + bw, y + bw], radius=18, fill=blk)

rrect(m, m)
rrect(m + bw + gap, m)
rrect(m, m + bw + gap)
rrect(m + bw + gap, m + bw + gap)

img.save('greyola.ico',
         sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
print('icon saved -> greyola.ico')
