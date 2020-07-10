


import { Component } from '@angular/core';
import { IonicPage, ModalController, NavController } from 'ionic-angular';

import { Item } from '../../models/item';
// import { Items } from '../../providers';
import { Tag } from '../../models/tag';
import { Tags } from '../../providers/tags/tags';
// import { Tags } from '../../mocks/providers/tags';

@IonicPage()
@Component({
  selector: 'page-list-master',
  templateUrl: 'list-master.html'
})
export class ListMasterPage {
  currentItems: Tag[] = [];

  // constructor(public navCtrl: NavController, public tags: Tags, public modalCtrl: ModalController) {
  //   this.tags.api.getTags('tags')
  //     .subscribe( resp => {
  //       console.log('currentItems',resp);
  //       this.currentItems.push(...resp.tags);
  //     });
    

  // }
  constructor(public navCtrl: NavController, public tags: Tags, public modalCtrl: ModalController) {
    this.tags.query()
      .subscribe( resp => {
        console.log('currentItems',resp);
        this.currentItems.push(...resp.tags);
      });
    

  }
  ionViewDidLoad() {
  }

  /**
   * Prompt the user to add a new item. This shows our ItemCreatePage in a
   * modal and then adds the new item to our data source if the user created one.
   */
  addItem() {
    let addModal = this.modalCtrl.create('ItemCreatePage');
    addModal.onDidDismiss(item => {
      if (item) {
        this.tags.add(item);
      }
    })
    addModal.present();
  }

  /**
   * Delete an item from the list of items.
   */
  deleteItem(item) {
    this.tags.delete(item);
  }

  /**
   * Navigate to the detail page for this item.
   */
  openItem(item: Item) {
    console.log("Entra a openItem()")
    this.navCtrl.push('ListRecipesPage', {
      tag: item
    });
  }
}
