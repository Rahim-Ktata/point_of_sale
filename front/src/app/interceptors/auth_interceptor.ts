import { HttpHandlerFn, HttpRequest } from "@angular/common/http";
import { AuthService } from "../services/auth_service/auth-service";
import { inject } from "@angular/core";


export function authInterceptor(
    req: HttpRequest<unknown>,
    next: HttpHandlerFn
) {
    // Inject the current `AuthService` and use it to get an authentication token:
    const authToken = inject(AuthService).getAuthToken();

    // Skip interceptor logic for auth endpoints (login, register, refresh)
    if (req.url.includes('/auth/login') || req.url.includes('/auth/register') || req.url.includes('/auth/refresh')) {
        return next(req);
        // .pipe(
        //     catchError((error) => {
        //         return throwError(() => error);
        //     })
        // );
    }

    // Clone the request to add the authentication header.
    const newReq = req.clone({
        headers: req.headers.append('Authorization', `Bearer ${authToken}`),
    });

    return next(newReq);
}