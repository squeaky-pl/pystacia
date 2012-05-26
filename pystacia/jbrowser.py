from java.awt.image import BufferedImage
from java.io import File
from java.net import URL
from javax.imageio import ImageIO
from javax.swing import JLabel, JFrame, ImageIcon


def open(path):
    label = JLabel(ImageIcon(ImageIO.read(File(URL(path).getFile()))))
    frame = JFrame()
    frame.getContentPane().add(label)
    frame.pack()
    frame.setLocation(200, 200)
    frame.setVisible(True)
