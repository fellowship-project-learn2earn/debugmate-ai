function HowItWorks() {
  const steps = [
    {
      number: "01",
      title: "Submit Your Error",
      description:
        "Paste your code and error message into the debugging workspace.",
    },
    {
      number: "02",
      title: "Understand",
      description:
        "Get a clear explanation of what happened and why the error occurred.",
    },
    {
      number: "03",
      title: "Learn & Practice",
      description:
        "Learn the underlying concept and practice with a small challenge.",
    },
  ];

  return (
    <section className="how-it-works" id="how-it-works">
      <div className="section-heading">
        <p className="section-label">HOW IT WORKS</p>

        <h2>From error to understanding.</h2>

        <p>
          DebugMate turns confusing programming errors into guided learning
          experiences.
        </p>
      </div>

      <div className="steps-grid">
        {steps.map((step) => (
          <article className="step-card" key={step.number}>
            <span className="step-number">{step.number}</span>

            <h3>{step.title}</h3>

            <p>{step.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

export default HowItWorks;