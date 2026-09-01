function HowItWorks() {
  const steps = [
    {
      number: "01",
      title: "Submit Your Error",
      description:
        "Choose your programming language, then paste your code and error message into the debugging workspace.",
    },
    {
      number: "02",
      title: "Understand What Happened",
      description:
        "DebugMate analyzes the error and explains what went wrong and why it happened in clear language.",
    },
    {
      number: "03",
      title: "Fix & Learn",
      description:
        "Get practical correction guidance, corrected code, and a learning point you can apply to future problems.",
    },
  ];

  return (
    <section className="how-it-works" id="how-it-works">
      <div className="section-heading">
        <span className="eyebrow">HOW IT WORKS</span>

        <h2>From error to understanding.</h2>

        <p>
          DebugMate turns confusing programming errors into structured,
          learner-friendly explanations.
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