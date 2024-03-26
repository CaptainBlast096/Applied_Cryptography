from PIL import Image

def main():
    img = Image.open("krab.jpg")
    pix = img.load()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            print(pix[x,y])

if __name__ == "__main__":
    main()