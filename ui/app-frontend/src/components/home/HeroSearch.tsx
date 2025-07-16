// src/components/home/HeroSearch.tsx
import Image from "next/image";
import { Button } from "../ui/Button";
import { Input } from "../ui/Input";
import { Search } from "lucide-react";

export function HeroSearch() {
  return (
    <section className="container mx-auto px-4 md:px-6 py-8">
      {/* Banner Promocional */}
      <div className="relative w-full h-48 md:h-64 rounded-xl overflow-hidden mb-8">
        <Image
          src="/images/teleconsulta-banner.jpg"
          alt="Banner de teleconsulta"
          fill
          className="object-cover"
        />
        <div className="absolute inset-0 bg-black/30 flex flex-col items-start justify-center p-6 md:p-10">
          <h2 className="text-white text-2xl md:text-4xl font-bold max-w-md">
            Teleconsulta a partir de R$29,90
          </h2>
          <Button size="lg" className="mt-4">
            Agendar
          </Button>
        </div>
      </div>

      {/* Área de Busca */}
      <div className="max-w-3xl mx-auto">
        <h3 className="text-center text-xl font-semibold text-slate-800 mb-4">
          Orçamento ou Agendamento
        </h3>
        <div className="flex flex-col md:flex-row gap-2">
          <Input
            type="text"
            placeholder="Busque por consultas, exames, médicos, clínicas..."
            className="py-3 h-auto text-base"
            icon={<Search />}
            label="" // Deixamos o label vazio para um look mais limpo
          />
          <Button size="lg" className="md:h-auto">Buscar</Button>
        </div>
      </div>
    </section>
  );
}