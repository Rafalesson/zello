// src/config/dashboardNav.ts
import { 
  LayoutDashboard, 
  CalendarPlus, 
  History, 
  User, 
  Shield, 
  Users 
} from "lucide-react";
import React from "react";

// Define a estrutura de um item de navegação para garantir a consistência
export interface NavItem {
  href: string;
  label: string;
  icon: React.ReactNode;
}

// Objeto de configuração que mapeia um tipo de usuário para sua lista de links
export const navConfig: Record<string, NavItem[]> = {
  PACIENTE: [
    { href: "/dashboard", label: "Visão Geral", icon: <LayoutDashboard className="h-5 w-5" /> },
    { href: "/buscar", label: "Agendar Consulta", icon: <CalendarPlus className="h-5 w-5" /> },
    { href: "/meus-agendamentos", label: "Meus Agendamentos", icon: <History className="h-5 w-5" /> },
    { href: "/perfil", label: "Meu Perfil", icon: <User className="h-5 w-5" /> },
  ],
  MEDICO: [
    // Links para o dashboard do médico (a serem implementados)
    { href: "/dashboard/agenda", label: "Minha Agenda", icon: <CalendarPlus className="h-5 w-5" /> },
    { href: "/dashboard/pacientes", label: "Meus Pacientes", icon: <Users className="h-5 w-5" /> },
    { href: "/perfil", label: "Meu Perfil", icon: <User className="h-5 w-5" /> },
  ],
  ADMIN: [
    // Links para o dashboard do administrador (a serem implementados)
    { href: "/admin/dashboard", label: "Painel Geral", icon: <LayoutDashboard className="h-5 w-5" /> },
    { href: "/admin/usuarios", label: "Gerenciar Usuários", icon: <Users className="h-5 w-5" /> },
    { href: "/admin/configuracoes", label: "Configurações", icon: <Shield className="h-5 w-5" /> },
  ],
};