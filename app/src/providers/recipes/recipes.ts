import { Injectable } from '@angular/core';
import { Recipe, RespuestaAdapt } from '../../models/recipe';
import { Api } from '../api/api';
/*
  Generated class for the RecipesProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class Recipes{
  items: Recipe[] = [];

  constructor(public api: Api) {  
    this.api.getRecipes('recipes')
    .subscribe( resp => {
      console.log('items',resp);
      this.items.push(...resp.recipes);
    });
  }

  query(params: string) {
    console.log(params);
    return this.api.getRecipes('recipes/tag/'+params);
  }

  query_all() {
    return this.api.getRecipes('recipes');
  }


  query_all_adapted() {
    return this.api.getRecipesAdapted('adapted_recipes');
  }

  add(recipe: Recipe) {
  }

  delete(recipe: Recipe) {
  }

  adapt(mode:String,recipe: Recipe) {
    return this.api.adaptRecipe('model/adapt/'+mode+'/'+recipe.id_recipe)
  }

  adaptSteps(recipe: RespuestaAdapt) {
    return this.api.adaptRecipeStep('model/adapt/steps',recipe)
  }


  adaptedRecipe: RespuestaAdapt;

  saveAdapted(recipe: RespuestaAdapt){
    this.api.postAdaptedRecipe('/adapted_recipes',recipe);
  }

  search(params?: any) {
    if (!params) {
      return this.items;
    }
    
    return this.items.filter((item) => {
      for (let key in params) {
        let field = item[key];
        if (typeof field == 'string' && field.toLowerCase().indexOf(params[key].toLowerCase()) >= 0) {
          return item;
        } else if (field == params[key]) {
          return item;
        }
      }
      return null;
    });
  }

}
 