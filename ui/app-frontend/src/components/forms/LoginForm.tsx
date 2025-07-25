// src/components/forms/LoginForm.tsx
"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { useState } from "react";
import { Mail, Lock } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";

// Schema de validação com a sintaxe moderna e mais robusta
const loginSchema = z.object({
  email: z.string({
      required_error: "O campo de e-mail é obrigatório.",
    })
    .min(1, { message: "O e-mail não pode estar vazio." })
    .email({ message: "Por favor, insira um e-mail válido." }),
  password: z.string({
      required_error: "O campo de senha é obrigatório.",
    })
    .min(8, { message: "A senha deve ter no mínimo 8 caracteres." }),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export function LoginForm() {
  const [apiError, setApiError] = useState<string | null>(null);
  const { login } = useAuth();
  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });
  const { formState: { errors, isSubmitting } } = form;

  async function onSubmit(data: LoginFormValues) {
    setApiError(null);
    try {
      await login({ username: data.email, password: data.password });
    } catch (err: any) {
      setApiError(err.message || "Ocorreu um erro inesperado.");
    }
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <Input
          id="email"
          label="E-mail"
          type="email"
          placeholder="seu@email.com"
          icon={<Mail />}
          disabled={isSubmitting}
          {...form.register("email")}
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
        )}
      </div>
      <div>
        <Input
          id="password"
          label="Senha"
          type="password"
          placeholder="Sua senha"
          icon={<Lock />}
          disabled={isSubmitting}
          {...form.register("password")}
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
        )}
      </div>
      <div className="flex items-center justify-end">
        <Link href="#" className="text-sm font-medium text-slate-900 hover:underline">
          Esqueceu a senha?
        </Link>
      </div>

      {apiError && (
        <p className="text-sm font-medium text-red-600 text-center">{apiError}</p>
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