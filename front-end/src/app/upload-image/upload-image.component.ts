import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import { DomSanitizer } from '@angular/platform-browser';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-upload-image',
  templateUrl: './upload-image.component.html',
  styleUrls: ['./upload-image.component.scss']
})
export class UploadImageComponent implements OnInit {
  file = null;
  file_size = null;
  file_name = null;
  isLinear = false;
  image_url
  firstFormGroup: FormGroup;
  secondFormGroup: FormGroup;
  formData = new FormData();
  pred = "Awaiting prediction..."
  constructor(private _formBuilder: FormBuilder, private sanitizer: DomSanitizer, private httpClient: HttpClient) { }

  ngOnInit() {
    this.firstFormGroup = this._formBuilder.group({
      firstCtrl: ['', Validators.required]
    });
    this.secondFormGroup = this._formBuilder.group({
      secondCtrl: ['', Validators.required]
    });
  }

  clear() {
    this.file = null;
    this.file_name = null;
    this.file_size = null;
  
    }

    addFile(event) {
      this.file = event.target.files[0];
       this.image_url = URL.createObjectURL(this.file)
      var reader = new FileReader();
      this.image_url = this.file;
      reader.readAsDataURL(this.file); 
      reader.onload = (_event) => { 
        this.image_url = reader.result; 
      }
      this.formData.append('file', this.file);
      this.file_size = event.target.files[0].size / 10e6;
      this.file_size = this.file_size.toPrecision(2);
      this.file_name = event.target.files[0].name;
  }

  removeFile() {
    this.file = null;
    this.file_name = null;
    this.file_size = null;
    this.formData.delete('file')
  }

  send_img(){
    console.log(this.formData.get('file'))
    this.httpClient.post('http://3.134.200.189:5000/', this.formData)
    .subscribe((resp) => {
      console.log(resp)
      this.pred = 'This sample has a ' + resp['pred'].toString() + '%' + ' chance of cancer'
  
      },
      (error) => {
      
      });
  }

}
