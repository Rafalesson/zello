// src/app/layout.tsx
import "./globals.css";
import type { Metadata } from "next";
import { Inter, Playfair_Display } from "next/font/google"; // 1. Importe Playfair_Display
import { AuthProvider } from "@/context/AuthContext";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";

// 2. Configure ambas as fontes
const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-playfair" });

export const metadata: Metadata = {
  title: "Zello",
  description: "Sua saúde conectada",
};

export default function RootLayout({ children }: { children: React.ReactNode; }) {
  return (
    // 3. Aplique as variáveis de fonte ao body
    <html lang="pt-BR" className="h-full bg-slate-100">
      <body className={`${inter.variable} ${playfair.variable} h-full font-sans`}>
        <AuthProvider>
          <div className="flex flex-col min-h-screen">
            <Header />
            <main className="flex-grow container mx-auto p-4 sm:p-6 lg:p-8">
              {children}
            </main>
            <Footer />
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}