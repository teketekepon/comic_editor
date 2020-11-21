
import os

from PIL import Image, ImageChops

from .getter import ImgGetter

Image.MAX_IMAGE_PIXELS = 1000000000


class ImgEditor:

    def __init__(self, op, path, reverse):
        self.op = op
        self.path = path
        self.reverse = reverse
        self.error = []
        self.count = 0

    @staticmethod
    def trim(image_file):
        """空白部分を切り取る"""
        try:
            im = Image.open(image_file)
        except Exception:
            return f'Image open error: faild to open {image_file}'
        else:
            bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
            diff = ImageChops.difference(im, bg)
            diff = ImageChops.add(diff, diff, 2.0, -100)
            bbox = diff.getbbox()
            if bbox:
                return im.crop(bbox)
            else:
                return im

    @staticmethod
    def rotate(image_file):
        """上下反転させる"""
        try:
            im = Image.open(image_file)
        except Exception:
            return f'Image open error: faild to open {image_file}'
        else:
            return im.rotate(180)

    @staticmethod
    def crop_half(image_file):
        """左右で切り分ける"""
        try:
            im = Image.open(image_file)
        except Exception:
            return f'Image open error: faild to open {image_file}', None
        else:
            if im.mode == 'RGBA' or 'transparency' in im.info:
                im.convert('RGB')
                im = im.crop(im.getbbox())
            c1_image = im.crop((0, 0, im.width // 2, im.height))
            c2_image = im.crop((im.width // 2, 0, im.width, im.height))
            return c1_image, c2_image

    @staticmethod
    def resize_half(image_file):
        """解像度を半分にする"""
        try:
            im = Image.open(image_file)
        except Exception:
            return f'Image open error: faild to open {image_file}'
        else:
            return im.resize((int(im.width//2), int(im.height//2)),
                             Image.LANCZOS)

    def main(self):
        images = ImgGetter(self.path).get_imagefiles(reverse=self.reverse)
        if self.op == 'crop_half':
            for x, i in enumerate(images):
                im1, im2 = self.crop_half(i)
                if type(im1) is str:
                    self.error.append(im1)
                    continue
                self.count += 1
                name = os.path.basename(i)
                save_path = self.path + '/tmp/' + str(x) + '-12-' + name
                im1.save(self.path + '/tmp/' + str(x) + '-1-' + name)
                im2.save(self.path + '/tmp/' + str(x) + '-2-' + name)
        else:
             for x, i in enumerate(images):
                im = eval('self.'+self.op)(i)
                if type(im) is str:
                    self.error.append(im)
                    continue
                self.count += 1
                name = os.path.basename(i)
                save_path = self.path + '/tmp/' + str(x) + '-' + name
                im.save(save_path)
        return self.error, self.count

    def main_yield(self):
        """ファイルごとの保存先をyieldで返す"""
        images = ImgGetter(self.path).get_imagefiles(reverse=self.reverse)
        if self.op == 'crop_half':
            for x, i in enumerate(images):
                im1, im2 = self.crop_half(i)
                if type(im1) is str:
                    yield im1
                    continue
                name = os.path.basename(i)
                save_path = self.path + '/tmp/' + str(x) + '-12-' + name
                im1.save(self.path + '/tmp/' + str(x) + '-1-' + name)
                im2.save(self.path + '/tmp/' + str(x) + '-2-' + name)
                yield save_path
        else:
            for x, i in enumerate(images):
                im = eval('self.'+self.op)(i)
                if type(im) is str:
                    yield im
                    continue
                name = os.path.basename(i)
                save_path = self.path + '/tmp/' + str(x) + '-' + name
                im.save(save_path)
                yield save_path
