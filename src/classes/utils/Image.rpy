init -9999 python in JK:
    _constant = True

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
            return Utils.resize_dimensions_to_limits(image.get_size(), desired_size)

        # ==============
        # STATIC METHODS
        # ==============

        @staticmethod
        def get_limited_image_size_with_preserved_aspect_ratio(desired_width, desired_height):
            # Get the aspect ratio from Ren'Py's screen configuration
            original_width = renpy.config.thumbnail_width or 1 if hasattr(renpy.config, "thumbnail_width") else 1
            original_height = renpy.config.thumbnail_height or 1 if hasattr(renpy.config, "thumbnail_height") else 1

            return Utils.resize_dimensions_to_limits((original_width, original_height), (desired_width, desired_height))