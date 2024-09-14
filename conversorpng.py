from PIL import Image

# Abrir a imagem TIFF
tiff_image = Image.open('C:\FATEC\API\IA\output_tiles\CBERS_4A_WPM_20240804_201_141_L2_BAND4_tile_0_0.tif')

# Salvar como PNG
tiff_image.save('C:\FATEC\API\IA\output_tiles\CBERS_4A_WPM_20240804_201_141_L2_BAND4_tile_0_0_PNG.png', 'PNG')