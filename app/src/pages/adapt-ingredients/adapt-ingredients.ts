import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, LoadingController } from 'ionic-angular';
import { Recipe, RespuestaAdapt, Ingredient } from '../../models/recipe';
import { Recipes } from '../../providers/recipes/recipes';

/**
 * Generated class for the AdaptIngredientsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-adapt-ingredients',
  templateUrl: 'adapt-ingredients.html',
})
export class AdaptIngredientsPage {
  item: Recipe;
  calories: any;
  adaptMode: any;
  variable: any;

  adaptedRecipe: RespuestaAdapt;
  adaptedIngredients: Ingredient[];

  constructor(public navCtrl: NavController, public loadingController: LoadingController, 
    public navParams: NavParams, public recipes: Recipes) {

      let loading = this.loadingController.create({});
      loading.present();

    this.item = navParams.get('item');
    this.recipes = recipes;
    this.calories = this.item.nutrients[0];
    this.adaptMode = navParams.get('adapt_mode')
    this.item.name = this.item.name;
    

    console.log("Adaptation mode: ",this.adaptMode);

    this.recipes.adapt(this.adaptMode,this.item)
    .subscribe( resp => {
      console.log('adaptedRecipe',resp);
      this.adaptedRecipe = resp;
      this.adaptedIngredients = resp.ingredients;
      // this.adaptedSteps = resp.steps;
      // console.log('adaptedSteps', this.adaptedSteps);
      loading.dismiss();
    });  
  }



  ionViewDidLoad() {
    console.log('ionViewDidLoad AdaptIngredientsPage');
  }


  generateRecipe(){
    console.log("Entra a generateRecipe()")
    console.log(this.adaptedRecipe);
    this.navCtrl.push('AdaptedRecipePage', {
      item: this.adaptedRecipe,
      adapt_mode: this.adaptMode,
      adaptedIngredients: this.adaptedIngredients
    });
  }

}
