from java.io import File  # @UnresolvedImport
from java.net import URL  # @UnresolvedImport
from javax.imageio import ImageIO  # @UnresolvedImport
from javax.swing import JLabel, JFrame, ImageIcon  # @UnresolvedImport


def open(path):  # @ReservedAssignment
    label = JLabel(ImageIcon(ImageIO.read(File(URL(path).getFile()))))
    frame = JFrame()
    frame.getContentPane().add(label)
    frame.pack()
    frame.setLocation(200, 200)
    frame.setVisible(True)
