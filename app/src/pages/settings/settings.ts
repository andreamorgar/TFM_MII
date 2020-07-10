import { Component } from '@angular/core';

import { IonicPage, NavController, NavParams } from 'ionic-angular';


import {  RespuestaAdapt } from '../../models/recipe';
import { Recipes } from '../../providers/recipes/recipes';
import { Item } from '../../models/item';



@IonicPage()
@Component({
  selector: 'page-settings',
  templateUrl: 'settings.html'
})
export class SettingsPage {

  currentItems: RespuestaAdapt[] = [];
  constructor(public navCtrl: NavController, public navParams: NavParams, public recipes: Recipes) {
    this.recipes.query_all_adapted()
    .subscribe( resp => {
      console.log('currentItems',resp);
      this.currentItems.push(...resp.recipes);
    });
   }


   removeItem(item: RespuestaAdapt){
     console.log("borrar_item");
   }
   openItem(item: Item) {
     console.log(item);
    this.navCtrl.push('AdaptedRecipePage', {
      item: item,
      adapt: false,
      adaptedIngredients: item.ingredients
    });
  }


   ionViewDidLoad() {

   }


}