#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_STACK_SIZE 1e9
int stack[(int)MAX_STACK_SIZE];
int stack_index = 0;


int xs[8] = {1, 1, 0, -1, -1, -1, 0, 1};
int ys[8] = {0, 1, 1, 1, 0, -1, -1, -1};

int chaine_index = 0;
// 3 2 1
// 4 X 0
// 5 6 7

void makeChain(int* image, int16_t* freeman, int x, int y, int w, int h) {
	stack[stack_index++] = x;
	stack[stack_index++] = y;
	int xd, yd;
	int sx, sy;
	int i;
	
	while(stack_index) {
		yd = stack[--stack_index];
		xd = stack[--stack_index];

		image[yd * w + xd] = 0;
		
		for(i = 0; i < 8; i++){
			sx = xd + xs[i];
			sy = yd + ys[i];
			
			if(sx < w && sx >= 0 && sy < h && sy >= 0 && image[sy * w + sx] == 255){
				stack[stack_index++] = xd + xs[i];
				stack[stack_index++] = yd + ys[i];
				freeman[chaine_index++] = i;
				break;
			}
		}
	}
}

int freeman(int* image, int16_t* freeman, int w, int h, int direct) {
	chaine_index = 0;
	int i, j;
	
	for(i = 0; i < w; i++)
	for(j = 0; j < h; j++){
		if(image[j * w + i] == 255){

			if(direct == 0){
				freeman[chaine_index++] = -1;
				freeman[chaine_index++] = i;
				freeman[chaine_index++] = j;
			}

			makeChain(image, freeman, i, j, w, h);
		}
	}

	return chaine_index;
}