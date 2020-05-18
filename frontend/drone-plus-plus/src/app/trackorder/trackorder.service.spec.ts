import { TestBed } from '@angular/core/testing';

import { TrackorderService } from './trackorder.service';

describe('TrackorderService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TrackorderService = TestBed.get(TrackorderService);
    expect(service).toBeTruthy();
  });
});
