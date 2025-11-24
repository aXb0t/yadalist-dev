export default {
  title: 'Layouts/Page Templates',
  tags: ['autodocs'],
}

export const LoginPage = () => `
  <div class="container-card">
    <nav class="nav nav--dark">
      <a href="#" class="nav__link">Home</a>
      <a href="#" class="nav__link">Login</a>
      <a href="#" class="nav__link">Sign Up</a>
    </nav>

    <div class="card" style="max-width: 400px; margin: 0 auto;">
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
  </div>
`

export const ProfilePage = () => `
  <div class="container-card">
    <nav class="nav nav--dark">
      <a href="#" class="nav__link">Home</a>
      <a href="#" class="nav__link">Profile</a>
      <a href="#" class="nav__link">Logout</a>
    </nav>

    <div class="card">
      <ul class="alert-list">
        <li class="alert alert--success">Profile loaded successfully</li>
      </ul>

      <h2 class="heading-2">User Profile</h2>

      <div style="display: flex; flex-direction: column; gap: 0.75rem;">
        <p><strong>Username:</strong> johndoe</p>
        <p><strong>Email:</strong> john.doe@example.com</p>
        <p><strong>First Name:</strong> John</p>
        <p><strong>Last Name:</strong> Doe</p>
        <p><strong>Date Joined:</strong> November 24, 2025</p>
        <p><strong>Last Login:</strong> November 24, 2025 14:30</p>
      </div>

      <div style="margin-top: 1.5rem;">
        <a href="#" class="link">Logout</a>
      </div>
    </div>
  </div>
`

export const PageWithMessages = () => `
  <div class="container-card">
    <nav class="nav nav--dark">
      <a href="#" class="nav__link">Home</a>
      <a href="#" class="nav__link">Profile</a>
      <a href="#" class="nav__link">Logout</a>
    </nav>

    <div class="card">
      <ul class="alert-list">
        <li class="alert alert--success">Changes saved successfully</li>
        <li class="alert alert--info">Email verification sent</li>
        <li class="alert alert--warning">Session will expire in 5 minutes</li>
      </ul>

      <h2 class="heading-2">Page Content</h2>
      <p>Main page content goes here...</p>
    </div>
  </div>
`
