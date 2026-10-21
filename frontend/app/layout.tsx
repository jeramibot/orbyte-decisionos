import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { title: 'DecisionOS · A clearer way to run your business', description: 'Synthetic SME procurement decisions with human approval.' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
