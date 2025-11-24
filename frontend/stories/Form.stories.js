export default {
  title: 'Components/Form',
  tags: ['autodocs'],
}

export const FormGroup = () => `
  <div class="form-group">
    <label class="form-label" for="example-input">Username</label>
    <input type="text" id="example-input" class="form-input" placeholder="Enter username">
    <span class="form-helptext">Your unique username for logging in</span>
  </div>
`

export const FormGroupWithError = () => `
  <div class="form-group">
    <label class="form-label" for="error-input">Email</label>
    <input type="email" id="error-input" class="form-input" value="invalid-email">
    <ul class="errorlist">
      <li>Enter a valid email address</li>
    </ul>
  </div>
`

export const LoginForm = () => `
  <div class="card" style="max-width: 400px;">
    <h2 class="heading-2">Login</h2>

    <form>
      <div class="form-group">
        <label class="form-label" for="username">Username</label>
        <input type="text" id="username" class="form-input" placeholder="Enter username">
      </div>

      <div class="form-group">
        <label class="form-label" for="password">Password</label>
        <input type="password" id="password" class="form-input" placeholder="Enter password">
      </div>

      <button type="submit" class="btn btn--primary">Login</button>
    </form>

    <p style="margin-top: 1rem;">
      Don't have an account? <a href="#" class="link">Sign up here</a>
    </p>
  </div>
`

export const SignupForm = () => `
  <div class="card" style="max-width: 400px;">
    <h2 class="heading-2">Sign Up</h2>

    <form>
      <div class="form-group">
        <label class="form-label" for="signup-username">Username</label>
        <input type="text" id="signup-username" class="form-input">
        <span class="form-helptext">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span>
      </div>

      <div class="form-group">
        <label class="form-label" for="signup-password1">Password</label>
        <input type="password" id="signup-password1" class="form-input">
        <span class="form-helptext">Your password must contain at least 8 characters.</span>
      </div>

      <div class="form-group">
        <label class="form-label" for="signup-password2">Password confirmation</label>
        <input type="password" id="signup-password2" class="form-input">
        <span class="form-helptext">Enter the same password as before, for verification.</span>
      </div>

      <button type="submit" class="btn btn--primary">Sign Up</button>
    </form>

    <p style="margin-top: 1rem;">
      Already have an account? <a href="#" class="link">Login here</a>
    </p>
  </div>
`

export const AllInputStates = () => `
  <div style="display: flex; flex-direction: column; gap: 1rem; max-width: 400px;">
    <div class="form-group">
      <label class="form-label">Normal Input</label>
      <input type="text" class="form-input" placeholder="Enter text">
    </div>

    <div class="form-group">
      <label class="form-label">Input with Value</label>
      <input type="text" class="form-input" value="Some text value">
    </div>

    <div class="form-group">
      <label class="form-label">Disabled Input</label>
      <input type="text" class="form-input" value="Disabled" disabled>
    </div>

    <div class="form-group">
      <label class="form-label">Input with Helptext</label>
      <input type="text" class="form-input" placeholder="example@email.com">
      <span class="form-helptext">We'll never share your email with anyone else.</span>
    </div>

    <div class="form-group">
      <label class="form-label">Input with Error</label>
      <input type="text" class="form-input" value="invalid">
      <ul class="errorlist">
        <li>This field is required</li>
      </ul>
    </div>
  </div>
`
