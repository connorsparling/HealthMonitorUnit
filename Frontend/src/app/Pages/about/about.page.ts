import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import marked from 'marked';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-about',
  templateUrl: './about.page.html',
  styleUrls: ['./about.page.scss'],
})
export class AboutPage implements OnInit {
  @ViewChild('aboutMD', { static: true }) aboutMD: ElementRef;

  constructor(
    private http: HttpClient
  ) { }

  ngOnInit() {
    this.http.get('assets/about/About.md', {responseType: 'text'}).subscribe(
      result => {
        const md = marked.setOptions({});
        const convertedData = md.parse(result);
        this.aboutMD.nativeElement.innerHTML = convertedData;
      },
      error => {
        console.log('Path not found with error:', error);
      }
    );
  }
}
