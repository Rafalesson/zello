// src/components/layout/UserProfile.tsx
"use client";

import { useAuth } from "@/context/AuthContext";
import Image from "next/image";
import { User as UserMale, UserRound as UserFemale } from "lucide-react";

export function UserProfile() {
  const { user } = useAuth();

  // Se o usuário ainda não foi carregado, não renderiza nada
  if (!user) return null;

  const renderAvatar = () => {
    if (user.foto_perfil_url) {
      return <Image src={user.foto_perfil_url} alt="Foto do perfil" fill className="object-cover" />;
    }
    if (user.sexo === 'MASCULINO') {
      return <UserMale className="h-6 w-6 text-slate-500" />;
    }
    return <UserFemale className="h-6 w-6 text-slate-500" />;
  };

  return (
    <div className="flex items-center gap-4 p-4 border-b border-slate-200">
      <div className="relative h-12 w-12 overflow-hidden rounded-full bg-slate-100 flex items-center justify-center">
        {renderAvatar()}
      </div>
      <div className="flex flex-col">
        <span className="font-semibold text-sm text-slate-800 truncate">
          {/* No futuro, teremos o nome do usuário aqui */}
          {user.email}
        </span>
        <span className="text-xs text-slate-500 capitalize">
          {user.tipo_usuario.toLowerCase()}
        </span>
      </div>
    </div>
  );
}