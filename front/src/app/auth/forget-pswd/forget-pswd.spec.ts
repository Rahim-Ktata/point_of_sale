import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ForgetPswd } from './forget-pswd';

describe('ForgetPswd', () => {
  let component: ForgetPswd;
  let fixture: ComponentFixture<ForgetPswd>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ForgetPswd],
    }).compileComponents();

    fixture = TestBed.createComponent(ForgetPswd);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
