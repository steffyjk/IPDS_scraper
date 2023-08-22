import easyocr
from pylab import rcParams


def convert_captcha_to_digits():
    rcParams['figure.figsize'] = 8, 16
    reader = easyocr.Reader(['en'])
    output = reader.readtext('captcha_image.jpg')
    digits = int(output[0][1].replace(' ', ''))

    return digits
