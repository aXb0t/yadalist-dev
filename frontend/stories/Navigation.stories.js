export default {
  title: 'Components/Navigation',
  tags: ['autodocs'],
}

export const NavbarAuthenticated = () => `
  <nav class="nav nav--dark">
    <a href="#" class="nav__link">Home</a>
    <a href="#" class="nav__link">Profile</a>
    <a href="#" class="nav__link">Logout</a>
  </nav>
`

export const NavbarUnauthenticated = () => `
  <nav class="nav nav--dark">
    <a href="#" class="nav__link">Home</a>
    <a href="#" class="nav__link">Login</a>
    <a href="#" class="nav__link">Sign Up</a>
  </nav>
`

export const NavbarWithManyLinks = () => `
  <nav class="nav nav--dark">
    <a href="#" class="nav__link">Home</a>
    <a href="#" class="nav__link">Dashboard</a>
    <a href="#" class="nav__link">Projects</a>
    <a href="#" class="nav__link">Team</a>
    <a href="#" class="nav__link">Settings</a>
    <a href="#" class="nav__link">Profile</a>
    <a href="#" class="nav__link">Logout</a>
  </nav>
`
