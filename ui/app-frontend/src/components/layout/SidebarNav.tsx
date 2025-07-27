// src/components/layout/SidebarNav.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { twMerge } from "tailwind-merge";
import { clsx } from "clsx";
import { LogOut } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { UserProfile } from "./UserProfile";
// CORREÇÃO: A importação agora aponta para o arquivo .tsx
import { navConfig } from "@/config/dashboardNav.tsx"; 

export function SidebarNav() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const navItems = user?.tipo_usuario ? navConfig[user.tipo_usuario] : [];

  return (
    <div className="flex flex-col h-full bg-white rounded-xl shadow-sm border border-slate-200">
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