import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, AlertController } from 'ionic-angular';


import { Recipe } from '../../models/recipe';
import { Recipes } from '../../providers/recipes/recipes';


@IonicPage()
@Component({
  selector: 'page-item-detail',
  templateUrl: 'item-detail.html'
})
export class ItemDetailPage {
  item: Recipe;
  calories: any;



  constructor(public navCtrl: NavController, 
    public recipes: Recipes, 
    private alertController: AlertController,
    navParams: NavParams) {

    this.item = navParams.get('item');
    this.recipes = recipes;
    this.calories = this.item.nutrients[0];
    this.item.name = this.item.name.charAt(0).toUpperCase() + this.item.name.slice(1);
  }

  adaptRecipe(){

    this.alertAdaptationRecipe();

  
  }



  async alertAdaptationRecipe() {
    
    const alert = this.alertController.create({
      title:'Adapt this recipe!',
      message: 'Select the food restriction you want to apply to recipe ingredients!',
      inputs: [
        {
          name: 'vegetarian',
          type: 'radio',
          label: 'Vegetarian',
          value: 'vegetarian',
          checked: true
        },
        {
          name: 'vegan',
          type: 'radio',
          label: 'Vegan',
          value: 'vegan'
        },
      ],
      buttons: [
        {
          text: 'Cancel',
          role: 'cancel',
          cssClass: 'secondary',
          handler: () => {
            console.log('Confirm Cancel');
          }
        }, {
          text: 'Ok',
          handler: (data:string) => {
            console.log('Confirm Ok');
            console.log(JSON.stringify(data));

            this.navCtrl.push('AdaptIngredientsPage', {
              item: this.item,
              adapt_mode: data
            });
            }

        }
      ]
    });

    await alert.present();
    if(alert){
      console.log(alert.data);
    }
    
  }

  
}
