// gcc --std=c99 linear_transform.c -lSDL2 -lSDL2_ttf -lSDL2_gfx -lm -o demo
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <math.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL2_gfxPrimitives.h>

typedef struct {
    SDL_Window *window;
    SDL_Renderer *renderer;
    int width;
    int height;
} Canvas;

typedef struct {
    double x, y, z;
} Vector;

typedef Vector Matrix[3];

typedef struct {
    Vector v[4096];
    int n;
} Mesh;

typedef struct {
    int w, h;
    int xrange;
    int yrange;
} Viewport;


void transform(Matrix matrix, Mesh *vertices)
{
    for (int i = 0; i < vertices->n; i++) {
        Vector v = {vertices->v[i].x, vertices->v[i].y, 1};

        v.x = matrix[0].x * v.x + matrix[0].y * v.y + matrix[0].z * v.z;
        v.y = matrix[1].x * v.x + matrix[1].y * v.y + matrix[1].z * v.z;
        v.z = matrix[2].x * v.x + matrix[2].y * v.y + matrix[2].z * v.z;

        vertices->v[i].x = v.x;
        vertices->v[i].y = v.y;
    }
}

void scale(Mesh *v, double k)
{
    Matrix m = {
        {k, 0, 0},
        {0, k, 0},
        {0, 0, 1}
    };
    transform(m, v);
}

#define to_radians(X) ((3.14159265359 / 180.0) * (X))

void rotate(Mesh *v, double angle)
{
    angle = to_radians(angle);
    Matrix m = {
        {cos(angle), -sin(angle),  0},
        {sin(angle),  cos(angle),  0},
        {         0,           0,  1}
    };
    transform(m, v);
}

void translate(Mesh *v, double dx, double dy)
{
    Matrix m = {
        {1, 0, dx},
        {0, 1, dy},
        {0, 0, 1}
    };
    transform(m, v);
}

void viewport(Mesh *view, Mesh *src, Viewport *port)
{
    Matrix m = {
        {port->w / (2 * port->xrange),                   0,  port->w / 2},
        {                  0, -port->h / (2 * port->xrange),  port->h / 2},
        {                  0,                            0,            1}
    };
    memcpy(view, src, sizeof(Mesh));
    transform(m, view);
}



int canvas_init(Canvas *canvas, int width, int height)
{
    if (SDL_Init(SDL_INIT_EVERYTHING) < 0) {
        printf("Chyba pri načítavaní SDL: %s\n", SDL_GetError());
        return -1;
    }

    if (TTF_Init() < 0) {
        printf("Chyba pri subsystéme fontov: %s\n", SDL_GetError());
        return -1;
    }

    canvas->window = SDL_CreateWindow("Lineárne transformácie",
                              0, 0, width, height, 0);
    if (canvas->window == NULL) {
        printf("Chyba pri otváraní okna: %s\n", SDL_GetError());
        return -1;
    }

    canvas->renderer = SDL_CreateRenderer(canvas->window, -1, SDL_RENDERER_ACCELERATED);
    if (canvas->renderer == NULL) {
        printf("Chyba pri vytváraní vykreslovača: %s\n", SDL_GetError());
        return -1;
    }
    SDL_RenderSetLogicalSize(canvas->renderer, width, height);
    canvas->width = width;
    canvas->height = height;

    return 0;
}

void canvas_destroy(Canvas *canvas)
{
    SDL_DestroyRenderer(canvas->renderer);
    SDL_DestroyWindow(canvas->window);
    SDL_Quit();
}

void text_draw(Canvas *c, TTF_Font *font, Vector *pos, const char *fmt, ...)
{
    char buffer[256];
    va_list args;
    SDL_Color color = {0, 0, 0, 255};

    va_start(args, fmt);
    vsprintf(buffer, fmt, args);
    va_end(args);

    SDL_Surface *surf = TTF_RenderText_Solid(font, buffer, color);
    SDL_Texture *texture = SDL_CreateTextureFromSurface(c->renderer, surf);

    SDL_Point text_pos = {pos->x, pos->y};
    SDL_Rect dstrect = {text_pos.x, text_pos.y, surf->w, surf->h};
    SDL_RenderCopy(c->renderer, texture, NULL, &dstrect);

    SDL_FreeSurface(surf);
    SDL_DestroyTexture(texture);
}

void grid_draw(Canvas *c, Mesh *g)
{
    int x, y;
    for (x = g->v[0].x; x <= g->v[1].x; x += (g->v[1].x - g->v[0].x) / 20) {
        thickLineRGBA(c->renderer, x, g->v[0].y, x, g->v[1].y, 1, 0, 0, 0, 50);
    }

    for (y = g->v[0].y; y <= g->v[1].y; y += (g->v[1].y - g->v[0].y) / 20) {
        thickLineRGBA(c->renderer, g->v[0].x, y, g->v[1].x, y, 1, 0, 0, 0, 50);
    }

    filledCircleRGBA(c->renderer, g->v[2].x, g->v[2].y, 4, 0, 0, 0, 255);
}


int main(void)
{
    Canvas c;
    Viewport display = {
        .w = 1024,
        .h = 550,
        .xrange = 10,
        .yrange = 10
    };

    Mesh grid = {
        .v = {
            {-display.xrange,   display.yrange},  //upper-left corner
            { display.xrange,  -display.yrange},  //lower-right corner
            {              0,                0}   // origin
        },
        .n = 3
    };

    Mesh polygon = {
        .v = {
            { 0,  5},
            {-5, -5},
            { 5, -5},
        },
        .n = 3
    };

    if (canvas_init(&c, display.w, display.h) < 0) {
        return -1;
    }

    TTF_Font *font = TTF_OpenFont("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14);
    SDL_Event event;
    SDL_bool done = SDL_FALSE;

    while (!done) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                done = SDL_TRUE;

            } else if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_i)
                    rotate(&polygon, 1);
                else if (event.key.keysym.sym == SDLK_o)
                    rotate(&polygon, -1);

                else if (event.key.keysym.sym == SDLK_UP)
                    translate(&polygon, 0, 1);
                else if (event.key.keysym.sym == SDLK_DOWN)
                    translate(&polygon, 0, -1);
                else if (event.key.keysym.sym == SDLK_LEFT)
                    translate(&polygon, -1, 0);
                else if (event.key.keysym.sym == SDLK_RIGHT)
                    translate(&polygon, 1, 0);

                else if (event.key.keysym.sym == SDLK_PLUS)
                    scale(&polygon, 1.1);
                else if (event.key.keysym.sym == SDLK_MINUS)
                    scale(&polygon, 0.9);
            }
        }

        SDL_SetRenderDrawColor(c.renderer, 255, 255, 255, 255);
        SDL_RenderClear(c.renderer);
        Mesh g;
        viewport(&g, &grid, &display);
        grid_draw(&c, &g);


        Mesh p;
        viewport(&p, &polygon, &display);

        for (int i = 0; i < p.n; i++) {
            int i_next = (i + 1) % p.n;
            thickLineRGBA(c.renderer, p.v[i].x, p.v[i].y,
                                      p.v[i_next].x, p.v[i_next].y,
                                      2, 0, 0, 255, 200);
            SDL_SetRenderDrawColor(c.renderer, 0, 0, 0, 255);
            text_draw(&c, font, &p.v[i], "[%.1f; %.1f]", polygon.v[i].x, polygon.v[i].y);


            Vector label_pos = {(p.v[i].x + p.v[i_next].x) / 2,
                                   (p.v[i].y + p.v[i_next].y) / 2};
            Vector v = {polygon.v[i_next].x - polygon.v[i].x,
                          polygon.v[i_next].y - polygon.v[i].y};
            text_draw(&c, font, &label_pos, "v(%.1f; %.1f)", v.x, v.y);
            filledCircleRGBA(c.renderer, p.v[i].x, p.v[i].y, 4, 255, 0, 0, 255);
        }

        SDL_RenderPresent(c.renderer);
        SDL_Delay(30);
    }
    canvas_destroy(&c);
}
