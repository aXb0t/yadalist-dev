export default {
  title: 'Pages/Capture',
  tags: ['autodocs'],
}

export const CapturePage = () => `
  <div class="container-card">
    <nav class="nav nav--dark">
      <a href="#" class="nav__link">Home</a>
      <a href="#" class="nav__link nav__link--active">Capture</a>
      <a href="#" class="nav__link">Items</a>
      <a href="#" class="nav__link">Logout</a>
    </nav>

    <div class="card">
      <h2 class="heading-2">Capture Item</h2>

      <!-- Image Grid Area -->
      <div style="margin-bottom: 1.5rem;">
        <label class="form-label">Photos (0/20)</label>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 0.75rem; margin-bottom: 0.75rem;">
          <!-- Placeholder for images will be added dynamically -->
          <div style="border: 2px dashed var(--nord4); border-radius: 0.5rem; aspect-ratio: 1; display: flex; align-items: center; justify-content: center; cursor: pointer; background: var(--nord6);">
            <span style="color: var(--nord3); font-size: 2rem;">+</span>
          </div>
        </div>
        <input type="file" id="image-upload" accept="image/*" multiple style="display: none;">
        <button type="button" class="btn btn--secondary" onclick="document.getElementById('image-upload').click()">
          Add Photos
        </button>
        <span class="form-helptext">Upload up to 20 images. Click existing images to remove.</span>
      </div>

      <!-- Voice Transcript Textarea -->
      <div class="form-group">
        <label class="form-label" for="voice-transcript">Notes / Voice Transcript</label>
        <textarea
          id="voice-transcript"
          class="form-input"
          rows="6"
          placeholder="Describe the item... or use voice input"
          style="resize: vertical; min-height: 120px;"
        ></textarea>
        <span class="form-helptext">Auto-saves as you type. Speak naturally - AI will process later.</span>
      </div>

      <!-- Action Buttons -->
      <div style="display: flex; gap: 0.75rem; margin-top: 1.5rem;">
        <button type="button" class="btn btn--primary">Next Item</button>
        <button type="button" class="btn btn--secondary">Save & Exit</button>
      </div>
    </div>
  </div>
`

export const CapturePageWithImages = () => `
  <div class="container-card">
    <nav class="nav nav--dark">
      <a href="#" class="nav__link">Home</a>
      <a href="#" class="nav__link nav__link--active">Capture</a>
      <a href="#" class="nav__link">Items</a>
      <a href="#" class="nav__link">Logout</a>
    </nav>

    <div class="card">
      <h2 class="heading-2">Capture Item</h2>

      <!-- Image Grid Area with Sample Images -->
      <div style="margin-bottom: 1.5rem;">
        <label class="form-label">Photos (3/20)</label>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 0.75rem; margin-bottom: 0.75rem;">
          <!-- Sample image placeholders -->
          <div style="position: relative; border-radius: 0.5rem; aspect-ratio: 1; background: var(--nord3); cursor: pointer;">
            <div style="position: absolute; top: 4px; right: 4px; background: var(--nord11); color: white; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.875rem; font-weight: bold;">×</div>
          </div>
          <div style="position: relative; border-radius: 0.5rem; aspect-ratio: 1; background: var(--nord3); cursor: pointer;">
            <div style="position: absolute; top: 4px; right: 4px; background: var(--nord11); color: white; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.875rem; font-weight: bold;">×</div>
          </div>
          <div style="position: relative; border-radius: 0.5rem; aspect-ratio: 1; background: var(--nord3); cursor: pointer;">
            <div style="position: absolute; top: 4px; right: 4px; background: var(--nord11); color: white; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.875rem; font-weight: bold;">×</div>
          </div>
          <div style="border: 2px dashed var(--nord4); border-radius: 0.5rem; aspect-ratio: 1; display: flex; align-items: center; justify-content: center; cursor: pointer; background: var(--nord6);">
            <span style="color: var(--nord3); font-size: 2rem;">+</span>
          </div>
        </div>
        <input type="file" id="image-upload" accept="image/*" multiple style="display: none;">
        <button type="button" class="btn btn--secondary" onclick="document.getElementById('image-upload').click()">
          Add Photos
        </button>
        <span class="form-helptext">Upload up to 20 images. Click × to remove images.</span>
      </div>

      <!-- Voice Transcript Textarea with Content -->
      <div class="form-group">
        <label class="form-label" for="voice-transcript">Notes / Voice Transcript</label>
        <textarea
          id="voice-transcript"
          class="form-input"
          rows="6"
          placeholder="Describe the item... or use voice input"
          style="resize: vertical; min-height: 120px;"
        >Vintage brass compass, looks nautical, has some patina, maker's mark on back says "Made in England", diameter about 3 inches, works perfectly</textarea>
        <span class="form-helptext">Auto-saves as you type. Speak naturally - AI will process later.</span>
      </div>

      <!-- Action Buttons -->
      <div style="display: flex; gap: 0.75rem; margin-top: 1.5rem;">
        <button type="button" class="btn btn--primary">Next Item</button>
        <button type="button" class="btn btn--secondary">Save & Exit</button>
      </div>
    </div>
  </div>
`

export const CapturePageMobile = () => `
  <div class="container-card" style="max-width: 375px;">
    <nav class="nav nav--dark">
      <a href="#" class="nav__link">Home</a>
      <a href="#" class="nav__link nav__link--active">Capture</a>
      <a href="#" class="nav__link">Items</a>
    </nav>

    <div class="card">
      <h2 class="heading-2">Capture Item</h2>

      <!-- Image Grid Area (Mobile) -->
      <div style="margin-bottom: 1.5rem;">
        <label class="form-label">Photos (2/20)</label>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin-bottom: 0.75rem;">
          <div style="position: relative; border-radius: 0.5rem; aspect-ratio: 1; background: var(--nord3); cursor: pointer;">
            <div style="position: absolute; top: 4px; right: 4px; background: var(--nord11); color: white; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.875rem; font-weight: bold;">×</div>
          </div>
          <div style="position: relative; border-radius: 0.5rem; aspect-ratio: 1; background: var(--nord3); cursor: pointer;">
            <div style="position: absolute; top: 4px; right: 4px; background: var(--nord11); color: white; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.875rem; font-weight: bold;">×</div>
          </div>
          <div style="border: 2px dashed var(--nord4); border-radius: 0.5rem; aspect-ratio: 1; display: flex; align-items: center; justify-content: center; cursor: pointer; background: var(--nord6);">
            <span style="color: var(--nord3); font-size: 1.5rem;">+</span>
          </div>
        </div>
        <button type="button" class="btn btn--secondary" style="width: 100%;">
          Add Photos
        </button>
      </div>

      <!-- Voice Transcript Textarea (Mobile) -->
      <div class="form-group">
        <label class="form-label" for="voice-transcript">Notes</label>
        <textarea
          id="voice-transcript"
          class="form-input"
          rows="4"
          placeholder="Describe the item..."
          style="resize: vertical; min-height: 100px;"
        ></textarea>
      </div>

      <!-- Action Buttons (Mobile) -->
      <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-top: 1rem;">
        <button type="button" class="btn btn--primary" style="width: 100%;">Next Item</button>
        <button type="button" class="btn btn--secondary" style="width: 100%;">Save & Exit</button>
      </div>
    </div>
  </div>
`
