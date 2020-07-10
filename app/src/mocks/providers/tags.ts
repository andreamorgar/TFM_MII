import { Injectable } from '@angular/core';

import { Tag } from '../../models/tag';

@Injectable()
export class Tags {
  items: Tag[] = [];

  defaultItem: any = {
    "name": "Burt Bear",
    "profilePic": "assets/img/speakers/bear.jpg",
    "about": "Burt is a Bear.",
  };


  constructor() {
    let items = [
      {
        "name": "Charlie Cheetah",
        "profilePic": "assets/img/speakers/cheetah.jpg",
        "about": "Charlie is a Cheetah."
      },
      {
        "name": "Donald Duck",
        "profilePic": "assets/img/speakers/duck.jpg",
        "about": "Donald is a Duck."
      },
      {
        "name": "Eva Eagle",
        "profilePic": "assets/img/speakers/eagle.jpg",
        "about": "Eva is an Eagle."
      },
      {
        "name": "Ellie Elephant",
        "profilePic": "assets/img/speakers/elephant.jpg",
        "about": "Ellie is an Elephant."
      },
      {
        "name": "Molly Mouse",
        "profilePic": "assets/img/speakers/mouse.jpg",
        "about": "Molly is a Mouse."
      },
      {
        "name": "Paul Puppy",
        "profilePic": "assets/img/speakers/puppy.jpg",
        "about": "Paul is a Puppy."
      }
      

    ];

    for (let item of items) {
      this.items.push(new Tag(item));
    }
  }

  query(params?: any) {
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

  add(item: Tag) {
    this.items.push(item);
  }

  delete(item: Tag) {
    this.items.splice(this.items.indexOf(item), 1);
  }
}








// {
//   "name": "Baked Zucchini Sticks",
//   "profilePic": "assets/img/recipes/mediterranean_baker_zucchini_sticks.jpg",
//   "about": "Mediterranean, Lunch",
//   "ingredients": [
//     "zucchini",
//     "red bell pepper",
//     "tomatoes",
//     "kalamata olives",
//     "large garlic cloves",
//     "oregano",
//     "ground black pepper",
//     "feta cheese",
//     "parsley"
//   ],
// },
// {
//   "name": "Greek Spinach-Avocado Salad",
//   "profilePic": "assets/img/recipes/green_spinach_avocado_salad.jpeg",
//   "about": "Mediterranean, Greek, salad",
//   "ingredients": [
//     "spinach",
//     "large tomato",
//     "English cucumber",
//     "crumbled feta cheese",
//     "red onion",
//     "avocado",
//     "kalamata olives",
//     "olive oil",
//     "dried oregano"
//   ],
// },
// {
//   "name":"Greek Chicken Bowls",
//   "profilePic": "assets/img/recipes/GREEK-CHICKEN-BOWLS.jpg",
//   "about": "Mediterranean, Lunch, Main dishes",
//   "ingredients": [
//     "cherry tomatoes",
//     "cucumbers",
//     "chicken breast",
//     "crumbled feta cheese"
//   ],
// },
// {
//   "name":"Grilled Chicken Skewers",
//   "profilePic": "assets/img/recipes/mediterranean_grilled_chicken_skewers.jpg",
//   "about": "Mediterranean, Lunch, Barbecue",
//   "ingredients": [
//     "boneless, skinless chicken breast",
//     "olive oil",
//     "lemon",
//     "dried oregano",
//     "dried parsley",
//     "cayenne pepper",
//     "salt"
//   ],
// }