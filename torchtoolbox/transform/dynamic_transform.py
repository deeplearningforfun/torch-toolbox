__all__ = ['DynamicRandomResizedCrop', 'DynamicResize', 'DynamicCenterCrop']

import abc
from PIL import Image
from torchvision.transforms import functional as F, RandomResizedCrop, Resize, CenterCrop
from torchvision.transforms.transforms import _setup_size


class DynamicSize(abc.ABC):
    def __init__(self, size):
        self._active_size = size

    @property
    def active_size(self):
        return self._active_size

    @active_size.setter
    def active_size(self, size):
        self._active_size = _setup_size(size, error_msg="Please provide only two dimensions (h, w) for size.")


class DynamicRandomResizedCrop(RandomResizedCrop, DynamicSize):
    def __init__(self, size, scale=(0.08, 1.0), ratio=(3. / 4., 4. / 3.), interpolation=Image.BILINEAR):
        RandomResizedCrop.__init(size, scale=scale, ratio=ratio, interpolation=interpolation)
        DynamicSize.__init__(self, self.size)

    def forward(self, img):
        i, j, h, w = self.get_params(img, self.scale, self.ratio)
        return F.resized_crop(img, i, j, h, w, self._active_size, self.interpolation)


class DynamicResize(Resize, DynamicSize):
    def __init__(self, size, interpolation=Image.BILINEAR):
        Resize.__init__(size, interpolation)
        DynamicSize.__init__(self.size)

    def forward(self, img):
        """
        Args:
            img (PIL Image or Tensor): Image to be scaled.

        Returns:
            PIL Image or Tensor: Rescaled image.
        """
        return F.resize(img, self._active_size, self.interpolation)


class DynamicCenterCrop(CenterCrop, DynamicSize):
    def __init__(self, size):
        CenterCrop.__init__(size)
        DynamicSize.__init__(self.size)

    def forward(self, img):
        """
        Args:
            img (PIL Image or Tensor): Image to be cropped.

        Returns:
            PIL Image or Tensor: Cropped image.
        """
        return F.center_crop(img, self._active_size)
