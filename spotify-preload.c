// SPDX-License: BSD-3-Clause

#define _GNU_SOURCE
#include <stdlib.h>
#include <dlfcn.h>

static const char *ICON_NAME_OVERRIDE = "com.spotify.Client-symbolic";

/* Electron currently uses app_indicator_set_icon_full() but this covers all options in-case. */

static void (*original_set_icon_full) (void *, const char *, const char *);
static void (*original_set_icon) (void *, const char *);
static void* (*original_indicator_new) (const char *, const char *, int);
static void* (*original_indicator_new_with_path) (const char *, const char *, int, const char*);

void *app_indicator_new (const char *id, const char *icon_name, int category)
{
    if (!original_indicator_new)
        original_indicator_new = dlsym (RTLD_NEXT, "app_indicator_new");

    return original_indicator_new (id, ICON_NAME_OVERRIDE, category);
}

void *app_indicator_new_with_path (const char *id, const char *icon_name, int category, const char *icon_theme_path)
{
    if (!original_indicator_new_with_path)
        original_indicator_new_with_path = dlsym (RTLD_NEXT, "app_indicator_new_with_path");

    return original_indicator_new_with_path (id, ICON_NAME_OVERRIDE, category, NULL);
}

void app_indicator_set_icon (void *indicator, const char *icon_name)
{
    if (!original_set_icon)
        original_set_icon = dlsym (RTLD_NEXT, "app_indicator_set_icon");

    original_set_icon (indicator, ICON_NAME_OVERRIDE);
}

void app_indicator_set_icon_full (void *indicator, const char *icon_name, const char *icon_desc)
{
    if (!original_set_icon_full)
        original_set_icon_full = dlsym (RTLD_NEXT, "app_indicator_set_icon_full");

    original_set_icon_full (indicator, ICON_NAME_OVERRIDE, icon_desc);
}
