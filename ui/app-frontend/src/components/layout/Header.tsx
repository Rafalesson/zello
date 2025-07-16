// src/components/layout/Header.tsx
"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { Button } from "@/components/ui/Button";
// O LoginModal não é mais necessário aqui
// import { LoginModal } from "../auth/LoginModal"; 

export function Header() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <header className="bg-white border-b border-slate-200">
      <nav className="container mx-auto px-4 sm:px-6 lg:px-8" aria-label="Top">
        <div className="w-full py-4 flex items-center justify-between">
          <div className="flex items-center">
            <Link href="/" className="font-serif text-2xl font-bold text-slate-800">
              Zello
            </Link>
          </div>
          <div className="ml-10 space-x-4">
            {isAuthenticated ? (
              // Se o usuário estiver autenticado, mostra Dashboard e Sair
              <>
                <Link href="/dashboard">
                   <Button variant="ghost" size="sm">Dashboard</Button>
                </Link>
                <Button onClick={logout} variant="secondary" size="sm">Sair</Button>
              </>
            ) : (
              // Se não estiver autenticado, não renderiza nada no header.
              // O botão principal estará na home page.
              null 
            )}
          </div>
        </div>
      </nav>
    </header>
  );
}