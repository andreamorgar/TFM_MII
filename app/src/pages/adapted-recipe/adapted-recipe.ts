import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, LoadingController, ToastController } from 'ionic-angular';
import { Recipe, RespuestaAdapt, Ingredient, Step } from '../../models/recipe';
import { Recipes } from '../../providers/recipes/recipes';




/**
 * Generated class for the AdaptedRecipePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-adapted-recipe',
  templateUrl: 'adapted-recipe.html',
})
export class AdaptedRecipePage {
  item: Recipe;
  calories: any;
  adaptMode: any;
  
  adaptedRecipe: RespuestaAdapt;
  adaptedIngredients: Ingredient[];
  adaptedSteps: Step[];


  constructor(public navCtrl: NavController, public loadingController: LoadingController, public toastController: ToastController,
    public navParams: NavParams, public recipes: Recipes) {

      let loading = this.loadingController.create({});
      loading.present();

    this.adaptedRecipe = navParams.get('item');
    this.recipes = recipes;
    this.calories = this.adaptedRecipe.nutrients[0];
    this.adaptedIngredients = navParams.get('adaptedIngredients')
    this.adaptMode = navParams.get('adapt_mode')

    // console.log("Adaptation mode: ",this.adaptMode);
    // console.log("Adapted Ingredients",this.adaptedIngredients)

    this.recipes.adaptSteps(this.adaptedRecipe)
    .subscribe( resp => {
      console.log('adaptedRecipe',resp);
      this.adaptedSteps = resp['steps'];
      console.log('adaptedSteps', this.adaptedSteps);
      loading.dismiss();
    });  
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad AdaptedRecipePage');
  }

  save(){
    this.recipes.saveAdapted(this.adaptedRecipe);
    this.presentToast();
  }


  async presentToast() {

    const toast = await this.toastController.create({
      message: 'Saved',
      duration: 1500
    });
    toast.present();
  }

}
