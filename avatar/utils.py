import requests
from PIL import Image, ImageOps, ImageDraw
from io import BytesIO
import math
import os

PI=3.14

def check_cache_img(url):
    # Check if the cache path not exists
    if not os.path.join('static', 'avatars'):
        os.makedirs(os.path.join('static', 'avatars'))
        
    # Check if the image is already cached
    cache_path = os.path.join('static', 'avatars', os.path.basename(url.split('/')[-1]+'.jpg'))
    if os.path.exists(cache_path):
        return cache_path
    return None

def load_image_as_circle(image_url, radius, proxies=None):
    try:
        # Add proxy support in the request
        if check_cache_img(image_url):
            print('Using cached image')
            img = Image.open(check_cache_img(image_url))
        else:
            response = requests.get(image_url, proxies=proxies)
            img = Image.open(BytesIO(response.content))
            img.save(os.path.join('static', 'avatars', os.path.basename(image_url.split('/')[-1])+'.jpg'))
        response = requests.get(image_url, proxies=proxies)
        img = Image.open(BytesIO(response.content))

        # Calculate diameter from radius
        diameter = radius * 2

        # Ensure source image is larger or equal to target size before resizing
        if img.size[0] < diameter or img.size[1] < diameter:
            img = img.resize((diameter, diameter), Image.Resampling.LANCZOS)
        else:
            # Resize using LANCZOS resampling
            img = img.resize((diameter, diameter), Image.Resampling.LANCZOS)

        # Create a mask to crop the image into a circle
        mask = Image.new('L', (diameter, diameter), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, diameter, diameter), fill=255)

        # Apply the mask to create a circular image
        img = ImageOps.fit(img, (diameter, diameter), centering=(0.5, 0.5))
        img.putalpha(mask)

        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

# Function to plot avatars in circular layout with varying sizes using PIL
def plot_avatars_full_circle(friends_dict, center_avatar_url, proxies=None):
    # Create a blank 1024x1024 white canvas
    canvas_size = (800, 800)
    canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 255))

    # Define the sizes for the avatars in each circle
    base_radius = int(35*1.25)  # Radius for avatars in the innermost circle
    center_avatar_size = 150  # Size for the center avatar (radius 70 means diameter 140)
    size_step = 5  # Decrease size by 10 pixels for each layer
    min_avatar_size = 15  # Minimum size to prevent overly small avatars

    # Load and place center avatar
    center_img = load_image_as_circle(center_avatar_url, center_avatar_size // 2, proxies=proxies)
    if center_img:
        center_position = (canvas_size[0] // 2 - center_avatar_size // 2, canvas_size[1] // 2 - center_avatar_size // 2)
        canvas.paste(center_img, center_position, center_img)

    # Sort friends based on their reply_score, highest score first
    sorted_friends = sorted(friends_dict.items(), key=lambda x: x[1]['reply_score'], reverse=True)

    # Plot avatars based on score
    radius_step = 85  # Distance between each circle in pixels
    initial_radius = 140  # Radius for the first circle
    friend_idx = 0
    radius = initial_radius
    layer = 0

    while friend_idx < len(sorted_friends) and layer < 4:
        # Calculate avatar size for this layer (decrease by size_step for each layer)
        avatar_radius = max(base_radius - layer * size_step, min_avatar_size // 2)  # Use radius now
        avatar_size = avatar_radius * 2  # Diameter for resizing

        # Calculate how many avatars fit in the current circle
        num_in_current_circle = int(2 * PI * radius / (avatar_size))  # Adjusted based on avatar size
        theta_step = 2 * PI / num_in_current_circle  # Angle between avatars
        rotation_offset = layer * (PI / 12)  # Rotate 15 degrees for each layer

        for i in range(num_in_current_circle):
            if friend_idx >= len(sorted_friends):
                break  # Stop if no more friends to place

            friend_data = sorted_friends[friend_idx][1]
            avatar_url = friend_data['avatar']
            theta = i * theta_step + rotation_offset  # Apply rotation

            # Calculate avatar position
            x = int(canvas_size[0] // 2 + radius * math.cos(theta) - avatar_radius)  # Center the circle
            y = int(canvas_size[1] // 2 + radius * math.sin(theta) - avatar_radius)

            # Load and place circular avatar
            img = load_image_as_circle(avatar_url, avatar_radius, proxies=proxies)
            if img:
                canvas.paste(img, (x, y), img)

            friend_idx += 1

        # Move to the next circle
        radius += radius_step
        layer += 1
    
    buf = BytesIO()
    canvas.save(buf, format='PNG')
    data = buf.getvalue()
    buf.close()
    return data