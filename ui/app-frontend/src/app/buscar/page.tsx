// src/app/buscar/page.tsx
"use client";

import { CategoryCard } from "@/components/home/CategoryCard";
import { HeroSearch } from "@/components/home/HeroSearch";
import { ClipboardPlus, Video, Scan } from "lucide-react";

export default function BuscarPage() {
  // Dados para os cards de categoria
  const teleconsultas = {
    icon: <Video className="h-8 w-8" />,
    title: "Teleconsulta",
    items: ["Psicólogo", "Nutricionista", "Dermatologista", "Endocrinologista", "Clínico Geral"],
  };

  const consultasPresenciais = {
    icon: <ClipboardPlus className="h-8 w-8" />,
    title: "Consultas Presenciais",
    items: ["Oftalmologista", "Clínico Geral", "Dermatologista"],
  };

  const exames = {
    icon: <Scan className="h-8 w-8" />,
    title: "Exames de Imagem",
    items: ["Radiografia Tórax", "Ecografia Aparelho Urinário", "Ecografia Transvaginal", "Raio X Joelho"],
  };

  return (
    // Removemos o padding do layout principal para que as seções controlem seu próprio espaço
    <div className="-mx-4 sm:-mx-6 lg:-mx-8">
      {/* Componente que contém o Banner e a Barra de Busca Principal */}
      <HeroSearch />

      {/* Seção de "Mais Procurados" */}
      <section className="container mx-auto px-4 md:px-6 py-12">
        <h2 className="text-2xl font-bold text-slate-800 mb-6">
          Mais procurados
        </h2>
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          <CategoryCard {...consultasPresenciais} />
          <CategoryCard {...teleconsultas} />
          <CategoryCard {...exames} />
        </div>
      </section>
    </div>
  );
}