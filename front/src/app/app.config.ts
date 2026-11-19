import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { providePrimeNG } from 'primeng/config';
import { MyPreset } from './mypreset';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './interceptors/auth_interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([authInterceptor])
    ),
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    providePrimeNG({
      license: 'eyJpZCI6ImE3MDUwNWZjLTg5NDEtNDVlMC04ZDJkLWIwNzZiYzUzMGY5NyIsInByb2R1Y3QiOiJwcmltZXVpIiwidGllciI6ImNvbW11bml0eSIsInR5cGUiOiJkZXYiLCJpYXQiOjE3OTMwMDQ4NzYsImV4cCI6MTgyNDU0MDg3Nn0.vQUWlQQ2tVBNi3o9_djERf8Pb-vpIGvE4lreUEa34mzBaQLRhswzHaF8BO_19nBoWcRrQoGNxGdROZyiV32bAA',
      theme: {
          preset: MyPreset,
          options: {
              prefix: 'p',
              darkModeSelector: '.my-app-dark', // important for tailwind to work

              // darkModeSelector: 'light',
              // darkModeSelector: 'dark',
              cssLayer: false,
              // cssLayer: {
              //   name: 'primeng',
              //   order: 'tailwind, app-styles , primeng,',
              // },
              cssVariables: true
          }
      }
    })
  ]
};
