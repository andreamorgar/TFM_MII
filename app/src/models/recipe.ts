export class Recipe {

    constructor(fields: any) {
      // Quick and dirty extend/assign fields to this model
      for (const f in fields) {
        // @ts-ignore
        this[f] = fields[f];
      }
    }
  
  }
  
  export interface RespuestaRecipes {
    recipes: Recipe[];
  }
  
  export interface Recipe {
    description: string;
    id_recipe: string;
    image: string;
    ingredients: string[];
    minutes: string;
    n_ingredients: number;
    n_steps: number;
    name: string;
    nutrients: number[];
    steps: string[];
    tags: string[];
  }


  export interface RespPost {
    msg: string;
  }

  // export interface RespuestaAdapt {
  //   adapted_ingredients: Adaptedingredient[];
  // }
  
  // export interface Adaptedingredient {
  //   ingrediente: string;
  //   modified: string;
  // }






  export interface RespuestaAdaptRecipes {
    recipes: RespuestaAdapt[];
  }
  



  export interface RespuestaAdapt {
    description: string;
    id_recipe: string;
    image: string;
    ingredients: Ingredient[];
    minutes: string;
    n_ingredients: number;
    n_steps: number;
    name: string;
    nutrients: number[];
    steps: Step[];
    tags: string[];
  }
  
  export interface Step {
    modified: string;
    step: string;
  }
  
  export interface Ingredient {
    adapted: string;
    modified: string;
    name: string;
  }