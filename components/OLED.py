from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from time import sleep


class OLED:
    def __init__(self):
        self.serial = i2c(port=1, address=0x3C)
        self.device = sh1106(self.serial)

    def paint(self, texts=[]):
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="white", fill="black")
            y=0
            for text in texts:
                draw.text((5,y), text, fill="white")
                y +=10
                
    def print(self,x, y, text):
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="white", fill="black")
            draw.text((x,y), text, fill="white")
                            

if __name__ == '__main__':

    print('SYSTEM ON...')
    oled = OLED()
    oled.paint(['Erivelto', 'Clenio', 'Da' ,'Costa', 'E', 'Silva'])
    sleep(5)
