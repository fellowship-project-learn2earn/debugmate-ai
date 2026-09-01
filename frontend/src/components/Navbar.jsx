function Navbar() {
  return (
    <nav className="navbar">
      <a href="/" className="navbar-logo" aria-label="DebugMate home">
        <span className="logo-mark">✦</span>
        <span>DebugMate</span>
        <span className="logo-badge">AI</span>
      </a>

      <div className="navbar-links">
        <a href="#how-it-works">How It Works</a>
        <a href="#about">About</a>
        <a href="#debug" className="nav-cta">
          Start Debugging
          <span>↗</span>
        </a>
      </div>
    </nav>
  );
}

export default Navbar;