import tinyimg


image = tinyimg.read('example.png')

image.rescale(320, 240)
image.rotate(30)
image.show()
image.write('output.jpeg')

# free acquired resources
image.close()