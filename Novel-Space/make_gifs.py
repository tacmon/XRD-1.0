import os
import imageio.v2 as imageio
import re

def numerical_sort(value):
    """
    Split the filename into parts of strings and numbers.
    This allows numerical sorting of filenames (e.g., 1.png, 2.png, ..., 10.png).
    """
    parts = re.split(r'(\d+)', value)
    return [int(text) if text.isdigit() else text.lower() for text in parts]

def create_gif(directory, output_filename, duration):
    """
    Create a GIF from images in a directory.
    """
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return

    images = []
    # Get all .png files in the directory
    filenames = sorted([f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))], key=numerical_sort)
    
    if not filenames:
        print(f"No image files found in {directory}.")
        return

    print(f"Creating {output_filename} from {len(filenames)} images in {directory} (duration={duration}s)...")
    
    for filename in filenames:
        filepath = os.path.join(directory, filename)
        images.append(imageio.imread(filepath))
    
    imageio.mimsave(output_filename, images, duration=duration, loop=0)
    print(f"Successfully saved {output_filename}")

if __name__ == "__main__":
    base_dir = "/root/xrd/XRD-1.0/Novel-Space/figure/real_data"
    
    # Task (1): 0.25s per frame
    create_gif(os.path.join(base_dir, "参考"), os.path.join(base_dir, "参考.gif"), duration=0.25)
    
    # Task (2): 0.1s per frame
    create_gif(os.path.join(base_dir, "AlN"), os.path.join(base_dir, "AlN.gif"), duration=0.1)
    
    # Task (3): 0.25s per frame
    create_gif(os.path.join(base_dir, "BST"), os.path.join(base_dir, "BST.gif"), duration=0.25)
    
    # Task (4): 0.25s per frame
    create_gif(os.path.join(base_dir, "CST"), os.path.join(base_dir, "CST.gif"), duration=0.25)
