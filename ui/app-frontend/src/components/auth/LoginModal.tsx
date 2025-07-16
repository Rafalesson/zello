// src/components/auth/LoginModal.tsx
"use client";

import { Modal, ModalContent, ModalTrigger } from "@/components/ui/Modal";
import { Button, type ButtonProps } from "@/components/ui/Button";
import { LoginForm } from "../forms/LoginForm";
import Image from "next/image";

interface LoginModalProps {
  buttonSize?: ButtonProps['size'];
  buttonVariant?: ButtonProps['variant'];
  buttonClassName?: string; // Propriedade adicionada para classes customizadas
}

export function LoginModal({ buttonSize, buttonVariant, buttonClassName }: LoginModalProps) {
  return (
    <Modal>
      <ModalTrigger asChild>
        {/* Passamos a nova prop de classe para o botão */}
        <Button variant={buttonVariant} size={buttonSize} className={buttonClassName}>
          Entrar
        </Button>
      </ModalTrigger>

      <ModalContent className="p-0 max-w-4xl overflow-hidden">
        <div className="grid grid-cols-1 md:grid-cols-2">
          <div className="hidden md:block relative h-full">
            <Image
              src="/images/login-hero.svg"
              alt="Profissional de saúde utilizando um laptop"
              fill
              className="object-cover"
            />
          </div>

          <div className="p-8 md:p-12 flex flex-col justify-center bg-white">
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