/* CODE128 Barcode Reader                     */
/* Coded by Martin Sarfy <sarfy@ics.muni.cz> on hire for HUDORA GmbH. */
/* Published under a BSD license. */
/* Usage: $ gcc barcode2.c -o barcode1 -ljpeg */
/*        $ ./barcode2 image.jpg              */

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<setjmp.h>
#include<jpeglib.h>

#include"code128.h"

/* ========= Constants --------- */
#define MAX 1024
int image[MAX][MAX];
int image_maxx,image_maxy;

#define BAR_MAX 1024

#define CONTRAST 5
#define ZOOM 8

#define HISTO_MAX (ZOOM*32)
static int histo[HISTO_MAX],histo_max=0;

// fixme: alloc space for whole image
int row[MAX*ZOOM][MAX];
//int *row[MAX]; ... ; row = malloc(..) ?
int row_maxx=0,row_maxy=0;

int abs(int a) { return a < 0 ? -a : a; }

/* ========= Image dump for debugging ---------- */
int output[ZOOM*MAX][MAX];
int output_maxx,output_maxy;

void printbar(int val) {
	if(val>155) val = 155;
	while(val--) printf("@");
	printf("\n");
}

void output_write(char* filename) {
    int x,y;
    FILE* pgm = fopen(filename,"wb");
	printf("writing %dx%d image to %s\n",output_maxx,output_maxy,filename);
    fprintf(pgm,"P5\n%d %d\n255\n",output_maxx,output_maxy);
    for(y=0;y<output_maxy;y++)
        for(x=0;x<output_maxx;x++)
            fputc(output[x][y],pgm);
    fclose(pgm);
}

/* compute widths in pixels of bars in image row */
int wave_widths(int *bar,int y) {
	int x, width = 0, bars = 0;

	/* compute average gray value */
	int avg = 0;
    for(x=0;x<row_maxx;x++) avg+=row[x][y];
    avg /= row_maxx;

	if(row[0][y]>=avg) bar[bars++] = 0; // add starting white, if needed
	for(x=0;x<row_maxx-1;x++) {
		if((row[x][y]<avg && row[x+1][y]>=avg) || 
		   (row[x][y]>=avg && row[x+1][y]<avg))
				bar[bars++] = width, width = 0;
		width++;
	}
	return bars;
}

int histogram(int y,int x0,int x1,int y0,int y1) {
	int i,x;
	int mx = x1-x0;
	int adjusted[mx];

	int min[mx], max[mx];
	for(x=0;x<mx;x++) {
		/* compute minimum and maximum of 2*CONTRAST pixels around x */
		int minx = x-CONTRAST, maxx = x+CONTRAST;
		if(minx<0)  minx = 0, maxx = 2*CONTRAST;
		if(maxx>mx) minx = mx-2*CONTRAST, maxx = mx;

		int min_level = 255, max_level = 0;
		for(i=minx;i<maxx-1;i++) {
			int level = (image[x0+i][y]+image[x0+i+1][y])/2;
			if(level < min_level) min_level = level;
			if(level > max_level) max_level = level;
		}
		min[x] = min_level, max[x] = max_level;
	}

	/* improve contrast using stretching by adjacent pixels */
	for(x=0;x<mx;x++) {	
		int delta = (max[x]-min[x]);
		if(delta < 1) delta = 1; // sanity check
		int level = 256*(image[x0+x][y]-min[x])/delta;
		if(level < 0) level = 0; if(level > 255) level = 255;
		adjusted[x] = 255-level;
	}

	if(row_maxx != mx*ZOOM-1) exit(18); // sanity check

	/* software zoom (ZOOM-times) -- linear interpolation */
	for(x=0;x<mx-1;x++) {	
		for(i=0;i<ZOOM;i++)
			row[ZOOM*x+i][y-y0] = 
//					(ZOOM-i)*image[x][y]/ZOOM+i*image[x+1][y]/ZOOM;
					(ZOOM-i)*adjusted[x]/ZOOM+i*adjusted[x+1]/ZOOM;
	}

	int bar[row_maxx];
	int bars = wave_widths(bar,y-y0);

	for(i=0;i<bars;i++) if(bar[i]<HISTO_MAX) 
		{ histo[bar[i]]++; if(bar[i] > histo_max) histo_max = bar[i]+1; }

	return bars;
}


/* locate continously high values in array, with at least w width */
int locate_hill(int ary[],int ary_length,int blur,int w,int *start,int *stop) {
	int i,j,max = 0;
	int blurred[ary_length];

	int maxh = 0;
	for(i=0;i<ary_length;i++) {
		int value = 0;
		for(j=i-blur;j<i+blur+1;j++) value += ary[(ary_length+j)%ary_length];
		blurred[i] = value/(blur+1+blur);
		if(blurred[i]>maxh) maxh = blurred[i];
	}

	for(i=blur+1;i<ary_length-blur;i++) {
		if(blurred[i-1]<=maxh/8 && blurred[i]>maxh/8) {
			int length = 0, volume = 0;
			for(;i<ary_length && blurred[i]>=maxh/8;i++) 
				length++, volume += blurred[i]; 
			if(length > w && max<volume) 
				max = volume, *start = i-length+1, *stop = i;
		}
	}
	return max;
}

/* find bounding box of a barcode */
int locate(int *x0,int *y0,int *x1,int *y1) {
	int x,y,i;
	int yline[image_maxy];
	int xline[image_maxx];

	/* rate edges on a line, number and their distance */
	for(y=0;y<image_maxy;y++) {
		int line=0, last = 0;
		for(x=1;x<image_maxx-1;x++) {
			int diff = abs(image[x-1][y] - image[x+1][y]);
			if(diff > 20) line += diff/(x-last), last = x;
		}
		yline[y] = line;
	}
	
	/* find range of lines with maximum rates */
	if(!locate_hill(yline,image_maxy,1,20,y0,y1)) {
		fprintf(stderr,"barcode not found (on y-axis)\n"); return 0;
	}

	/* rate vertical lines, find columns with black-white interface */
	xline[0] = xline[image_maxx-1] = 0;
	for(x=1;x<image_maxx-1;x++) {
		int sum = 0;
		for(y=*y0+1;y<*y1;y++) {
			/* add lengths of edges on vertical line */
			int d0 = abs(image[x-1][y-1] - image[x+1][y-1]);
			int d1 = abs(image[x-1][y]   - image[x+1][y]);
			sum += d0*d1;
		}
		xline[x] = sum;
	}

	/* find range of columns with maximum rates */
	if(!locate_hill(xline,image_maxx,6,200,x0,x1)) {
		fprintf(stderr,"barcode not found (on x-axis)\n"); return 0;
	}
	return 1;
}

/* from histogram of bars widths [in pixels] compute unit width */
int get_width(int delta,int *histo,int histo_max) {
	int i,width=0;
	for(i=0;i<histo_max;i++) if(histo[i] > delta) width = i;
	for(;width<histo_max;width++) 
		if(histo[width+1] >= histo[width]) break;
	return width;
//	for(i=0;i<histo_max;i++) if(histo[i]>max) max = histo[i];
//	for(i=1;i<histo_max;i++) if(i<50 || histo[i])
//		{ printf("%3d %4d ",i,histo[i]); printbar(160*histo[i]/max); }
}

/* measure barcode widths (1..4) */
int measure(int y,int width4,char *bar) {
	int i,wave[row_maxx];
	int waves = wave_widths(wave,y);
	int bars=0;

	for(i=0;i<waves;i++) {
		int w = wave[i]; // skip bar, if its too small
		if(i<waves-1 && wave[i+1]<width4/4)
			w += wave[i+1] + wave[i+2], i+=2;
		int type = w/(width4/4);
		if(type<0 || type>4) continue;
		if(i) bar[bars++] = '0'+type; // strip first bar
	}
	if(!(bars%2)) bars--; // strip closing bar, if it's white
	bar[bars] = '\0';
	printf("bars: %s\n",bar);
	return bars;
}

/* convert barcode widths to text, as defined in CODE128 standard */
int interpret(int y,char *bar,int code[BAR_MAX],char text[BAR_MAX]) {
	int i,j,out[512],codes = 0;
	int codeset=0,shifted=0;
	int bars = strlen(bar);

	text[0] = '\0';

	// optimalization: check end code now..
	if(strncmp(bar+bars-7,"2331112",7)) return 0;

	for(i=0;i<bars;) {
		// find value
		char *this_text,*this_code;
		for(j=0;j<107;j++) {
			this_code = code128[4*j+3];
			if(!strncmp(this_code,bar+i,strlen(this_code))) break;
		}
		if(j==107) j==-1, this_code = NULL;
		code[codes++] = j;

		int actual = codeset;
		if(shifted) actual = (codeset == 1) ? 2 : 1, shifted = 0;
		this_text = this_code ? code128[4*j+actual] : "?";

		if(!strncmp(this_text,"StartA",6)) codeset = 0;
		if(!strncmp(this_text,"StartB",6)) codeset = 1;
		if(!strncmp(this_text,"StartC",6)) codeset = 2;
		if(!strncmp(this_text,"CodeA",5)) codeset = 0;
		if(!strncmp(this_text,"CodeB",5)) codeset = 1;
		if(!strncmp(this_text,"CodeC",5)) codeset = 2;
		if(!strncmp(this_text,"Shift",5)) shifted = 1;
		if(strlen(this_text) < 4) strncat(text,this_text,BAR_MAX); 
		if(!i && strncmp(this_text,"Start",5)) return 0;
		i+= this_code ? strlen(this_code) : 6;
	}

	/* compute and verify checksum */
	int checksum = 0;
	for(i=0;i<codes-2;i++) checksum += i ? i*code[i] : code[i];
	if(checksum%103 != code[codes-2]) 
		printf("checksum failed for [%s] %d != %d\n",
			   text,checksum%103,code[codes-2]);
	if((codes < 3) || (checksum%103 != code[codes-2])) return 0;

	text[strlen(text)-1] = '\0'; // strip checksum and stop char
	printf("%s\n",text);
	return 1;
}

/* main algorithm */
void barcode() {
	int i,max=0,y,x0,y0,x1,y1;

	/* locate bounding box of barcode */
	if(!locate(&x0,&y0,&x1,&y1)) return;
	printf("bounding box: [%d,%d]-[%d,%d]\n",x0,y0,x1,y1);

	/* compute histogram of bars widths */
	/* and store scaled and adjusted image to row[][] array */
	row_maxx = (x1-x0)*ZOOM-1;
	row_maxy = y1-y0;
	for(y=y0;y<y1;y++) histogram(y,x0,x1,y0,y1);

	/* find-out unit width of barcode (average whole barcode) */
	int width4 = get_width((y1-y0)/4,histo,histo_max);
	printf("widths: %d - %d - %d - %d\n",width4/4,width4/2,3*width4/4,width4);

	int coef_a, coef_b;

	/* well, not used -- try several widths in brutal-force way */
	for(y=0;y<row_maxy;y++) {
		char bar[BAR_MAX],bars;
		char text[BAR_MAX];
		int  code[BAR_MAX];
		/* measure bar widths and interpret barcode */
		bars = measure(y,width4,bar);
		if(bars) interpret(y,bar,code,text);
	}
}

/* ----------------------------------------------------------------------*/
/* JPEG handing and picture adjusting */

int to_level(unsigned char* buffer,int i) {
    int level = (buffer[3*i+0]*0.3 + buffer[3*i+1]*0.59 + buffer[3*i+2]*0.11);
    return level > 255 ? 255 : level;
}

char* add_to_image(int row,unsigned char *b,int w) {
    int i;
    for(i=0;i<w;i++) image[i][row] = to_level(b,i);
}

struct my_error_mgr {
  struct jpeg_error_mgr pub;	/* "public" fields */
  jmp_buf setjmp_buffer;	/* for return to caller */
};
typedef struct my_error_mgr * my_error_ptr;

void my_error_exit (j_common_ptr cinfo) {
  my_error_ptr myerr = (my_error_ptr) cinfo->err;
  (*cinfo->err->output_message) (cinfo);
  longjmp(myerr->setjmp_buffer, 1);
}


int read_jpeg(FILE *infile) {
	struct jpeg_decompress_struct cinfo;
	struct my_error_mgr jerr;
	int i,y;
	JSAMPARRAY buffer;		/* Output row buffer */
	int row_stride;		/* physical row width in output buffer */

	cinfo.err = jpeg_std_error(&jerr.pub);
	jerr.pub.error_exit = my_error_exit;
	if (setjmp(jerr.setjmp_buffer)) {
		jpeg_destroy_decompress(&cinfo);
		fclose(infile);
		return 0;
	}
	jpeg_create_decompress(&cinfo);

	jpeg_stdio_src(&cinfo, infile);
	jpeg_read_header(&cinfo, TRUE);
	jpeg_start_decompress(&cinfo);

	row_stride = cinfo.output_width * cinfo.output_components;
	buffer = (*cinfo.mem->alloc_sarray)
		((j_common_ptr) &cinfo, JPOOL_IMAGE, row_stride, 1);

	image_maxx = cinfo.output_width;
	image_maxy = 0;

	while (cinfo.output_scanline < cinfo.output_height) {
    	jpeg_read_scanlines(&cinfo, buffer, 1);
		add_to_image(image_maxy++,buffer[0], image_maxx);
	}

	jpeg_finish_decompress(&cinfo);
	jpeg_destroy_decompress(&cinfo);
	return 1;
}
/* ----------------------------------------------------------------------*/

int main(int argc,char* argv[]) {
	int i,max=0;
	
	if(argc != 2) 
		{ fprintf(stderr,"\nusage: %s file.jpg\n\n",argv[0]); return 1; }

	FILE *f = fopen(argv[1],"rb");
	if(!f) { perror(argv[1]); return 1; }

	read_jpeg(f);
	barcode();
	return 0;
}

