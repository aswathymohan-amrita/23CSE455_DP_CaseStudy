import React, { useState } from 'react';

export interface UserSession {
  email: string;
  role: 'MANAGER' | 'SERVER' | 'KITCHEN' | 'UNAUTHENTICATED';
  token?: string;
}

interface AuthModalProps {
  currentSession: UserSession;
  onLoginSuccess: (session: UserSession) => void;
  onClose: () => void;
  isOpen: boolean;
}

export const AuthModal: React.FC<AuthModalProps> = ({
  currentSession,
  onLoginSuccess,
  onClose,
  isOpen,
}) => {
  const [email, setEmail] = useState('mgr@restaurant.com');
  const [password, setPassword] = useState('mgr123');
  const [targetEndpointRole, setTargetEndpointRole] = useState<'MANAGER' | 'SERVER' | 'KITCHEN'>('MANAGER');

  // Execution Trace State
  const [trace, setTrace] = useState<{
    facadeStatus: 'idle' | 'success' | 'failed';
    facadeMsg: string;
    tokenCheck: 'idle' | 'pass' | 'fail';
    roleCheck: 'idle' | 'pass' | 'fail';
    routeAccess: 'idle' | 'granted' | 'forbidden';
    httpStatus: number | null;
  }>({
    facadeStatus: 'idle',
    facadeMsg: '',
    tokenCheck: 'idle',
    roleCheck: 'idle',
    routeAccess: 'idle',
    httpStatus: null,
  });

  if (!isOpen) return null;

  const mockUsers: Record<string, { pass: string; role: 'MANAGER' | 'SERVER' | 'KITCHEN' }> = {
    'mgr@restaurant.com': { pass: 'mgr123', role: 'MANAGER' },
    'server@restaurant.com': { pass: 'serve123', role: 'SERVER' },
    'chef@restaurant.com': { pass: 'chef123', role: 'KITCHEN' },
  };

  const handleRunAuth = () => {
    // ── 1. FACADE EXECUTION (mirrors AuthService.login) ──
    const user = mockUsers[email];
    if (!user || user.pass !== password) {
      setTrace({
        facadeStatus: 'failed',
        facadeMsg: !user ? 'User not found in DB' : 'Invalid password (bcrypt mismatch)',
        tokenCheck: 'fail',
        roleCheck: 'fail',
        routeAccess: 'forbidden',
        httpStatus: 401,
      });
      return;
    }

    const generatedToken = `tok_${btoa(email).slice(0, 10)}_${user.role}`;
    const newSession: UserSession = { email, role: user.role, token: generatedToken };

    // ── 2. CHAIN OF RESPONSIBILITY (mirrors middleware/auth.ts) ──
    // Link 1: TokenValidator
    const hasToken = !!generatedToken && generatedToken.startsWith('tok_');
    // Link 2: RoleChecker (checking access for required endpoint role)
    const roleMatches = user.role === targetEndpointRole || user.role === 'MANAGER'; // manager has broad access

    setTrace({
      facadeStatus: 'success',
      facadeMsg: `User authenticated via AuthFacade. Generated: ${generatedToken}`,
      tokenCheck: hasToken ? 'pass' : 'fail',
      roleCheck: roleMatches ? 'pass' : 'fail',
      routeAccess: roleMatches ? 'granted' : 'forbidden',
      httpStatus: roleMatches ? 200 : 403,
    });

    onLoginSuccess(newSession);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <span className="pill-badge orange">GoF Patterns in Action</span>
            <h3 style={{ marginTop: '0.25rem' }}>Staff Authentication & Permission Engine</h3>
            <p style={{ color: '#78716c', fontSize: '0.85rem' }}>
              Tests <strong>Façade Pattern</strong> (login orchestration) and <strong>Chain of Responsibility</strong> (middleware token & role check).
            </p>
          </div>
          <button className="btn-close" onClick={onClose}>×</button>
        </div>

        {/* Quick Credentials Presets */}
        <div style={{ marginTop: '1rem', marginBottom: '1rem' }}>
          <label style={{ fontSize: '0.8rem', fontWeight: 600, color: '#44403c', display: 'block', marginBottom: '0.4rem' }}>
            Quick Select Preset Staff:
          </label>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button
              type="button"
              className="btn-preset"
              onClick={() => { setEmail('mgr@restaurant.com'); setPassword('mgr123'); }}
            >
              👔 Manager (mgr@restaurant.com)
            </button>
            <button
              type="button"
              className="btn-preset"
              onClick={() => { setEmail('server@restaurant.com'); setPassword('serve123'); }}
            >
              💁 Server (server@restaurant.com)
            </button>
            <button
              type="button"
              className="btn-preset"
              onClick={() => { setEmail('chef@restaurant.com'); setPassword('chef123'); }}
            >
              👨‍🍳 Chef (chef@restaurant.com)
            </button>
            <button
              type="button"
              className="btn-preset error"
              onClick={() => { setEmail('guest@unknown.com'); setPassword('badpass'); }}
            >
              ❌ Invalid Credentials
            </button>
          </div>
        </div>

        {/* Form Inputs */}
        <div className="form-grid">
          <div>
            <label className="form-label">Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="form-input"
            />
          </div>
          <div>
            <label className="form-label">Password</label>
            <input
              type="text"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-input"
            />
          </div>
        </div>

        <div style={{ marginTop: '1rem' }}>
          <label className="form-label">Test Permission Chain Against Route:</label>
          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.3rem' }}>
            {(['MANAGER', 'SERVER', 'KITCHEN'] as const).map((r) => (
              <label key={r} style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', fontSize: '0.85rem', cursor: 'pointer' }}>
                <input
                  type="radio"
                  name="targetRole"
                  checked={targetEndpointRole === r}
                  onChange={() => setTargetEndpointRole(r)}
                />
                Requires {r}
              </label>
            ))}
          </div>
        </div>

        <button onClick={handleRunAuth} className="btn-primary-orange" style={{ width: '100%', marginTop: '1.25rem' }}>
          🚀 Execute AuthFacade & Middleware Chain
        </button>

        {/* Live Execution Trace / Flow */}
        {trace.httpStatus !== null && (
          <div className="trace-box">
            <h4 style={{ color: '#c2410c', marginBottom: '0.5rem', fontSize: '0.9rem' }}>
              Execution Trace Results:
            </h4>

            {/* Facade Step */}
            <div className={`trace-step ${trace.facadeStatus}`}>
              <div className="step-num">1</div>
              <div>
                <strong>Façade Pattern (AuthService.login):</strong>
                <p style={{ fontSize: '0.8rem' }}>{trace.facadeMsg}</p>
              </div>
            </div>

            {/* Chain of Responsibility Step 1 */}
            <div className={`trace-step ${trace.tokenCheck === 'pass' ? 'success' : 'failed'}`}>
              <div className="step-num">2</div>
              <div>
                <strong>CoR Link 1 — TokenValidator:</strong>
                <p style={{ fontSize: '0.8rem' }}>
                  {trace.tokenCheck === 'pass' ? 'Token verified & attached to req.user ✓' : 'Rejected with HTTP 401 (No valid token) ✗'}
                </p>
              </div>
            </div>

            {/* Chain of Responsibility Step 2 */}
            <div className={`trace-step ${trace.roleCheck === 'pass' ? 'success' : 'failed'}`}>
              <div className="step-num">3</div>
              <div>
                <strong>CoR Link 2 — RoleChecker ({targetEndpointRole}):</strong>
                <p style={{ fontSize: '0.8rem' }}>
                  {trace.roleCheck === 'pass'
                    ? `Role matched target permission. Allowed downstream ✓`
                    : `Forbidden! Endpoint requires ${targetEndpointRole}, user role failed ✗`}
                </p>
              </div>
            </div>

            {/* Final Route Status */}
            <div style={{ marginTop: '0.75rem', padding: '0.5rem 0.75rem', background: trace.httpStatus === 200 ? '#ecfdf5' : '#fef2f2', borderRadius: 6, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.85rem', fontWeight: 600, color: trace.httpStatus === 200 ? '#065f46' : '#991b1b' }}>
                HTTP Final Response: {trace.httpStatus} {trace.httpStatus === 200 ? 'OK — Access Granted' : trace.httpStatus === 401 ? 'Unauthorized' : 'Forbidden'}
              </span>
              <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#78716c' }}>
                Active: {currentSession.email} ({currentSession.role})
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthModal;
