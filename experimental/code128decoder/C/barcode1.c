/* CODE128 Barcode Reader                     */
/* Coded by Martin Sarfy <sarfy@ics.muni.cz> on hire for HUDORA GmbH. */
/* Published under a BSD license. */
/* Usage: $ gcc barcode1.c -o barcode1 -ljpeg */
/*        $ ./barcode1 image.jpg              */

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<setjmp.h>
#include<jpeglib.h>

int abs(int a) { return a < 0 ? -a : a; }

int find_barcode(int row,unsigned char *buffer,int stride);

/* ----------------------------------------------------------------------*/
/* JPEG loading code */

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


void read_jpeg(FILE *infile) {
	struct jpeg_decompress_struct cinfo;
	struct my_error_mgr jerr;
	JSAMPARRAY buffer;		/* Output row buffer */
	int row_stride;		    /* physical row width in output buffer */

	cinfo.err = jpeg_std_error(&jerr.pub);
	jerr.pub.error_exit = my_error_exit;
	if (setjmp(jerr.setjmp_buffer)) {
		jpeg_destroy_decompress(&cinfo);
		fclose(infile);
		return;
	}
	jpeg_create_decompress(&cinfo);

	jpeg_stdio_src(&cinfo, infile);
	jpeg_read_header(&cinfo, TRUE);
	jpeg_start_decompress(&cinfo);

	row_stride = cinfo.output_width * cinfo.output_components;
	buffer = (*cinfo.mem->alloc_sarray)
		((j_common_ptr) &cinfo, JPOOL_IMAGE, row_stride, 1);

	while (cinfo.output_scanline < cinfo.output_height) {
    	jpeg_read_scanlines(&cinfo, buffer, 1);
		if(find_barcode(cinfo.output_scanline,buffer[0], row_stride)) break;
	}

	while(cinfo.output_scanline < cinfo.output_height)
    	jpeg_read_scanlines(&cinfo, buffer, 1);

	jpeg_finish_decompress(&cinfo);
	jpeg_destroy_decompress(&cinfo);
}
/* ---------------------------------------------------------------------- */

int main(int argc,char* argv[]) {
	if(argc != 2) 
		{ fprintf(stderr,"\nusage: %s file.jpg\n\n",argv[0]); return 1; }

	FILE *f = fopen(argv[1],"rb");
	if(!f) { perror(argv[1]); return 1; }

	read_jpeg(f);

	return 0;
}

/* --------------------------------------------------------------------- */
/* Algorithms */

int gray(unsigned char* buffer,int i) {
	return (buffer[3*i+0]*0.3 + buffer[3*i+1]*0.59 + buffer[3*i+2]*0.11);
}
int iswhite(unsigned char* buffer,int i) {
	return (buffer[3*i+0]>0x80 && buffer[3*i+1]>0x80 && buffer[3*i+2]>0x80);
}

#define ROW_MAX 10240
int diff_line[ROW_MAX];
#define BLOCK 15
#define THRESHOLD 300
int block_line[ROW_MAX];
int run_line[ROW_MAX];
int gray_line[ROW_MAX];
char bars_line[ROW_MAX];
	
#include "code128.h"

/* save to bars_line[] widths of bars */
/* width units are in coef_a a coef_b */
int process_bars(int x0,int x1,int avg,int coef_a,int coef_b) {
	int run, bar = 0, current = 0;
	int x;

	for(x=x0;x<x1;x++) {
		for(run=0;x+run<=x1&&run<100;run++) {
			if(current  && gray_line[x+run] <  avg) break;
			if(!current && gray_line[x+run] >= avg) break;
		}
		int width = (run+coef_a)/coef_b;
		if(width < 1 || width > 4) return 0;
		bars_line[bar++] = '0'+width;
		x += run; current = !current;
	}
	bars_line[bar] = '\0';
	return bar;
}

/* convert barcode widths to text, as defined in CODE128 standard */
int interpret(char* bar,char output[512]) {
	int  i,j,out[512],outlen = 0;
	int  codeset=0,shifted=0;

	output[0] = '\0';

	// optimalization: check end code now..
	if(strncmp(bar+strlen(bar)-7,"2331112",7)) return 0;

	for(i=0;i<strlen(bar);) {
		char *text,*code;
		for(j=0;j<107;j++) {
			code = code128[4*j+3];
			if(!strncmp(code,bar+i,strlen(code))) break;
		}
		if(j==107) code = NULL;

		int actual = codeset;
		if(shifted) {
			actual = (codeset == 1) ? 2 : 1;
			shifted = 0;
		}
		text = code ? code128[4*j+actual] : "?";

		if(!strncmp(text,"StartA",6)) codeset = 0;
		if(!strncmp(text,"StartB",6)) codeset = 1;
		if(!strncmp(text,"StartC",6)) codeset = 2;
		if(!strncmp(text,"CodeA",5)) codeset = 0;
		if(!strncmp(text,"CodeB",5)) codeset = 1;
		if(!strncmp(text,"CodeC",5)) codeset = 2;
		if(!strncmp(text,"Shift",5)) shifted = 1;
		if(strlen(text) < 4) strncat(output,text,512); 

		out[outlen++] = j;
		if(!i && strncmp(text,"Start",5)) return 0;
		i+= code ? strlen(code) : 6;
	}

	int checksum = 0;
	for(i=0;i<outlen-2;i++) checksum += i ? i*out[i] : out[i];
	if(checksum%103 != out[outlen-2]) return 0;

	output[strlen(output)-1] = '\0';
	return 1;
}

/* read barcode on a given position (x0..x1, line y) */
int read_barcode(unsigned char *b,int x0,int x1,int y) {
	int j,i,x,avg=0,w=0;
	int coef_a,coef_b;
	char output[512];

	/* compute average gray, used to decide whether pixel is white or black */
	avg = 0; 
	for(x=x0;x<x1;x++) avg+=gray(b,x);
	avg /= (x1-x0);

	/* crop starting and closing white "quiet zone" */
	for(x0=x0+3;x0<x1;x0++) if(gray(b,x0) < avg) break;
	for(x1=x1-3;x0<x1;x1--) if(gray(b,x1) < avg) break;

	/* software zoom -- generate new two values between every two pixels */
	for(x=x0;x<x1;x++) {
		gray_line[3*x+0] = gray(b,x);
		gray_line[3*x+1] = 2*gray(b,x)/3 + gray(b,x+1)/3;
		gray_line[3*x+2] = gray(b,x)/3 + 2*gray(b,x+1)/3;
	}
	x0 *= 3; x1 *= 3;

	/* try several widths of barcode, one should match */
	for(coef_b=2;coef_b<=10;coef_b++)
		for(coef_a=0;coef_a<coef_b;coef_a++)
			if(process_bars(x0,x1,avg,coef_a,coef_b))
				if(interpret(bars_line,output)) { 
					printf("%s\n",output);
					return 1;
				}
	return 0;
}


/* does this part of image look as barcode? */
int changes_enough(int x,int length,int req) {
	int i,diffs=0;
	for(i=0;i<length;i++) if(diff_line[x+i] > 30) diffs++;
	return (diffs > req) ? diffs : 0;
}

/* detect barcode on the line and try to read it */
int find_barcode(int row,unsigned char *b,int stride) {
	int j,i,w=stride/3-2;
	int blocks=0,sum,line = 0;
	/* there should be at least 100 edges on line */
	int run,min_run = 100;
	int x,x0,x1; /* starting and closing position */

	/* detect edges on the line and count their number */
	for(i=0;i<w;i++) {
		int diff = abs(gray(b,i+1+1) - gray(b,i+1-1));
		if(diff > 20) line++;
		diff_line[i] = diff;
	}
	/* do not continue, if not enough */
	if(line < min_run) return 0;

	/* find starting and closing position */
	for(x0=25;x0<w-25;x0++) if(changes_enough(x0-15,30,10)) break;
	for(x1=w-25;x1>25;x1--) if(changes_enough(x1-15,30,10)) break;

	/* try to read barcode */
	return read_barcode(b,x0-10,x1+10,row);
}

