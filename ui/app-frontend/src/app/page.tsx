// src/app/page.tsx
"use client"; // Necessário para usar o componente LoginModal que é do cliente

import { LoginModal } from "@/components/auth/LoginModal";
import { Button } from "@/components/ui/Button";
import { Stethoscope, CalendarDays, Video } from "lucide-react"; // Ícones para a seção de benefícios
import Link from "next/link";

export default function HomePage() {
  return (
    // Usamos um fragmento para não adicionar um div extra desnecessário
    <>
      {/* Seção 1: Hero - A primeira impressão */}
      <section className="w-full py-20 md:py-32 lg:py-40">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center space-y-8 text-center"> {/* Aumentei o espaçamento para 'space-y-8' */}
            <div className="space-y-4">
              <h1 className="font-serif text-4xl font-bold tracking-tighter sm:text-5xl md:text-1xl text-slate-900">
                A saúde que você precisa, onde você estiver.
              </h1>
              <p className="mx-auto max-w-[700px] text-slate-600 md:text-1xl">
                Zello conecta você a profissionais de saúde qualificados por meio de teleconsultas seguras e convenientes. Cuide de si mesmo sem sair de casa.
              </p>
            </div>

            {/* Chamada para Ação (CTA) com botões ajustados */}
            <div className="mx-auto w-full max-w-sm grid grid-cols-2 gap-4">
              {/* O LoginModal agora tem seu botão com largura total (w-full) por padrão */}
              <LoginModal buttonSize="lg" buttonVariant="primary" />
              
              {/* Ajuste no Link para funcionar corretamente com o `asChild` do nosso componente Button */}
              <Link href="/cadastro" legacyBehavior passHref>
                <Button asChild variant="outline" size="lg">
                  <a>Criar Conta</a>
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Seção 2: Benefícios - O que oferecemos */}
      <section className="w-full py-12 md:py-24 lg:py-32 bg-white">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center justify-center space-y-4 text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl text-slate-900">
              Uma nova forma de cuidar de você
            </h2>
            <p className="max-w-[900px] text-slate-600 md:text-lg">
              Nossa plataforma foi desenhada para ser simples, segura e eficiente.
            </p>
          </div>
          {/* Grid responsivo para os cartões de benefícios */}
          <div className="mx-auto grid max-w-5xl items-start gap-8 sm:grid-cols-2 md:grid-cols-3">
            {/* Benefício 1 */}
            <div className="flex flex-col items-center text-center gap-2">
              <div className="bg-slate-100 p-4 rounded-full">
                <Stethoscope className="h-8 w-8 text-slate-900" />
              </div>
              <h3 className="text-xl font-bold">Especialistas Qualificados</h3>
              <p className="text-sm text-slate-600">
                Acesse uma rede de médicos e profissionais de diversas especialidades, prontos para te atender.
              </p>
            </div>
            {/* Benefício 2 */}
            <div className="flex flex-col items-center text-center gap-2">
              <div className="bg-slate-100 p-4 rounded-full">
                <CalendarDays className="h-8 w-8 text-slate-900" />
              </div>
              <h3 className="text-xl font-bold">Agendamento Flexível</h3>
              <p className="text-sm text-slate-600">
                Encontre horários que se encaixam na sua rotina e agende suas consultas de forma rápida e fácil.
              </p>
            </div>
            {/* Benefício 3 */}
            <div className="flex flex-col items-center text-center gap-2">
              <div className="bg-slate-100 p-4 rounded-full">
                <Video className="h-8 w-8 text-slate-900" />
              </div>
              <h3 className="text-xl font-bold">Consultas por Vídeo</h3>
              <p className="text-sm text-slate-600">
                Realize suas consultas por vídeo em alta qualidade, com total segurança e privacidade.
              </p>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}