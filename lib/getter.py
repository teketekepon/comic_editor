
import glob
import re

from PIL import Image


class ImgGetter:

    def __init__(self, path):
        self.path = path

    def get_imagefile(self, i, *, recursive=False):
        """指定したインデックスの画像ファイルパスを取得する"""
        epath = glob.escape(self.path)
        images = sorted(glob.glob(epath + r'/*.png', recursive=recursive)
                        + glob.glob(epath + r'/*.jpg', recursive=recursive))
        try:
            return images[i]
        except IndexError:
            return None

    def get_imagefiles(self, *, recursive=False, reverse=False):
        """フォルダから画像ファイルパスのリストを取得する"""
        epath = glob.escape(self.path)
        if reverse:
            images = sorted(glob.glob(epath + r'/*.png', recursive=recursive)
                            + glob.glob(epath + r'/*.jpg', recursive=recursive),
                            reverse=True)
        else:
            images = sorted(glob.glob(epath + r'/*.png', recursive=recursive)
                            + glob.glob(epath + r'/*.jpg', recursive=recursive))
        return images

    def generator_imagefiles(self):
        """フォルダから画像ファイルパスを取得するジェネレータ"""
        epath = glob.escape(self.path)
        for x in glob.iglob(epath + r'/*'):
            if re.serch(r'\.png$|\.jpg$|\.jpeg$', x):
                yield x

    def generator_images(self):
        """フォルダ内の画像ファイルからImageオブジェクトを生成するジェネレータ"""
        epath = glob.escape(self.path)
        for x in glob.iglob(epath + r'/*.png'):
            if re.serch(r'\.png$|\.jpg$|\.jpeg$', x):
                try:
                    yield Image.open(x)
                except Exception:
                    print(f'Image open error: faild to open "{x}"')
                    continue
