import torch
from torchvision import transforms as transforms
from matplotlib import pyplot as plt

class ImageAug(object):
    def __init__(self):
        pass

    def img_resize(self, im, shape):
        return transforms.Resize(shape)(im)

