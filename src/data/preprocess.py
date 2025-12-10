import cv2
import numpy as np
from pathlib import Path
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json


class BillPreprocessor:    
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size
        
    def resize_image(self, image, target_size=None):

        if target_size is None:
            target_size = self.target_size
            
        h, w = image.shape[:2]
        target_w, target_h = target_size
        
        ratio = min(target_w / w, target_h / h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        result = np.zeros((target_h, target_w, 3), dtype=np.uint8)
        
        y_offset = (target_h - new_h) // 2
        x_offset = (target_w - new_w) // 2
        result[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        
        return result
    
    def normalize_image(self, image):
        return image.astype(np.float32) / 255.0
    
    def enhance_image(self, image):
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def denoise_image(self, image):

        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    
    def preprocess_for_model(self, image_path, enhance=True, denoise=False):

        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"No se pudo cargar la imagen: {image_path}")
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        if denoise:
            image = self.denoise_image(image)
        
        if enhance:
            image = self.enhance_image(image)
        
        image = self.resize_image(image)
        
        image = self.normalize_image(image)
        
        image = np.expand_dims(image, axis=0)
        
        return image


def create_data_augmentation(rotation_range=20, 
                             width_shift_range=0.2,
                             height_shift_range=0.2,
                             zoom_range=0.2,
                             horizontal_flip=True):

    datagen = ImageDataGenerator(
        rotation_range=rotation_range,
        width_shift_range=width_shift_range,
        height_shift_range=height_shift_range,
        zoom_range=zoom_range,
        horizontal_flip=horizontal_flip,
        vertical_flip=False, 
        brightness_range=[0.7, 1.3],
        fill_mode='nearest',
        rescale=1./255 
    )
    
    return datagen


def process_dataset(input_dir, output_dir, target_size=(224, 224)):

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    preprocessor = BillPreprocessor(target_size=target_size)
    
    class_dirs = [d for d in input_path.iterdir() if d.is_dir()]
    
    print(f"Procesando dataset desde: {input_dir}")
    print(f"Clases encontradas: {len(class_dirs)}")
    
    stats = {}
    
    for class_dir in class_dirs:
        class_name = class_dir.name
        output_class_dir = output_path / class_name
        output_class_dir.mkdir(parents=True, exist_ok=True)
        
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
            image_files.extend(list(class_dir.glob(ext)))
        
        print(f"\n  Clase: {class_name}")
        print(f"  Imágenes: {len(image_files)}")
        
        processed_count = 0
        
        for img_file in image_files:
            try:
                image = cv2.imread(str(img_file))
                if image is None:
                    continue
                
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                image = preprocessor.resize_image(image)
                image = preprocessor.enhance_image(image)
                
                output_file = output_class_dir / img_file.name
                cv2.imwrite(str(output_file), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                
                processed_count += 1
                
            except Exception as e:
                print(f"Error procesando {img_file.name}: {str(e)}")
        
        stats[class_name] = processed_count
        print(f"Procesadas: {processed_count}")
    
    stats_file = output_path / "preprocessing_stats.json"
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\nPreprocesamiento completado!")
    print(f"Estadísticas guardadas en: {stats_file}")


def create_samples_subset(processed_dir, samples_dir, samples_per_class=50):

    processed_path = Path(processed_dir)
    samples_path = Path(samples_dir)
    samples_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Creando subset de muestras...")
    
    class_dirs = [d for d in processed_path.iterdir() if d.is_dir()]
    
    for class_dir in class_dirs:
        class_name = class_dir.name
        output_class_dir = samples_path / class_name
        output_class_dir.mkdir(parents=True, exist_ok=True)
        
        image_files = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.png'))
        
        import random
        samples = random.sample(image_files, min(samples_per_class, len(image_files)))
        
        import shutil
        for img_file in samples:
            shutil.copy(img_file, output_class_dir / img_file.name)
        
        print(f"  {class_name}: {len(samples)} muestras")
    
    print(f"Subset creado en: {samples_dir}")


if __name__ == "__main__":
    print("="*60)
    print("PREPROCESAMIENTO DE DATASET")
    print("="*60)
    
    process_dataset(
        input_dir="data/raw",
        output_dir="data/processed",
        target_size=(224, 224)
    )
    
    create_samples_subset(
        processed_dir="data/processed",
        samples_dir="data/samples",
        samples_per_class=50
    )