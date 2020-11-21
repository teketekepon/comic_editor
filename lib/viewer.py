
from PIL import Image, ImageTk

from .getter import ImgGetter
from .editor import ImgEditor


class ImgViewer:

    def __init__(self, path, op=None):
        self.op = op
        self.path = path

    def create(self, i):
        im_file = ImgGetter(self.path).get_imagefile(i)
        if im_file is None:
            return None, 'Image not found'
        if self.op is None:
            im = Image.open(im_file)
        elif self.op == 'trim':
            im = ImgEditor.trim(im_file)
        elif self.op == 'rotate':
            im = ImgEditor.rotate(im_file)
        elif self.op == 'crop_half':
            im, c2 = ImgEditor.crop_half(im_file)
        elif self.op == 'resize_half':
            im = ImgEditor.resize_half(im_file)
        else:
            im = Image.open(im_file)
        # 縦横比でサイズを決めモニターからはみ出さないサイズに調整
        size = int(800*(im.size[0]/im.size[1]))
        itk = ImageTk.PhotoImage(im.resize((size, size*im.size[1]//im.size[0])))
        return itk, im_file
