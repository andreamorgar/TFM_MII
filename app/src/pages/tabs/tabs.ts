import { Component } from '@angular/core';
import { IonicPage, NavController } from 'ionic-angular';

import { Tab1Root, Tab2Root, Tab3Root } from '../';

@IonicPage()
@Component({
  selector: 'page-tabs',
  templateUrl: 'tabs.html'
})
export class TabsPage {
  tab1Root: any = Tab1Root;
  tab2Root: any = Tab2Root;
  tab3Root: any = Tab3Root;

  tab1Title = " ";
  tab2Title = " ";
  tab3Title = " ";

  // this.tab1Title = values['TAB1_TITLE'];
  constructor(public navCtrl: NavController) {
    
      this.tab1Title = 'Recipes';
      this.tab2Title = 'Search';
      this.tab3Title = 'Adapted recipes';
    
  }
}
