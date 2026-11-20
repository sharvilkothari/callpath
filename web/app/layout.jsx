import "./globals.css";
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";

export const metadata = {
  title: "CallPath · SIP and RTP workbench",
  description: "Run isolated Asterisk experiments and compare SIP and RTP evidence.",
};

export default function Layout({ children }) {
  return <html lang="en" className={`${GeistSans.variable} ${GeistMono.variable}`}><body>{children}</body></html>;
}
