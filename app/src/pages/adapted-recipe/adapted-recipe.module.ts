import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AdaptedRecipePage } from './adapted-recipe';

@NgModule({
  declarations: [
    AdaptedRecipePage,
  ],
  imports: [
    IonicPageModule.forChild(AdaptedRecipePage),
  ],
})
export class AdaptedRecipePageModule {}
