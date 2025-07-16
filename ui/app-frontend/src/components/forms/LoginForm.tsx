// src/components/forms/LoginForm.tsx
"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { useState } from "react";
import { Mail, Lock } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
// O Checkbox não é mais necessário aqui
// import { Checkbox } from "@/components/ui/Checkbox"; 
import { useAuth } from "@/context/AuthContext";
import Link from "next/link";

// Schema de validação simplificado, sem o 'rememberMe'
const loginSchema = z.object({
  email: z.string().email({ message: "Por favor, insira um e-mail válido." }),
  password: z.string().min(8, { message: "A senha deve ter no mínimo 8 caracteres." }),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export function LoginForm() {
  const [error, setError] = useState<string | null>(null);
  const { login } = useAuth();
  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });
  const { isSubmitting } = form.formState;

  // Função para submissão BEM-SUCEDIDA
  async function onSubmit(data: LoginFormValues) {
    console.log("VALIDAÇÃO OK! Dados enviados:", data);
    setError(null);
    try {
      await login({ username: data.email, password: data.password });
    } catch (err: any) {
      setError(err.message || "Ocorreu um erro inesperado.");
    }
  }
  
  // Função para submissão que FALHOU na validação
  function onInvalid(errors: any) {
    console.error("VALIDAÇÃO FALHOU! Erros:", errors);
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit, onInvalid)} className="space-y-6">
      <div className="space-y-4">
        <Input
          id="email"
          label="E-mail"
          type="email"
          placeholder="seu@email.com"
          icon={<Mail />}
          disabled={isSubmitting}
          {...form.register("email")}
        />
        {form.formState.errors.email && (
          <p className="text-sm text-red-600">{form.formState.errors.email.message}</p>
        )}
      </div>
      <div className="space-y-4">
        <Input
          id="password"
          label="Senha"
          type="password"
          placeholder="Sua senha"
          icon={<Lock />}
          disabled={isSubmitting}
          {...form.register("password")}
        />
        {form.formState.errors.password && (
          <p className="text-sm text-red-600">{form.formState.errors.password.message}</p>
        )}
      </div>
      
      {/* Seção 'Lembrar de mim' e 'Esqueceu a senha' removida para simplificar */}
      <div className="flex items-center justify-end">
        <Link href="#" className="text-sm font-medium text-slate-900 hover:underline">
          Esqueceu a senha?
        </Link>
      </div>

      {error && (
        <p className="text-sm font-medium text-red-600 text-center">{error}</p>
      )}

      <Button type="submit" className="w-full" disabled={isSubmitting}>
        {isSubmitting ? "Entrando..." : "Entrar"}
      </Button>

      <p className="text-center text-sm text-slate-600">
        Novo por aqui?{" "}
        <Link href="/cadastro" className="font-semibold text-slate-900 hover:underline">
          Crie uma conta
        </Link>
      </p>
    </form>
  );
}