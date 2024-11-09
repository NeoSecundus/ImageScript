from dataclasses import dataclass


@dataclass
class _ConverterSettings:
    arx: int = 1
    """Aspect Ratio X"""
    ary: int = 1
    """Aspect Ratio Y"""


class Converter:
    _conf = _ConverterSettings()

    @classmethod
    def file_to_image(cls):
        pass

    @classmethod
    def image_to_file(cls):
        pass

    @classmethod
    def execute_image(cls):
        pass

    @classmethod
    def pack(cls):
        pass

    @classmethod
    def unpack(cls):
        pass
