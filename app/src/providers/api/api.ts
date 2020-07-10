import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { RespuestaTags } from '../../models/tag';
import { RespuestaRecipes, RespuestaAdapt, RespuestaAdaptRecipes } from '../../models/recipe';
/**
 * Api is a generic REST Api handler. Set your API url first.
 */
@Injectable()
export class Api {
  url: string = 'http://0.0.0.0:5000';

  constructor(public http: HttpClient) {
  }

  getTags(endpoint: string){
    console.log(this.http.get<RespuestaTags>(this.url + '/' + endpoint));
    return this.http.get<RespuestaTags>(this.url + '/' + endpoint); 
  }

  getRecipes(endpoint: string){
    console.log(this.http.get<RespuestaRecipes>(this.url + '/' + endpoint));
    return this.http.get<RespuestaRecipes>(this.url + '/' + endpoint); 
  }


  getRecipesAdapted(endpoint: string){
    console.log(this.http.get<RespuestaAdaptRecipes>(this.url + '/' + endpoint));
    return this.http.get<RespuestaAdaptRecipes>(this.url + '/' + endpoint); 
  }

  adaptRecipe(endpoint: string){
    console.log(this.http.get<RespuestaAdapt>(this.url + '/' + endpoint));
    return this.http.get<RespuestaAdapt>(this.url + '/' + endpoint); 
  }


  adaptRecipeStep(endpoint: string, body: any){
    
    console.log(this.url+ '/' + endpoint);
    console.log(body)

    this.http.post(this.url + '/' + endpoint,body)
      .subscribe(data => {
        console.log(data['_body']);
       }, error => {
        console.log(error);
    });

    return this.http.post(this.url + '/' + endpoint,body)
  }

  get(endpoint: string, params?: any, reqOpts?: any) {
    if (!reqOpts) {
      reqOpts = {
        params: new HttpParams()
      };
    }

    
    if (params) {
      reqOpts.params = new HttpParams();
      for (let k in params) {
        reqOpts.params = reqOpts.params.set(k, params[k]);
      }
    }

    console.log(this.http.get(this.url + '/' + endpoint, reqOpts));
    return this.http.get(this.url + '/' + endpoint, reqOpts);
  }

  post(endpoint: string, body: any, reqOpts?: any) {
    return this.http.post(this.url + '/' + endpoint, body, reqOpts);
  }

  postAdaptedRecipe(endpoint: string, body: any){
    
    console.log(this.url + endpoint);
    console.log(body)

    this.http.post(this.url + endpoint,body)
      .subscribe(data => {
        console.log(data['_body']);
       }, error => {
        console.log(error);
      });

    return this.http.post(this.url + endpoint,body)

  }

  put(endpoint: string, body: any, reqOpts?: any) {
    return this.http.put(this.url + '/' + endpoint, body, reqOpts);
  }

  delete(endpoint: string, reqOpts?: any) {
    return this.http.delete(this.url + '/' + endpoint, reqOpts);
  }

  patch(endpoint: string, body: any, reqOpts?: any) {
    return this.http.patch(this.url + '/' + endpoint, body, reqOpts);
  }
}
