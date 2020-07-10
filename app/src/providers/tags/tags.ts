import { Injectable } from '@angular/core';

import { Api } from '../api/api';
import { Tag } from '../../models/tag';

@Injectable()
export class Tags {
  x:any;
  constructor(public api: Api) {}

  query() {
    return this.api.getTags('tags')
  }

  add(tag: Tag) {
  }

  delete(tag: Tag) {
  }

}
