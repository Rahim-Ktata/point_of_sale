import { Component, signal } from '@angular/core';
import { RouterModule } from '@angular/router';


@Component({
  imports: [RouterModule],
  selector: 'app-root',
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App {
  protected readonly title = signal('pos_front');
}
