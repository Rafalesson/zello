// src/components/auth/ProfileMenu.tsx
"use client";

import { useAuth } from "@/context/AuthContext";
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuGroup, 
  DropdownMenuItem, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from "../ui/DropdownMenu";
import Image from "next/image";
import { User as UserIcon, LogOut, Settings } from "lucide-react";
import Link from "next/link";

export function ProfileMenu() {
  const { user, logout } = useAuth();

  // Verificação de segurança: não renderiza nada se o usuário não estiver carregado.
  // Isso resolve o erro 'User is not defined' que tivemos antes.
  if (!user) {
    return null;
  }

  const renderAvatar = () => {
    if (user.foto_perfil_url) {
      return <Image src={user.foto_perfil_url} alt="Foto do perfil" fill className="object-cover" />;
    }
    return <UserIcon className="h-6 w-6 text-slate-500" />;
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button className="relative h-9 w-9 overflow-hidden rounded-full bg-slate-200 flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-slate-950 focus:ring-offset-2">
          {renderAvatar()}
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end">
        <DropdownMenuGroup>
          <div className="px-2 py-1.5">
            <p className="text-sm font-semibold truncate">Olá, {user.email.split('@')[0]}</p>
            <p className="text-xs text-slate-500 truncate">{user.email}</p>
          </div>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <Link href="/perfil">
            <DropdownMenuItem>
              <UserIcon className="mr-2 h-4 w-4" />
              <span>Meu Perfil</span>
            </DropdownMenuItem>
          </Link>
          <Link href="/configuracoes">
            <DropdownMenuItem>
              <Settings className="mr-2 h-4 w-4" />
              <span>Configurações</span>
            </DropdownMenuItem>
          </Link>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={logout}>
          <LogOut className="mr-2 h-4 w-4" />
          <span>Sair</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}