import type { Metadata } from "next";
import { Space_Grotesk } from "next/font/google";
import { InterviewProvider } from "@/context/InterviewContext";
import "./globals.css";

const spaceGrotesk = Space_Grotesk({
  variable: "--font-space-grotesk",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "VocalAce | AI-Powered Mock Interview Platform",
  description: "Advanced speech analysis and transcription for interview preparation",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
          rel="stylesheet"
        />
      </head>
      <body
        className={`${spaceGrotesk.variable} font-sans antialiased bg-white dark:bg-background-dark text-slate-900 dark:text-white`}
      >
        <InterviewProvider>
          {children}
        </InterviewProvider>
      </body>
    </html>
  );
}
