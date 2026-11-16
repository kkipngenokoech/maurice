import Image from "next/image";

const integrations = [
  ["Gmail", "In testing", "Catch up on unread email across your connected inboxes."],
  ["Google Calendar", "In testing", "See what’s on your calendar. Scheduling tasks on request is planned."],
  ["Notion", "Planned", "Save notes and to-dos from your WhatsApp conversations."],
  ["Granola", "Planned", "Bring in meeting notes and turn action items into tasks."],
];

export default function Home() {
  return (
    <div className="site">
      <header className="top">
        <a className="brand" href="/" aria-label="Maurice home"><Logo /> Maurice</a>
        <a className="source" href="https://github.com/kkipngenokoech/maurice">GitHub ↗</a>
      </header>

      <main>
        <section className="hero" aria-labelledby="intro">
          <div className="intro">
            <p className="label"><span className="dot" /> A personal assistant for WhatsApp</p>
            <h1 id="intro">A little help.<br /><em>One chat away.</em></h1>
            <p className="lede">Ask what’s on your calendar, catch up on email, or send a voice note when your hands are full.</p>
            <a className="action" href="#features">See how Maurice works <span aria-hidden="true">↓</span></a>
          </div>

          <figure className="demo">
            <div className="paper">
              <div className="chat-title"><Logo /><span><strong>Maurice</strong><small>Example conversation</small></span></div>
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
          <h2 id="features-title">How Maurice works</h2>
          <div className="workflow">
            <div className="workflow-path">
              <div><strong>WhatsApp</strong><span>Send a text or voice note. Get a reply in chat.</span></div>
              <span className="workflow-arrow" aria-hidden="true">↔</span>
              <div><strong>Maurice</strong><span>Uses the connected apps that your request needs.</span></div>
            </div>
            <div className="workflow-connector" aria-hidden="true">↓</div>
            <ul className="feature-grid" aria-label="Integrations">
              {integrations.map(([title, status, description]) => (
                <li key={title}><h3>{title}</h3><span className="integration-status">{status}</span><p>{description}</p></li>
              ))}
            </ul>
          </div>
          <p className="workflow-brief"><strong>Planned:</strong> One WhatsApp briefing with unread email, upcoming events, and tasks due.</p>
        </section>
      </main>

      <footer><span>Maurice</span><a href="https://kipngenokoech.com">Built by Kipngeno Koech ↗</a></footer>
    </div>
  );
}

function Logo() {
  return <Image className="logo" src="/maurice-logo-black.png" alt="" width={34} height={34} unoptimized />;
}
