// src/components/layout/DashboardLayout.tsx
import React from "react";
import { SidebarNav } from "./SidebarNav";

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      {/* Sidebar Fixa para Desktop (escondida em telas menores) */}
      <aside className="hidden lg:block fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 border-r border-slate-200">
        <SidebarNav />
      </aside>

      {/* Área de Conteúdo Principal */}
      {/* Adicionamos um padding à esquerda em telas grandes para não ficar embaixo da sidebar */}
      <main className="lg:pl-64">
        <div className="p-4 sm:p-6 lg:p-8">
          {children}
        </div>
      </main>
    </div>
  );
}