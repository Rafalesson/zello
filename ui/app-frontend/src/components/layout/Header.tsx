// src/components/layout/Header.tsx
"use client";
    
import Link from "next/link";
import Image from "next/image";
import { useAuth } from "@/context/AuthContext";
import { LoginModal } from "../auth/LoginModal";
import { HeartPulse, MessageCircle, User as UserIcon, Menu, LayoutDashboard } from "lucide-react";
import { Sheet, SheetContent, SheetTrigger } from "../ui/Sheet";
import { SidebarNav } from "./SidebarNav";

export function Header() {
  const { isAuthenticated, user } = useAuth();

  const renderAvatar = () => {
    if (user?.foto_perfil_url) {
      return <Image src={user.foto_perfil_url} alt="Foto do perfil" fill className="object-cover" />;
    }
    if (user?.sexo === 'MASCULINO') {
      return <UserIcon className="h-6 w-6 text-slate-500" />;
    }
    // Para outros casos (Feminino, Outro, ou não definido), usamos um ícone neutro/padrão
    return <UserIcon className="h-6 w-6 text-slate-500" />;
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-white/80 backdrop-blur-lg">
      <div className="relative flex h-16 items-center justify-between px-4 md:px-8">
        
        {/* LADO ESQUERDO: Visível apenas em telas grandes (desktop) */}
        <div className="hidden lg:flex">
          <Link href={isAuthenticated ? "/dashboard" : "/"} className="flex items-center gap-2">
            <HeartPulse className="h-7 w-7 text-slate-800" />
            <span className="font-serif text-2xl font-bold text-slate-800">Zello</span>
          </Link>
        </div>

        {/* LADO ESQUERDO (MOBILE): Ocupa espaço para balancear o layout */}
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
          
          {isAuthenticated && user ? (
            <>
              <Link href="/dashboard" className="hidden lg:block text-slate-600 hover:text-slate-900" aria-label="Acessar Dashboard">
                <LayoutDashboard className="h-6 w-6" />
              </Link>
              <Link href="/perfil">
                <div className="relative h-9 w-9 overflow-hidden rounded-full bg-slate-200 flex items-center justify-center">
                  {renderAvatar()}
                </div>
              </Link>
            </>
          ) : (
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