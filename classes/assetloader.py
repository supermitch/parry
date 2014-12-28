from __future__ import division
import glob
import json
import os
import sys

import pygame

IMAGE_EXTENSIONS = ('.png', '.gif')
SOUND_EXTENSIONS = ('.wav', '.mid', '.midi')

def extract_base_no_ext(filename):
    """ e.g. 'c:/data/image.png' returns 'image' """
    return os.path.splitext(os.path.basename(filename))[0]

def generate_coords(size, shape):
    """
    Return rect coords for subsurfaces, given size and shape of spritesheet.

    e.g. size = 300 x 100, shape = 8 x 1 (cols x rows)

    """
    if shape is None:
        return [(0, 0, size[0], size[1])]
    cols = size[0] / shape[0]
    rows = size[1] / shape[1]
    top_lefts = [(x * cols, y * rows) for x in range(shape[0]) for y in range(shape[1])]
    coords = [(int(x), int(y), int(cols), int(rows)) for x, y in top_lefts]
    return coords

class AssetLoader(object):
    """
    AssetLoader loads images and sounds, turning them into
    pygame objects (like Surface and Sound) where possible,
    accessible by dictionary key of 'name'. Additional information
    can be defined in attribute JSON files.

    """

    def __init__(self, folder=None, scale=1):
        """ If a folder is defined, look there, else we'll assume. """
        if folder is not None:
            self.root = folder
        else:
            self.root = os.path.join(
                            os.path.dirname(os.path.realpath(__file__)), '..')
        self.image_scaling = scale  # How to rescale images
        self.images = self.load_images()
        self.sounds = self.load_sounds()

    @property
    def assets(self):
        """ Return an (images, sounds) tuple. """
        return self.images, self.sounds

    def load_images(self):
        """ Load images from all sub-dirs in root. """
        folder = os.path.join(self.root, 'images')
        attrib_data = self.__load_attrs(folder)

        images = {}
        for f in os.listdir(folder):
            if f.lower().endswith(IMAGE_EXTENSIONS):
                f_name = extract_base_no_ext(f)
                f_full = os.path.join(folder, f)

                attrs = attrib_data.get(f_name, {})
                # Extract default values from attributes for this file
                kind = attrs.get('kind', 'sprite')
                name = attrs.get('name', f_name)
                coords = attrs.get('coords', None)
                shape = attrs.get('shape', None)

                if kind == 'sprite':
                    sprite = pygame.image.load(f_full).convert_alpha()
                    size = tuple(int(x * self.image_scaling) \
                                 for x in sprite.get_size())
                    sprite = pygame.transform.scale(sprite, size)

                elif kind == 'spritesheet':
                    sheet = pygame.image.load(f_full).convert_alpha()
                    if coords is None:  # Use shape, e.g. 8 x 1
                        coords = generate_coords(sheet.get_size(), shape)
                    sprite = [sheet.subsurface(coord) for coord in coords]
                    size = tuple(int(x * self.image_scaling) \
                                 for x in sprite[0].get_size())
                    sprite = [pygame.transform.scale(x, size) for \
                              x in sprite]

                if name in images:
                    print('Image asset name collision! {}'.format(name))
                images[name] = sprite
        return images


    def load_sounds(self):
        """ Load sounds from all sub-dirs in root. """
        folder = os.path.join(self.root, 'sounds')
        attrib_data = self.__load_attrs(folder)

        pygame.mixer.set_num_channels(12)

        sounds = {}
        for f in os.listdir(folder):
            if f.lower().endswith(SOUND_EXTENSIONS):
                f_name = extract_base_no_ext(f)
                f_full = os.path.join(folder, f)

                attrs = attrib_data.get(f_name, {})
                # Extract default attrs from attributes for this file
                # Default is sound named after file w/ volume 1.0
                kind = attrs.get('kind', 'sound')
                name = attrs.get('name', f_name)
                volume = attrs.get('volume', 1.0)
                loops = attrs.get('loops', -1)
                start = attrs.get('start', 0.0)

                if name in sounds:
                    print('Sound asset name collision! {}'.format(name))
                if kind == 'sound':
                    sounds[name] = pygame.mixer.Sound(f_full)
                    sounds[name].set_volume(volume)
                elif kind == 'music':
                    # Save details as tuple for later streaming playblack.
                    sounds[name] = (f_full, loops, start)

        return sounds

    def __load_attrs(self, folder):
        """ Load JSON attributes from the given folder. """
        f_name = os.path.join(folder, 'attrs.json')
        try:
            with open(f_name, 'r') as f:
                return json.load(f)
        except (AttributeError, ValueError):
            print('Bad JSON in attribs: {}'.format(f_name))
            return None
        except IOError:
            return None

