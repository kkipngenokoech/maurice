import "./style.css";

export const metadata = {
  title: "Maurice — A little help in WhatsApp",
  description: "Maurice is a personal assistant for WhatsApp. Send a message or a voice note, check your calendar, and catch up on email.",
};

export default function Layout({ children }) {
  return <html lang="en"><body>{children}</body></html>;
}
