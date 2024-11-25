from PIL import Image
import anvil
import json

with open('blocks.json') as f:
    BLOCKS = json.load(f)


region: anvil.Region = anvil.Region.from_file('out/r.0.0.mca')
chunks = [[region.get_chunk(x, z) for x in range(32)] for z in range(32)]

img = Image.new('RGB', (512, 512), 'white')

def get_block(x, z):
    chunkX = x // 16
    chunkZ = z // 16
    blockX = x % 16
    blockZ = z % 16
    return chunks[chunkZ][chunkX].get_block(blockX, 0, blockZ).name()

for x in range(512):
    for z in range(512 - 3):
        colors = [BLOCKS[get_block(x, z + i)] for i in range(3)]

        img.putpixel((x, z), tuple(colors))

img.show()