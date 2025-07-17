// src/app/buscar/page.tsx
"use client";

import { CategoryCard } from "@/components/home/CategoryCard";
import { Carousel, CarouselItem } from "@/components/ui/Carousel";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Search, ClipboardPlus, Video, Scan } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export default function BuscarPage() {
  const slides = [
    { image: "/images/banner-teleconsulta.jpg", title: "Teleconsulta a partir de R$29,90", buttonText: "Agendar Agora", href: "#" },
    { image: "/images/banner-exames.jpg", title: "Exames Laboratoriais em Casa", buttonText: "Ver Opções", href: "#" },
    { image: "/images/banner-saude-mental.jpg", title: "Cuide da Sua Saúde Mental", buttonText: "Falar com um Psicólogo", href: "#" }
  ];

  const teleconsultas = { icon: <Video className="h-8 w-8 text-slate-700" />, title: "Teleconsulta", items: ["Psicólogo", "Nutricionista", "Dermatologista", "Endocrinologista", "Clínico Geral"] };
  const consultasPresenciais = { icon: <ClipboardPlus className="h-8 w-8 text-slate-700" />, title: "Consultas Presenciais", items: ["Oftalmologista", "Clínico Geral", "Dermatologista"] };
  const exames = { icon: <Scan className="h-8 w-8 text-slate-700" />, title: "Exames de Imagem", items: ["Radiografia Tórax", "Ecografia Aparelho Urinário", "Tomografia de Tórax"] };

  return (
    <div className="-mx-4 sm:-mx-6 lg:-mx-8">
      {/* Seção 1: Carrossel de Serviços */}
      <section className="container mx-auto px-4 md:px-6 mb-8 pt-4">
        <Carousel options={{ align: "start" }}>
          {slides.map((slide, index) => (
            <CarouselItem key={index}>
              <div className="relative w-full h-48 md:h-64 rounded-xl overflow-hidden">
                <Image src={slide.image} alt={slide.title} fill className="object-cover" />
                {/* AJUSTE FINAL: Aumentamos o padding horizontal (px-10 md:px-24) para dar mais espaço para as setas */}
                <div className="absolute inset-0 bg-black/40 flex flex-col items-start justify-center p-6 md:p-10 px-10 md:px-24">
                  <h2 className="text-white text-2xl md:text-4xl font-bold max-w-md">{slide.title}</h2>
                  <Link href={slide.href}>
                    <Button size="lg" className="mt-4">{slide.buttonText}</Button>
                  </Link>
                </div>
              </div>
            </CarouselItem>
          ))}
        </Carousel>
      </section>

      {/* Seção 2: Área de Busca */}
      <section className="container mx-auto px-4 md:px-6 py-8">
        <div className="max-w-3xl mx-auto">
          <h3 className="text-center text-2xl font-semibold text-slate-800 mb-4">
            Encontre o que você precisa
          </h3>
          {/* AJUSTE: 
            - Por padrão (mobile), usamos 'flex-col'.
            - Em telas pequenas para cima (sm:), mudamos para 'flex-row' e 'items-end'.
          */}
          <div className="flex flex-col sm:flex-row sm:items-end gap-2">
            <Input 
              type="text" 
              placeholder="Busque por consultas, exames, médicos..." 
              icon={<Search />} 
              label="" 
              className="h-11 text-base w-full" // Garante largura total no mobile
            />
            {/* O botão já tem a altura correta (h-11) por causa do size="lg" */}
            <Button size="lg" className="w-full sm:w-auto">Buscar</Button>
          </div>
        </div>
      </section>
      
      {/* Seção 3: Navegue por Categorias */}
      <section className="container mx-auto px-4 md:px-6 py-12">
        <h2 className="text-2xl font-bold text-slate-800 mb-6">
          Navegue por Categorias
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