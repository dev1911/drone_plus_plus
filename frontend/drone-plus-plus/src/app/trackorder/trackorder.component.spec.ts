import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrackorderComponent } from './trackorder.component';

describe('TrackorderComponent', () => {
  let component: TrackorderComponent;
  let fixture: ComponentFixture<TrackorderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrackorderComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrackorderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
