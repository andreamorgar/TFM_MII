import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';

import { Item } from '../../models/item';

import { Recipes } from '../../providers/recipes/recipes';
import { Recipe } from '../../models/recipe';

@IonicPage()
@Component({
  selector: 'page-search',
  templateUrl: 'search.html'
})
export class SearchPage {
  
  currentItems: Recipe[] = [];
  constructor(public navCtrl: NavController, public navParams: NavParams, public recipes: Recipes) {
    this.recipes.query_all()
    .subscribe( resp => {
      console.log('currentItems',resp);
      this.currentItems.push(...resp.recipes);
    });
   }

  /**
   * Perform a service for the proper items.
   */
  getItems(ev) {
    let val = ev.target.value;
    if (!val || !val.trim()) {
      this.currentItems = []; // primero lo vaciamos
      this.recipes.query_all()
      .subscribe( resp => {
        console.log('currentItems',resp);
        this.currentItems.push(...resp.recipes);
      });
      
      return;
    }
    this.currentItems = this.recipes.search({
      name: val
    });
  }

  /**
   * Navigate to the detail page for this item.
   */
  openItem(item: Item) {
    this.navCtrl.push('ItemDetailPage', {
      item: item
    });
  }

}
