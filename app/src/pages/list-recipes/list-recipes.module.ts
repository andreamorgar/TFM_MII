import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ListRecipesPage } from './list-recipes';

@NgModule({
  declarations: [
    ListRecipesPage,
  ],
  imports: [
    IonicPageModule.forChild(ListRecipesPage),
  ],
})
export class ListRecipesPageModule {}
