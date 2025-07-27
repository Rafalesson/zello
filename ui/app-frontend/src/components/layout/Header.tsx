// src/components/layout/Header.tsx
"use client";
    
import Link from "next/link";
import Image from "next/image";
import { useAuth } from "@/context/AuthContext";
import { LoginModal } from "../auth/LoginModal";
import { ProfileMenu } from "../auth/ProfileMenu";
import { HeartPulse, MessageCircle, User as UserIcon, Menu, LayoutDashboard } from "lucide-react";
import { Sheet, SheetContent, SheetTrigger } from "../ui/Sheet";
import { SidebarNav } from "./SidebarNav";

export function Header() {
  const { isAuthenticated } = useAuth();

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-white/80 backdrop-blur-lg">
      {/* Usamos um grid de 3 colunas para o layout mobile e flex para o desktop */}
      <div className="relative flex h-16 items-center justify-between px-4 md:px-8 lg:px-6">
        
        {/* LADO ESQUERDO (DESKTOP): Logo visível apenas em telas grandes */}
        <div className="hidden lg:flex">
          <Link href={isAuthenticated ? "/dashboard" : "/"} className="flex items-center gap-2">
            <HeartPulse className="h-7 w-7 text-slate-800" />
            <span className="font-serif text-2xl font-bold text-slate-800">
              Zello
            </span>
          </Link>
        </div>

        {/* LADO ESQUERDO (MOBILE): Menu hambúrguer para balancear o layout */}
        <div className="flex justify-start lg:hidden">
          {isAuthenticated && (
            <Sheet>
              <SheetTrigger asChild>
                <button className="text-slate-600 hover:text-slate-900" aria-label="Abrir menu">
                  <Menu className="h-6 w-6" />
                </button>
              </SheetTrigger>
              <SheetContent side="left" className="p-0">
                <SidebarNav />
              </SheetContent>
            </Sheet>
          )}
        </div>

        {/* LOGO CENTRAL (MOBILE): Visível apenas em telas pequenas */}
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 lg:hidden">
          <Link href={isAuthenticated ? "/dashboard" : "/"} className="flex items-center gap-2">
            <HeartPulse className="h-7 w-7 text-slate-800" />
            <span className="font-serif text-2xl font-bold text-slate-800">Zello</span>
          </Link>
        </div>

        {/* LADO DIREITO: Ações */}
        <div className="flex justify-end items-center gap-4 md:gap-6">
          <a href="#" target="_blank" rel="noopener noreferrer" aria-label="Contato">
            <MessageCircle className="h-6 w-6 text-slate-600 hover:text-slate-900" />
          </a>
          
          {isAuthenticated ? (
            // Se o usuário está logado, renderiza o ícone de dashboard e o menu de perfil
            <div className="flex items-center gap-4">
                <Link href="/dashboard" className="text-slate-600 hover:text-slate-900 transition-colors" aria-label="Acessar Dashboard">
                    <LayoutDashboard className="h-6 w-6" />
                </Link>
                <ProfileMenu />
            </div>
          ) : (
            // Se não está logado, renderiza o ícone que abre o modal de login
            <LoginModal>
              <button className="text-slate-600 hover:text-slate-900" aria-label="Acessar conta">
                <UserIcon className="h-6 w-6" />
              </button>
            </LoginModal>
          )}
        </div>

      </div>
    </header>
  );
}