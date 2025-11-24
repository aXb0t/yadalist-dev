export default {
  title: 'Components/Card',
  tags: ['autodocs'],
}

export const BasicCard = () => `
  <div class="card" style="max-width: 400px;">
    <h2 class="heading-2">Card Title</h2>
    <p>This is a basic card component with some content inside.</p>
  </div>
`

export const CardWithForm = () => `
  <div class="card" style="max-width: 400px;">
    <h2 class="heading-2">Contact Us</h2>
    <form>
      <div class="form-group">
        <label class="form-label">Name</label>
        <input type="text" class="form-input" placeholder="Your name">
      </div>
      <div class="form-group">
        <label class="form-label">Email</label>
        <input type="email" class="form-input" placeholder="your@email.com">
      </div>
      <div class="form-group">
        <label class="form-label">Message</label>
        <textarea class="form-input" rows="4" placeholder="Your message"></textarea>
      </div>
      <button type="submit" class="btn btn--primary">Send Message</button>
    </form>
  </div>
`

export const ProfileCard = () => `
  <div class="card" style="max-width: 500px;">
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
      <a href="#" class="link">Edit Profile</a>
    </div>
  </div>
`

export const MultipleCards = () => `
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
    <div class="card">
      <h3 class="heading-3">Card 1</h3>
      <p>First card content goes here.</p>
      <button class="btn btn--primary" style="margin-top: 1rem;">Action</button>
    </div>
    <div class="card">
      <h3 class="heading-3">Card 2</h3>
      <p>Second card content goes here.</p>
      <button class="btn btn--secondary" style="margin-top: 1rem;">Action</button>
    </div>
    <div class="card">
      <h3 class="heading-3">Card 3</h3>
      <p>Third card content goes here.</p>
      <button class="btn btn--success" style="margin-top: 1rem;">Action</button>
    </div>
  </div>
`
