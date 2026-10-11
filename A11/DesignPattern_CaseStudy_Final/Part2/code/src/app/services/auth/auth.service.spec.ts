import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { AuthService } from './auth.service';

describe('AuthService', () => {
  let service: AuthService;
  let http: HttpTestingController;
  const savedUser = { id: 3, name: 'Student' };

  beforeEach(() => {
    spyOn(localStorage, 'getItem').and.returnValue(null);
    spyOn(localStorage, 'setItem');
    spyOn(localStorage, 'removeItem');
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    service = TestBed.inject(AuthService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('publishes login state through the shared subject', () => {
    const updates: unknown[] = [];
    service.currentUser$.subscribe(user => updates.push(user));
    service.setUser(savedUser);
    expect(localStorage.setItem).toHaveBeenCalledWith('currentUser', JSON.stringify(savedUser));
    expect(updates).toEqual([null, savedUser]);
  });

  it('clears persisted and published state after a successful logout', () => {
    service.setUser(savedUser);
    const updates: unknown[] = [];
    service.currentUser$.subscribe(user => updates.push(user));
    service.logout().subscribe();
    http.expectOne('http://localhost:8080/api/logout').flush({});
    expect(localStorage.removeItem).toHaveBeenCalledWith('currentUser');
    expect(updates).toEqual([savedUser, null]);
  });
});
