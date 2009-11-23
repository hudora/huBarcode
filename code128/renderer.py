"""Rendering code for code128 barcode"""

__revision__ = "$Revision: 1$"

import Image, ImageFont, ImageDraw
import logging, os

log = logging.getLogger( "code128" )

# maps bar width against font size
font_sizes = \
{
    1: 8,
    2: 14,
    3: 18,
    4: 24
}


class Code128Renderer:
    """Rendering class for code128 - given the bars and the original
    text, it will render an image of the barcode, including edge 
    zones and text."""
    
    def __init__( self, bars, text ):
        self.bars = bars
        self.text = text


    def write_file( self, filename, bar_width ):
        """Write barcode data out to image file
        filename - the name of the image file or an file object
        bar_width - the desired width in pixels of each bar"""
        
        # 11 bars per character, plus the stop
        num_bars = len(self.bars)

        log.debug( "There are %d bars", num_bars )

        # Quiet zone is 10 bar widths on each side
        quiet_width = bar_width * 10

        # Total image width
        image_width = (2 * quiet_width) + (num_bars * bar_width)

        # Image height 30% of width
        image_height = image_width / 3 

        log.debug( "Image is %d x %d", image_width, image_height )

        # Image: has a white background
        img = Image.new( 'L', (image_width, image_height), 255 )

        class BarWriter:
            """Class which moves across the image, writing out bars""" 
            def __init__(self, img):
                self.img = img
                self.current_x = quiet_width
                self.symbol_top = quiet_width / 2

            def write_bar( self, value, full=False ):
                """Draw a bar at the current position,
                if the value is 1, otherwise move on silently"""

                # only write anything to the image if bar value is 1
                bar_height = int( image_height * (full and 0.9 or 0.8) )
                if value == 1:
                    for ypos in range(self.symbol_top, bar_height):
                        for xpos in range(self.current_x, \
                                            self.current_x+bar_width):
                            img.putpixel( (xpos, ypos), 0 )
                self.current_x += bar_width

            def write_bars( self, bars, full=False ):
                """write all bars to the image"""
                for bar in bars:
                    self.write_bar( int(bar), full )


        writer = BarWriter( img )
        writer.write_bars( self.bars )

        # Draw the text
        font_size = font_sizes.get(bar_width, 24)
            
        # Locate the font file relative to the module
        c128dir, _ = os.path.split( __file__ )
        rootdir, _ = os.path.split( c128dir )  
        fontfile = os.path.join( rootdir, "fonts", 
                                "courR%02d.pil" % font_size )
        font = ImageFont.load_path( fontfile )
        draw = ImageDraw.Draw( img )

        xtextwidth = len(self.text) * font_size  
        xtextpos = image_width/2 - (xtextwidth/2)
        draw.text( (xtextpos, int(image_height*.8)), 
                    self.text, font=font )

        img.save( filename, 'PNG')
