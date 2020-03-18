import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UploadImageComponent } from './upload-image/upload-image.component';


const routes: Routes = [
  {path:'', component:UploadImageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
