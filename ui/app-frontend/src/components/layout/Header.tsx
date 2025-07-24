// src/components/layout/Header.tsx
"use client";

import Link from "next/link";
import Image from "next/image";
import { useAuth } from "@/context/AuthContext";
import { LoginModal } from "../auth/LoginModal";
import { HeartPulse, MessageCircle, User as UserIcon } from "lucide-react";

export function Header() {
  const { isAuthenticated, user } = useAuth();

  // Define o link do logo com base no estado de autenticação
  const logoHref = isAuthenticated ? "/buscar" : "/";

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-lg">
      <div className="container mx-auto flex h-16 items-center justify-between px-4 md:px-6">
        {/* Lado Esquerdo: Logo com link dinâmico */}
        <Link href={logoHref} className="flex items-center gap-2">
          <HeartPulse className="h-7 w-7 text-slate-800" />
          <span className="font-serif text-2xl font-bold text-slate-800">
            Zello
          </span>
        </Link>

        {/* Lado Direito: Ações */}
        <div className="flex items-center gap-4">
          <a
            href="https://wa.me/5581999999999" // Exemplo de número
            target="_blank"
            rel="noopener noreferrer"
            className="text-slate-600 hover:text-slate-900"
            aria-label="Contato via WhatsApp"
          >
            <MessageCircle className="h-6 w-6" />
          </a>

          {isAuthenticated && user ? (
            // Se ESTÁ logado, mostra a foto do perfil
            <Link href="/dashboard">
              <div className="relative h-9 w-9 overflow-hidden rounded-full bg-slate-200 flex items-center justify-center text-slate-600 font-semibold">
                {user.foto_perfil_url ? (
                  <Image
                    src={user.foto_perfil_url}
                    alt="Foto do perfil"
                    fill
                    className="object-cover"
                  />
                ) : (
                  user.email.charAt(0).toUpperCase()
                )}
              </div>
            </Link>
          ) : (
            // Se NÃO ESTÁ logado, o ícone de perfil abre o modal de login
            <LoginModal>
              <button
                className="text-slate-600 hover:text-slate-900"
                aria-label="Acessar conta"
              >
                <UserIcon className="h-6 w-6" />
              </button>
            </LoginModal>
          )}
        </div>
      </div>
    </header>
  );
}
