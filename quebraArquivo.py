import rasterio
import numpy as np
import os
import tensorflow as tf

def split_image(input_tiff, output_folder, num_tiles, band_number=1, image_name='image'):
    # Abrir o arquivo TIFF com rasterio
    with rasterio.open(input_tiff) as dataset:
        # Lê a banda desejada (por exemplo, banda NIR)
        band = dataset.read(band_number)

        # Tamanho da imagem original
        height, width = band.shape
        print(f"Imagem original: {height} x {width}")
        # Calcula o tamanho aproximado de cada tile
        tile_height = int(height // np.sqrt(num_tiles))
        tile_width = int(width // np.sqrt(num_tiles))

        # Verifica se a pasta de saída existe, senão cria
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        tile_count = 0
        # Loop para dividir a imagem em blocos menores
        for i in range(0, height, tile_height):
            for j in range(0, width, tile_width):
                # Certifica-se de que o último bloco alcance o limite da imagem
                end_i = min(i + tile_height, height)
                end_j = min(j + tile_width, width)
                
                # Extrai o bloco atual
                block = band[i:end_i, j:end_j]

                # Coordenadas de transform para os blocos menores
                transform = dataset.transform * rasterio.Affine.translation(j, i)

                # Nome do arquivo para cada bloco
                output_file = os.path.join(output_folder, f"{image_name}_tile_{i}_{j}.tif")

                # Salvar o bloco como um novo arquivo TIFF
                with rasterio.open(
                    output_file,
                    'w',
                    driver='GTiff',
                    height=block.shape[0],
                    width=block.shape[1],
                    count=1,  # Apenas uma banda
                    dtype=band.dtype,
                    crs=dataset.crs,
                    transform=transform,
                ) as dst:
                    dst.write(block, 1)

                print(f"Tile {i}_{j} salvo como {output_file}")
                tile_count += 1

                # Parar se o número de tiles desejado for alcançado
                if tile_count >= num_tiles:
                    return

# Exemplo de uso
input_tiff = r'C:\FATEC\API\IA\CBERS_4A_WPM_20240804_201_141_L2_BAND4.tif'  # Caminho para a imagem TIFF
output_folder = 'output_tiles'  # Pasta para salvar os blocos
num_tiles = 10  # Número de blocos



def load_image_tiff(image_path):
    with rasterio.open(image_path) as dataset:
        band = dataset.read(1)  # Carrega a primeira banda
        band_scaled = ((band - band.min()) / (band.max() - band.min()) * 255).astype('uint8')
    return band_scaled

def preprocess_image(image_path):
    # Carregar e normalizar a imagem
    image = load_image_tiff(image_path)

    # Converta para o formato que o TensorFlow pode processar
    image_tensor = tf.convert_to_tensor(image, dtype=tf.float32)
    
    # Normaliza para 0-1 para alimentar o modelo
    image_tensor = image_tensor / 255.0

    # Expanda a dimensão para representar lotes de tamanho 1 (batch_size=1)
    image_tensor = tf.expand_dims(image_tensor, axis=0)

    return image_tensor





#split_image(input_tiff, output_folder, num_tiles, image_name='CBERS_4A_WPM_20240804_201_141_L2_BAND4')


# Carrega a imagem TIFF e a normaliza
image_path = 'C:\FATEC\API\IA\output_tiles\CBERS_4A_WPM_20240804_201_141_L2_BAND4_tile_0_0.tif'
image_tensor = preprocess_image(image_path)

print(image_tensor.shape)  # Verifica a forma do tensor
