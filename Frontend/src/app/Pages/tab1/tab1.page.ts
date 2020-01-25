import { Component, OnInit } from '@angular/core';
import { WebSocketService } from 'src/app/Services/web-socket.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page implements OnInit {
  ecgSegments;
  private ecgData = null;
  private beatTypes = {
    'N': 'Normal beat',
    'L': 'Left bundle branch block beat',
    'R': 'Right bundle branch block beat',
    'B': 'Bundle branch block beat (unspecified)',
    'A': 'Atrial premature beat',
    'a': 'Aberrated atrial premature beat',
    'J': 'Nodal (junctional) premature beat',
    'S': 'Supraventricular premature or ectopic beat (atrial or nodal)',
    'V': 'Premature ventricular contraction',
    'r': 'R-on-T premature ventricular contraction',
    'F': 'Fusion of ventricular and normal beat',
    'e': 'Atrial escape beat',
    'j': 'Nodal (junctional) escape beat',
    'n': 'Supraventricular escape beat (atrial or nodal)',
    'E': 'Ventricular escape beat',
    '/': 'Paced beat',
    'f': 'Fusion of paced and normal beat',
    'Q': 'Unclassifiable beat',
    '?': 'Beat not classified during learning',
  };

  private nonBeatTypes = {
    '[': 'Start of ventricular flutter/fibrillation',
    '!': 'Ventricular flutter wave',
    ']': 'End of ventricular flutter/fibrillation',
    'x': 'Non-conducted P-wave (blocked APC)',
    '(': 'Waveform onset',
    ')': 'Waveform end',
    'p': 'Peak of P-wave',
    't': 'Peak of T-wave',
    'u': 'Peak of U-wave',
    '`': 'PQ junction',
    '\'': 'J-point',
    '^': '(Non-captured) pacemaker artifact',
    '|': 'Isolated QRS-like artifact [1]',
    '~': 'Change in signal quality [1]',
    '+': 'Rhythm change [2]',
    's': 'ST segment change [2]',
    'T': 'T-wave change [2]',
    '*': 'Systole',
    'D': 'Diastole',
    '=': 'Measurement annotation [2]',
    '"': 'Comment annotation [2]',
    '@': 'Link to external data [3]',
  };

  private arrythmiaType = {
    '·': 'Normal beat',
    'N': 'Normal beat',
    'L': 'Left bundle branch block beat',
    'R': 'Right bundle branch block beat',
    'A': 'Atrial premature beat',
    'a': 'Aberrated atrial premature beat',
    'J': 'Nodal (junctional) premature beat',
    'S': 'Supraventricular premature beat',
    'V': 'Premature ventricular contraction',
    'F': 'Fusion of ventricular and normal beat',
    '[': 'Start of ventricular flutter/fibrillation',
    '!': 'Ventricular flutter wave',
    ']': 'End of ventricular flutter/fibrillation',
    'e': 'Atrial escape beat',
    'j': 'Nodal (junctional) escape beat',
    'E': 'Ventricular escape beat',
    '/': 'Paced beat',
    'f': 'Fusion of paced and normal beat',
    'x': 'Non-conducted P-wave (blocked APB)',
    'Q': 'Unclassifiable beat',
    '|': 'Isolated QRS-like artifact',
  };

  constructor(
    private router: Router,
    private webSocketService: WebSocketService
  ) {}

  ngOnInit() {
    this.webSocketService.addFromEvent(this.router.url, 'new-ecg-segments', (data) => {
      this.ecgData = data;
      this.replaceECGSegments();
    });
    this.getNewECGSegments();
  }

  getNewECGSegments() {
    this.webSocketService.emitMessage('get-ecg-segments');
  }

  replaceECGSegments() {
    this.ecgSegments = this.ecgData.map(d => (
      {
      title: this.beatTypes[d.type] ? (this.beatTypes[d.type] + ' ' + d.item + ' of ' + d.count) : ('ERR -> ' + d.type),
      values: d.values
    }));
  }
}
