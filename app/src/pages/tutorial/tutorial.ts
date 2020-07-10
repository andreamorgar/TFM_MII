import { Component } from '@angular/core';
import { IonicPage, MenuController, NavController, Platform } from 'ionic-angular';


export interface Slide {
  title: string;
  description: string;
  image: string;
}

@IonicPage()
@Component({
  selector: 'page-tutorial',
  templateUrl: 'tutorial.html'
})
export class TutorialPage {
  slides: Slide[];
  showSkip = true;
  dir: string = 'ltr';

  constructor(public navCtrl: NavController, public menu: MenuController, public platform: Platform) {
    this.dir = platform.dir();

        this.slides = [
          {
            title: 'Welcome!',
            description: 'In this app, you can find lots of recipes and customize to your preferences. You will be able to modify your recipes to take into account allergies, intolerances, specific diseases like diabetes or even diets such as vegetarian or vegan.',
            image: 'assets/img/icon_def.png',
          },
          {
            title: 'How to?',
            description: 'When you fancy cooking, explore the recipe gallery. Pick one and adapt the ingredients to your needs by applying food restrictions.',
            image: 'assets/img/food_app1.png',
          },
          {
            title: 'Smart recipe adaptation',
            description: 'The app uses food intelligence to calculate the most suitable alternative for your diet',
            image: 'assets/img/food_app2.png',
          }
        ];
 
  }

  startApp() {
    this.navCtrl.setRoot('WelcomePage', {}, {
      animate: true,
      direction: 'forward'
    });
  }

  onSlideChangeStart(slider) {
    this.showSkip = !slider.isEnd();
  }

  ionViewDidEnter() { 
    this.menu.enable(false);
  }

  ionViewWillLeave() {  
    this.menu.enable(true);
  }

}
