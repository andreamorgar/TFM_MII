import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { Recipes } from '../../providers/recipes/recipes';
import { Recipe } from '../../models/recipe';

/**
 * Generated class for the ListRecipesPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-list-recipes',
  templateUrl: 'list-recipes.html',
})
export class ListRecipesPage {
  tag: any;
  currentItems: Recipe[] = [];

  constructor(public navCtrl: NavController, navParams: NavParams, public recipes: Recipes) {
    // get the specific tag to look for related recipes
    this.tag = navParams.get('tag');
    console.log(this.tag)

    this.recipes.query(this.tag.tag)
    .subscribe( resp => {
      console.log('currentItems',resp);
      this.currentItems.push(...resp.recipes);
    });
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad ListRecipesPage');
  }


  openItem(item: Recipe) {
    this.navCtrl.push('ItemDetailPage', {
      item: item
    });
  }

}
