init -1000 python in SSSSS:
    class ImagePlaceholder(renpy.display.core.Displayable):
        def __init__(self, width=0, height=0, **properties):
            super(ImagePlaceholder, self).__init__(**properties)

            self.width = width
            self.height = height

        def render(self, width, height, st, at):
            return renpy.display.render.Render(self.width, self.height)

    class Image(renpy.display.core.Displayable):
        def __init__(self, surface, width, height, fitAfterResize=False, **properties):
            super(Image, self).__init__(**properties)
            self.width = width
            self.height = height
            self.surface = surface
            self.fitAfterResize = fitAfterResize # Fits the bounds to the new size instead of using provided width and height

        def render(self, width, height, st, at):
            surface = self.surface

            sw, sh = surface.get_size()
            w, h = self.scale(surface, (self.width, self.height))

            # Render the image in its original size
            rv = renpy.display.render.Render(sw, sh)
            rv.blit(surface, (0, 0))
 
            # Scale it down to the desired size based on width and height arguments
            try:
                renpy.display.render.blit_lock.acquire()
                surface = renpy.display.scale.smoothscale(surface, (w, h))
            finally:
                renpy.display.render.blit_lock.release()

            cw, ch = surface.get_size()

            if self.fitAfterResize:
                self.width = cw
                self.height = ch

            # Create a new render for the scaled down image and return that
            nrv = renpy.display.render.Render(self.width, self.height)
            nrv.blit(surface, (0, 0))

            return nrv

        def scale(self, image, desired_size):
            original_size=image.get_size()

            # Extract dimensions
            desired_width, desired_height = desired_size
            original_width, original_height = original_size

            # Calculate scaling factors for width and height
            width_scaling = float(desired_width) / float(original_width)
            height_scaling = float(desired_height) / float(original_height)

            # Choose the minimum scaling factor to fit the entire image
            scaling_factor = min(width_scaling, height_scaling)

            # Calculate adjusted image size
            new_width = original_width * scaling_factor
            new_height = original_height * scaling_factor

            return int(new_width), int(new_height)

    class Utils():
        @staticmethod
        def splitSavename(save_name):
            page, slot = save_name.split('-')

            return page, slot

        @staticmethod
        def getSortedSaves():
            regexp = r'\d+' + '-' + r'\d+'
            return Utils.sortSaves(renpy.list_slots(regexp=regexp))

        @staticmethod
        def sortSaves(saves_list):
            return sorted(saves_list, key=Utils.__custom_saves_sort)
        
        @staticmethod
        def __custom_saves_sort(save_name):
            page, slot = Utils.splitSavename(save_name)
            return int(page), int(slot)