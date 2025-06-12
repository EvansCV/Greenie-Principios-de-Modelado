from PIL import ImageTk, Image

def leer_imagen(path, size):
        return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ADAPTIVE))

def leer_icon(path):
        return ImageTk.PhotoImage(Image.open(path))


