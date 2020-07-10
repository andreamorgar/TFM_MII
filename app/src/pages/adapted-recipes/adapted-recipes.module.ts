import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AdaptedRecipesPage } from './adapted-recipes';

@NgModule({
  declarations: [
    AdaptedRecipesPage,
  ],
  imports: [
    IonicPageModule.forChild(AdaptedRecipesPage),
  ],
})
export class AdaptedRecipesPageModule {}
