Setup:
npm install -g @angular/cli
ng new student-portal-angular --routing --style=css
cd student-portal-angular

Copy this folder's src/app/*.ts files into your project's src/app/.
Add <router-outlet></router-outlet> and nav links to app.component.html.
Make sure app.config.ts includes provideHttpClient().

Run:
ng serve
