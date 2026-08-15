function Navbar() {
  return (
    <nav className="navbar">
      <a href="/" className="navbar-logo">
        DebugMate
      </a>

      <div className="navbar-links">
        <a href="#how-it-works">How It Works</a>
        <a href="#about">About</a>
        <a href="#debug">Get Started</a>
      </div>
    </nav>
  );
}

export default Navbar;