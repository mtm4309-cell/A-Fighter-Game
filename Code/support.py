from csv import reader
import os
from os import walk
import pygame

_image_cache = {} 
_sound_cache = {}

# The two variables hold assets that have been loaded for the game UI, such as backgrounds and buttons. These assets are not part of the main game assets but are essential for the user interface.

_GAME_UI_IMAGES = (
    "UI related/BACKGROUNDS/when_not_running.png",
    "UI related/BACKGROUNDS/when_running.png",
    "UI related/BACKGROUNDS/level_template.png",
    "UI related/BUTTONS/blue_blast_button_not_selected.png",
    "UI related/BUTTONS/blue_blast_button_selected.png",
    "UI related/BUTTONS/purple_blast_button_not_selected.png",
    "UI related/BUTTONS/purple_blast_button_selected.png",
)

_IMAGE_EXTENSIONS = {".bmp", ".jpeg", ".jpg", ".png"}
_SOUND_EXTENSIONS = {".mp3", ".ogg", ".wav"}


def _cache_key(path): # This function generates a normalized cache key for the given file path. It ensures that the path is in a consistent format, which helps in caching and retrieving assets efficiently.
    return os.path.normcase(os.path.normpath(path))


def load_image(path): # This function loads an image from the specified path and caches it for future use. If the image has already been loaded, it retrieves it from the cache instead of loading it again, which improves performance.
    key = _cache_key(path)
    if key not in _image_cache:
        _image_cache[key] = pygame.image.load(path).convert_alpha()
    return _image_cache[key]


def load_sound(path): # This function loads a sound from the specified path and caches it for future use. If the sound has already been loaded, it retrieves it from the cache instead of loading it again, which improves performance.
    key = _cache_key(path)
    if key not in _sound_cache:
        _sound_cache[key] = pygame.mixer.Sound(path)
    return _sound_cache[key]


def game_asset_paths(): # This function returns a list of all the game asset paths (images and sounds) that need to be loaded.
    paths = []
    for folder in ("Sprites", "Sound Effects"):
        for root, directories, filenames in walk(folder):
            directories.sort()
            for filename in sorted(filenames):
                extension = os.path.splitext(filename)[1].lower()
                supported_extensions = (
                    _IMAGE_EXTENSIONS if folder == "Sprites" else _SOUND_EXTENSIONS
                )
                if extension in supported_extensions:
                    paths.append(os.path.join(root, filename))

    paths.extend(_GAME_UI_IMAGES) # Adding the UI images to the list of asset paths to ensure they are loaded as well.
    paths.append("UI related/BACKGROUNDS/arena.png") # Adding the arena background to the list of asset paths to ensure it is loaded as well.
    return paths


def load_game_asset(path): # This function loads a game asset (image or sound) based on its file extension. It uses the appropriate loading function (load_image or load_sound) depending on whether the asset is an image or a sound.
    if os.path.splitext(path)[1].lower() in _SOUND_EXTENSIONS:
        load_sound(path)
    else:
        load_image(path)


def import_csv_layout(path): # Not used in this game, but is there when necessary
    terrain_map = [] 
    with open(path) as level_map:
        layout = reader(level_map,delimiter= ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path): # This function imports all image files from a specified folder and returns them as a list of Pygame surfaces. It uses the load_image function to load each image and store it in a list, which is then returned for use in animations or other purposes.
    surface_list = []
    
    for _,__,img_file in walk(path):
        for image in img_file:
            full_path = os.path.join(path, image)
            image_surf = load_image(full_path)
            surface_list.append(image_surf)
    return surface_list
