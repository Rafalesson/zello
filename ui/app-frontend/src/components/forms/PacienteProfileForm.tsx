// src/components/forms/ProfileForm.tsx
"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { profileSchema, type ProfileFormValues } from "@/schemas/profileSchema";
import { Input } from "../ui/Input";
import { Button } from "../ui/Button";

interface ProfileFormProps {
  currentUserData: {
    nome_completo: string;
    telefone?: string | null;
    foto_perfil_url?: string | null; // Adicionado
  };
  onSubmit: (data: ProfileFormValues) => Promise<void>;
}

export function ProfileForm({ currentUserData, onSubmit }: ProfileFormProps) {
  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      nome_completo: currentUserData.nome_completo || "",
      telefone: currentUserData.telefone || "",
      foto_perfil_url: currentUserData.foto_perfil_url || "", // Adicionado
    },
  });

  const { isSubmitting } = form.formState;

  useEffect(() => {
    form.reset({
        nome_completo: currentUserData.nome_completo || "",
        telefone: currentUserData.telefone || "",
        foto_perfil_url: currentUserData.foto_perfil_url || "", // Adicionado
    });
  }, [currentUserData, form]);

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6 max-w-lg">
      <Input
        id="nome_completo"
        label="Nome Completo"
        type="text"
        disabled={isSubmitting}
        {...form.register("nome_completo")}
      />
      <Input
        id="telefone"
        label="Telefone"
        type="tel"
        placeholder="(XX) XXXXX-XXXX"
        disabled={isSubmitting}
        {...form.register("telefone")}
      />
      {/* NOVO CAMPO PARA FOTO */}
      <Input
        id="foto_perfil_url"
        label="URL da Foto de Perfil"
        type="text"
        placeholder="https://exemplo.com/sua-foto.jpg"
        disabled={isSubmitting}
        {...form.register("foto_perfil_url")}
      />
      <div className="pt-2">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Salvando..." : "Salvar Alterações"}
        </Button>
      </div>
    </form>
  );
}