import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ResetPswd } from './reset-pswd';

describe('ResetPswd', () => {
  let component: ResetPswd;
  let fixture: ComponentFixture<ResetPswd>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResetPswd],
    }).compileComponents();

    fixture = TestBed.createComponent(ResetPswd);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
