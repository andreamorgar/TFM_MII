// import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AlertController } from 'ionic-angular';


/*
  Generated class for the AlertsProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class Alerts {

  constructor(private alertController: AlertController) {
    
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
          name: 'veggie',
          type: 'radio',
          label: 'Veggie',
          value: 'veggie'
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
