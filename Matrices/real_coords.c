#include <stdio.h>
#include <stdarg.h>
#include <math.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>

#define WIDTH       1024
#define HEIGHT      550

#define POINT_CNT  4
SDL_Point triangle[POINT_CNT] = {
    {WIDTH / 2, HEIGHT / 4},
    {WIDTH / 4, HEIGHT * (3.0 / 4.0)},
    {WIDTH * (3.0 / 4.0), HEIGHT * (3.0 / 4.0)},
    {WIDTH / 2, HEIGHT / 4}
};

SDL_Point origin = {0, 0};

typedef struct {
    SDL_Window *window;
    SDL_Renderer *renderer;
    int width;
    int height;
} Canvas;

void transform(SDL_Point origin, SDL_Point triangle[], double matrix[3][3])
{
    int i, j;

    for (i = 0; i < POINT_CNT; i++) {
        // Vypočítaj vektor = B - A
        double v[] = {
            triangle[i].x - origin.x,
            triangle[i].y - origin.y,
            1
        };

        // Aplikuj lineárnu transformáciu
        for (j = 0; j < 3; j++) {
            v[j] =   matrix[j][0] * v[0]
                   + matrix[j][1] * v[1]
                   + matrix[j][2] * v[2];
        }

        // Vráť vektor do priestoru vzhľadom na počiatok
        triangle[i].x = v[0] + origin.x;
        triangle[i].y = v[1] + origin.y;
    }
}

void scale(SDL_Point origin, SDL_Point triangle[], double k)
{
    double matrix[3][3] = {
        {k, 0, 0},
        {0, k, 0},
        {0, 0, 1}
    };
    transform(origin, triangle, matrix);
}

void rotate(SDL_Point origin, SDL_Point triangle[], double angle)
{
    // Radiany -> Stupne
    angle = (3.14159265359 / 180) * angle;
    double matrix[3][3] = {
        {cos(angle), -sin(angle),  0},
        {sin(angle),  cos(angle),  0},
        {         0,           0,  1}
    };
    transform(origin, triangle, matrix);
}

void translate(SDL_Point origin, SDL_Point triangle[], double dx, double dy)
{
    double matrix[3][3] = {
        {1, 0, dx},
        {0, 1, dy},
        {0, 0, 1}
    };
    transform(origin, triangle, matrix);
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

void text_draw(SDL_Renderer *rend, TTF_Font *font, SDL_Point *pos, const char *fmt, ...)
{
    char buffer[256];
    va_list args;
    SDL_Color color = {0, 0, 0, 255};

    va_start(args, fmt);
    vsprintf(buffer, fmt, args);
    va_end(args);

    SDL_Surface *surf = TTF_RenderText_Solid(font, buffer, color);
    SDL_Texture *texture = SDL_CreateTextureFromSurface(rend, surf);

    SDL_Rect dstrect = {pos->x, pos->y, surf->w, surf->h};
    SDL_RenderCopy(rend, texture, NULL, &dstrect);

    SDL_FreeSurface(surf);
    SDL_DestroyTexture(texture);
}

void vertex_draw(SDL_Renderer *rend, TTF_Font *font, SDL_Point *pos, int a)
{
    SDL_Rect point_rect = {pos->x - a / 2, pos->y - a / 2, a, a};
    SDL_RenderFillRect(rend, &point_rect);
    text_draw(rend, font, pos, "[%d; %d]", pos->x, pos->y);
}

void vector_draw(SDL_Renderer *rend, TTF_Font *font, SDL_Point *a, SDL_Point *b)
{
    SDL_RenderDrawLine(rend, a->x, a->y, b->x, b->y);
    SDL_Point draw_pos =  {(a->x + b->x) / 2, (a->y + b->y) / 2};
    SDL_Point v = {b->x - a->x, b->y - a->y};

    text_draw(rend, font, &draw_pos, "v(%d; %d)", v.x, v.y);
}


int main(void)
{
    Canvas c;
    int i;

    if (canvas_init(&c, WIDTH, HEIGHT) < 0) {
        return -1;
    }
    TTF_Font *font = TTF_OpenFont("/home/miroslav/.fonts/Inconsolata.otf", 12);

    SDL_Event event;
    SDL_bool done = SDL_FALSE;

    while (!done) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                done = SDL_TRUE;

            } else if (event.type == SDL_MOUSEBUTTONDOWN) {
                if (event.button.button == SDL_BUTTON_LEFT) {
                    origin.x = event.button.x;
                    origin.y = event.button.y;
                }
            } else if (event.type == SDL_MOUSEWHEEL) {
                if (event.wheel.y == 1)
                    scale(origin, triangle, 1.1);
                else
                    scale(origin, triangle, 0.9);
            } else if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_i)
                    rotate(origin, triangle, 1);
                else if (event.key.keysym.sym == SDLK_o)
                    rotate(origin, triangle, -1);

                else if (event.key.keysym.sym == SDLK_UP)
                    translate(origin, triangle, 0, -10);
                else if (event.key.keysym.sym == SDLK_DOWN)
                    translate(origin, triangle, 0, +10);
                else if (event.key.keysym.sym == SDLK_LEFT)
                    translate(origin, triangle, -10, 0);
                else if (event.key.keysym.sym == SDLK_RIGHT)
                    translate(origin, triangle, +10, 0);

                else if (event.key.keysym.sym == SDLK_PLUS)
                    scale(origin, triangle, 1.1);
                else if (event.key.keysym.sym == SDLK_MINUS)
                    scale(origin, triangle, 0.9);
            }
        }

        SDL_SetRenderDrawColor(c.renderer, 255, 255, 255, 255);
        SDL_RenderClear(c.renderer);

        SDL_SetRenderDrawColor(c.renderer, 0, 0, 0, 255);
        for (i = 0; i < POINT_CNT - 1; i++) {
            vector_draw(c.renderer, font, &triangle[i], &triangle[i + 1]);
            vertex_draw(c.renderer, font, &triangle[i], 5);
        }

        SDL_SetRenderDrawColor(c.renderer, 255, 0, 0, 255);
        vertex_draw(c.renderer, font, &origin, 5);
        for (i = 0; i < 4; i++) {
            SDL_SetRenderDrawColor(c.renderer, 0, 255, 0, 255);
            vector_draw(c.renderer, font, &origin, &triangle[i]);
        }
        SDL_RenderPresent(c.renderer);
        SDL_Delay(30);
    }
    canvas_destroy(&c);
}
