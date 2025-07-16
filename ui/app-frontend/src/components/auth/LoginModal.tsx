// src/components/auth/LoginModal.tsx
"use client";

import React from "react";
import Image from "next/image";
import { Modal, ModalContent, ModalTrigger, DialogTitle, DialogDescription } from "@/components/ui/Modal";
import { LoginForm } from "../forms/LoginForm";

export function LoginModal({ children }: { children: React.ReactNode }) {
  return (
    <Modal>
      <ModalTrigger asChild>{children}</ModalTrigger>
      <ModalContent className="p-0 max-w-4xl overflow-hidden">
        <DialogTitle className="sr-only">Login</DialogTitle>
        <DialogDescription className="sr-only">Formulário para acessar sua conta Zello.</DialogDescription>

        <div className="grid grid-cols-1 md:grid-cols-2">

          {/* Coluna da Esquerda (IMAGEM) */}
          <div className="hidden md:block relative h-full">
            <Image
              src="/images/login-hero.svg" 
              alt="Profissional de saúde utilizando um laptop"
              fill
              className="object-cover"
            />
          </div>

          {/* Coluna da Direita (FORMULÁRIO) */}
          <div className="p-8 md:p-12 flex flex-col justify-center">
            <div className="flex flex-col space-y-2 text-center mb-8">
              <h1 className="font-serif text-4xl font-bold tracking-tight text-slate-900">
                Bem-vindo(a)
              </h1>
              <p className="text-md text-slate-500">
                Acesse sua conta para continuar.
              </p>
            </div>
            <LoginForm />
          </div>

        </div>
      </ModalContent>
    </Modal>
  );
}