from pathlib import Path

from PIL import Image


path = Path(__file__).resolve().parent / "kubejs/assets/kubejs/textures/item/prism_lens.png"
path.parent.mkdir(parents=True, exist_ok=True)
image = Image.new("RGBA", (16, 16))
pixels = image.load()
for y in range(16):
    for x in range(16):
        radius = ((x - 7.5) ** 2 + (y - 7.5) ** 2) ** 0.5
        if 5.0 <= radius <= 6.8 and not (x >= 10 and y <= 5):
            pixels[x, y] = (16, 8, 45, 255)
        if 4.0 <= radius < 5.6 and not (x >= 10 and y <= 5):
            pixels[x, y] = (96, 39, 255, 255)
        if radius < 4.5:
            pixels[x, y] = (65, 201, 245, 230)
        if radius < 2.4:
            pixels[x, y] = (192, 247, 255, 255)
for x, y in ((7, 1), (7, 2), (7, 13), (7, 14), (1, 7), (2, 7), (13, 7), (14, 7)):
    pixels[x, y] = (255, 240, 106, 255)
image.save(path)
print(path)
