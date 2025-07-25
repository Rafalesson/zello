// src/schemas/profileSchema.ts
import * as z from "zod";

export const profileSchema = z.object({
  nome_completo: z.string().min(3, { message: "O nome completo é obrigatório." }),
  telefone: z.string().optional(),
  foto_perfil_url: z.string().url({ message: "Por favor, insira uma URL válida." }).optional().or(z.literal('')),
});

export type ProfileFormValues = z.infer<typeof profileSchema>;