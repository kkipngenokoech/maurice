const features = [
  ["Voice notes", "Talk it through. Send a voice note when typing would take longer."],
  ["Calendar · in testing", "Ask what’s coming up and get the answer right in the chat."],
  ["Gmail · in testing", "Catch up on unread email across the Google accounts you connect."],
];

export default function Home() {
  return (
    <div className="site">
      <header className="top">
        <a className="brand" href="/" aria-label="Maurice home"><span aria-hidden="true">m</span> Maurice</a>
        <a className="source" href="https://github.com/kkipngenokoech/maurice">GitHub ↗</a>
      </header>

      <main>
        <section className="hero" aria-labelledby="intro">
          <div className="intro">
            <p className="label"><span className="dot" /> A personal assistant for WhatsApp</p>
            <h1 id="intro">A little help.<br /><em>One chat away.</em></h1>
            <p className="lede">Ask what’s on your calendar, catch up on email, or send a voice note when your hands are full.</p>
            <a className="action" href="#features">What Maurice can do <span aria-hidden="true">↓</span></a>
          </div>

          <figure className="demo">
            <div className="paper">
              <div className="chat-title"><span className="avatar" aria-hidden="true">m</span><span><strong>Maurice</strong><small>Example conversation</small></span></div>
              <div className="chat">
                <p className="date">MONDAY MORNING</p>
                <div className="bubble outgoing">What’s on my calendar this morning?</div>
                <div className="bubble incoming">Two things before lunch.<br /><br /><strong>09:30</strong> &nbsp; Team check-in<br /><strong>11:00</strong> &nbsp; Call with Sam</div>
                <div className="bubble outgoing voice"><svg viewBox="0 0 100 24" width="100" height="24" fill="none" aria-hidden="true"><path d="M4 10v4m8-8v12m8-15v18m8-11v4m8-6v8m8-13v18m8-16v14m8-10v6m8-12v18m8-13v8m8-7v6m8-5v4" stroke="currentColor" strokeWidth="3" strokeLinecap="round"/></svg><span>Voice note · 0:08</span></div>
              </div>
            </div>
            <figcaption>From the morning calendar to a quick voice note.</figcaption>
          </figure>
        </section>

        <section className="features" id="features" aria-labelledby="features-title">
          <h2 id="features-title">What you can ask about</h2>
          <div className="feature-grid">
            {features.map(([title, description]) => (
              <article key={title}><h3>{title}</h3><p>{description}</p></article>
            ))}
          </div>
        </section>
      </main>

      <footer><span>Maurice</span><a href="https://kipngenokoech.com">Built by Kipngeno Koech ↗</a></footer>
    </div>
  );
}
