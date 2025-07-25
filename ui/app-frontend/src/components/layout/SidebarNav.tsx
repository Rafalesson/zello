// src/components/layout/SidebarNav.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { twMerge } from "tailwind-merge";
import { clsx } from "clsx";
import { 
  LayoutDashboard, 
  CalendarPlus, 
  History, 
  User, 
  LogOut 
} from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { UserProfile } from "./UserProfile";

interface NavItem {
  href: string;
  label: string;
  icon: React.ReactNode;
}

export function SidebarNav() {
  const pathname = usePathname();
  const { logout } = useAuth();

  const navItems: NavItem[] = [
    { href: "/dashboard", label: "Visão Geral", icon: <LayoutDashboard className="h-5 w-5" /> },
    { href: "/buscar", label: "Agendar Consulta", icon: <CalendarPlus className="h-5 w-5" /> },
    { href: "/meus-agendamentos", label: "Meus Agendamentos", icon: <History className="h-5 w-5" /> },
    { href: "/perfil", label: "Meu Perfil", icon: <User className="h-5 w-5" /> },
  ];

  return (
    // A classe 'rounded-xl' foi removida
    <div className="flex flex-col h-full bg-white shadow-sm border border-slate-200">
      <UserProfile />

      <nav className="flex-grow p-4">
        <ul className="space-y-1">
          {navItems.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                className={twMerge(
                  clsx(
                    "flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md transition-colors",
                    pathname === item.href
                      ? "bg-slate-900 text-white"
                      : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                  )
                )}
              >
                {item.icon}
                <span>{item.label}</span>
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      <div className="p-4 border-t border-slate-200">
        <button
          onClick={logout}
          className="flex items-center gap-3 w-full px-3 py-2 text-sm font-medium rounded-md text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-colors"
        >
          <LogOut className="h-5 w-5" />
          <span>Sair</span>
        </button>
      </div>
    </div>
  );
}